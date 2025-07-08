import pdfplumber
import re
import json

def find_header_boundary_from_lines(page):
    """
    Finds the y-coordinate of the bottom-most of the two header lines.
    This dynamically identifies the top of the content area for EACH page.
    """
    horizontal_lines = [line for line in page.lines if abs(line['y0'] - line['y1']) < 1]
    top_of_page_threshold = page.height * 0.80
    header_lines = [line for line in horizontal_lines if line['y0'] > top_of_page_threshold]
    
    if len(header_lines) >= 2:
        sorted_header_lines = sorted(header_lines, key=lambda line: line['y0'], reverse=True)
        boundary_line = sorted_header_lines[1]
        return boundary_line['y0']
    
    print(f"Warning: Could not find two header lines on page {page.page_number}. Using a default margin.")
    return page.height - (1.3 * 72)

def parse_complex_pdf_robust(pdf_path):
    """
    Parses the complex financial PDF using a robust two-stage process.
    """
    # --- STAGE 1: CLEAN AND CONSOLIDATE ALL CONTENT LINES ---
    
    all_content_lines = []
    with pdfplumber.open(pdf_path) as pdf:
        # Loop through each page SOLELY to clean it and extract its text.
        for page in pdf.pages:
            # Find the header boundary FOR THIS SPECIFIC PAGE.
            header_boundary_y = find_header_boundary_from_lines(page)
            
            # Crop the page to exclude the header.
            crop_box = (0, 0, page.width, header_boundary_y)
            content_area = page.crop(bbox=crop_box)
            
            # Extract text from the clean content area.
            text = content_area.extract_text(x_tolerance=2, y_tolerance=5, layout=True)
            
            if text:
                # Add the lines from this page to our master list.
                all_content_lines.extend(text.split('\n'))

    # --- STAGE 2: PARSE THE CONSOLIDATED, CLEAN DATA ---

    # Regex patterns (same as before)
    date_pattern = re.compile(r"^\s*DATE:\s*(\d{2}-[A-Z]{3}-\d{4})\s*$")
    data_row_pattern = re.compile(r"(.+?)\s{2,}([\d,.-]+)$")
    # A pattern to detect section titles that might have been part of a data row
    # This helps avoid misinterpreting "Description" or "Amount" as data
    non_data_keywords = re.compile(r"Description|Amount", re.IGNORECASE)

    all_days_data = []
    current_day_data = None
    current_section_data = None

    # Now, loop through the single, clean list of lines.
    for line in all_content_lines:
        line = line.strip()
        if not line:
            continue

        date_match = date_pattern.match(line)
        data_match = data_row_pattern.search(line)
        is_a_keyword = non_data_keywords.search(line)

        # --- STATE MACHINE LOGIC (applied to the clean stream) ---
        if date_match:
            if current_section_data and current_day_data:
                current_day_data['sections'].append(current_section_data)
            if current_day_data:
                all_days_data.append(current_day_data)
            current_day_data = {"date": date_match.group(1), "sections": []}
            current_section_data = None
        
        # Check if it's a data row and NOT a header keyword like "Description"
        elif data_match and not is_a_keyword and current_section_data:
            description = data_match.group(1).strip()
            value_str = data_match.group(2).replace(',', '')
            value = float(value_str)
            current_section_data['data'].append((description, value))
        
        elif current_day_data: # If it's not a date or data, it must be a section title.
            if current_section_data:
                current_day_data['sections'].append(current_section_data)
            section_title = line
            section_type = "transactions" if "TRANSACTIONS" in section_title else "summary"
            current_section_data = {
                "title": section_title,
                "type": section_type,
                "data": []
            }

    # Finalize the very last entry after the loop finishes
    if current_section_data and current_day_data:
        current_day_data['sections'].append(current_section_data)
    if current_day_data:
        all_days_data.append(current_day_data)

    # Post-processing to convert summary data to a dictionary
    for day in all_days_data:
        for section in day['sections']:
            if section['type'] == 'summary':
                section['data'] = dict(section['data'])

    return all_days_data

def main():
    pdf_file = "complex_financials.pdf"
    parsed_data = parse_complex_pdf_robust(pdf_file)
    json_output = json.dumps(parsed_data, indent=2)
    print(json_output)
    with open("complex_output_robust.json", "w") as f:
        f.write(json_output)
    print(f"\nSuccessfully saved parsed data to complex_output_robust.json")

if __name__ == "__main__":
    main()
