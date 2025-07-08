import pdfplumber
import re
import json

def find_header_boundary_from_lines(page):
    """
    Finds the y-coordinate of the bottom-most of the two header lines.
    This dynamically identifies the top of the content area.
    """
    # A line is horizontal if its y0 and y1 coordinates are very close.
    horizontal_lines = [line for line in page.lines if abs(line['y0'] - line['y1']) < 1]
    
    # Header lines are expected to be in the top 20% of the page.
    top_of_page_threshold = page.height * 0.80
    header_lines = [line for line in horizontal_lines if line['y0'] > top_of_page_threshold]
    
    # We expect at least two lines in the header.
    if len(header_lines) >= 2:
        # Sort by y-coordinate, highest (top of page) first.
        sorted_header_lines = sorted(header_lines, key=lambda line: line['y0'], reverse=True)
        # The boundary is the *second* line from the top.
        boundary_line = sorted_header_lines[1]
        return boundary_line['y0']
    
    # Fallback if the expected lines aren't found.
    print(f"Warning: Could not find two header lines on page {page.page_number}. Using a default margin.")
    return page.height - (1.3 * 72) # Default to 1.3 inches from top

def parse_complex_pdf(pdf_path):
    """
    Parses the complex financial PDF by detecting header lines and section structure.
    """
    # Regex to find a line with a date
    date_pattern = re.compile(r"^\s*DATE:\s*(\d{2}-[A-Z]{3}-\d{4})\s*$")
    
    # Regex to find a data row (works for both summary and transactions)
    # Captures: 1) The description, 2) The numeric value
    data_row_pattern = re.compile(r"(.+?)\s{2,}([\d,.-]+)$")

    all_days_data = []
    current_day_data = None
    current_section_data = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 1. DYNAMICALLY FIND HEADER AND CROP
            header_boundary_y = find_header_boundary_from_lines(page)
            # Crop box is (x0, bottom, x1, top). Coordinates are from the bottom.
            crop_box = (0, 0, page.width, header_boundary_y)
            content_area = page.crop(bbox=crop_box)
            
            text = content_area.extract_text(x_tolerance=2, y_tolerance=5)
            if not text:
                continue

            # 2. PROCESS THE CLEANED TEXT LINE BY LINE
            for line in text.split('\n'):
                line = line.strip()
                if not line:
                    continue

                date_match = date_pattern.match(line)
                data_match = data_row_pattern.search(line)

                # --- STATE MACHINE LOGIC ---
                # The order of these checks is critical.

                # A. Is this a DATE line?
                if date_match:
                    # First, finalize the previous day's data before starting a new one.
                    if current_section_data and current_day_data:
                        current_day_data['sections'].append(current_section_data)
                    if current_day_data:
                        all_days_data.append(current_day_data)
                    
                    # Start a new day object
                    current_day_data = {
                        "date": date_match.group(1),
                        "sections": []
                    }
                    current_section_data = None # Reset the section

                # B. Is this a DATA ROW? (and are we inside a section?)
                elif data_match and current_section_data:
                    description = data_match.group(1).strip()
                    value_str = data_match.group(2).replace(',', '')
                    value = float(value_str)
                    current_section_data['data'].append((description, value))

                # C. If not a date or data, it must be a SECTION TITLE.
                elif current_day_data:
                    # Finalize the previous section before starting a new one.
                    if current_section_data:
                        current_day_data['sections'].append(current_section_data)
                    
                    section_title = line
                    # Infer the section type from its title
                    section_type = "transactions" if "TRANSACTIONS" in section_title else "summary"
                    
                    # Start a new section object
                    current_section_data = {
                        "title": section_title,
                        "type": section_type,
                        "data": [] # Store data as a list of tuples initially
                    }

    # After the loop, append the very last day's data
    if current_section_data and current_day_data:
        current_day_data['sections'].append(current_section_data)
    if current_day_data:
        all_days_data.append(current_day_data)

    # 3. POST-PROCESSING: Convert summary data from list to dictionary
    for day in all_days_data:
        for section in day['sections']:
            if section['type'] == 'summary':
                # Convert [(key1, val1), (key2, val2)] to {key1: val1, key2: val2}
                section['data'] = dict(section['data'])

    return all_days_data

def main():
    pdf_file = "complex_financials.pdf"
    
    parsed_data = parse_complex_pdf(pdf_file)
    
    if not parsed_data:
        print("Could not parse any data from the PDF.")
        return
        
    # Convert the final Python object to a pretty-printed JSON string
    json_output = json.dumps(parsed_data, indent=2)
    
    print(json_output)
    
    with open("complex_output.json", "w") as f:
        f.write(json_output)
    print(f"\nSuccessfully saved parsed data to complex_output.json")

if __name__ == "__main__":
    main()
