# create_sample_pdf.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import datetime

# --- Configuration ---
FILENAME = "daily_financials.pdf"

# --- Sample Data to be written to the PDF ---
# This structure mimics the final JSON we want to achieve.
SAMPLE_DATA = [
    {
        "date": "01-JAN-2023",
        "accounts": {
            "Sales Revenue": 5250.75,
            "Service Fees": 800.00,
            "Cost of Goods Sold": -2100.50,
            "Office Supplies": -150.25,
            "Daily Total": 3800.00
        }
    },
    {
        "date": "02-JAN-2023",
        "accounts": {
            "Sales Revenue": 4800.00,
            "Service Fees": 650.50,
            "Cost of Goods Sold": -1950.00,
            "Daily Total": 3500.50
        }
    },
    {
        "date": "03-JAN-2023",
        "accounts": {
            "Sales Revenue": 6100.00,
            "Product Returns": -300.00,
            "Service Fees": 950.00,
            "Cost of Goods Sold": -2800.00,
            "Marketing Spend": -500.00,
            "Daily Total": 3450.00
        }
    },
    # This block will cause a page break
    {
        "date": "04-JAN-2023",
        "accounts": {
            "Sales Revenue": 7200.10,
            "Service Fees": 1100.00,
            "Cost of Goods Sold": -3100.90,
            "Daily Total": 5199.20
        }
    },
    {
        "date": "05-JAN-2023",
        "accounts": {
            "Sales Revenue": 5550.00,
            "Service Fees": 750.50,
            "Cost of Goods Sold": -2200.00,
            "Bank Fees": -25.00,
            "Daily Total": 4075.50
        }
    }
]

def draw_header(c, page_num):
    """Draws the header on each page."""
    c.saveState()
    c.setFont('Helvetica-Bold', 10)
    c.drawString(inch, 10.5 * inch, "My Company Inc. - Daily Statement")
    c.drawRightString(7.5 * inch, 10.5 * inch, f"CONFIDENTIAL    Page {page_num}")
    c.line(inch, 10.4 * inch, 7.5 * inch, 10.4 * inch)
    c.restoreState()

def draw_footer(c):
    """Draws the footer on each page."""
    c.saveState()
    c.setFont('Helvetica', 8)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(inch, 0.75 * inch, f"Report Generated: {timestamp}")
    c.restoreState()

def create_financial_pdf():
    """Generates a multi-page PDF with headers, footers, and daily financial data."""
    c = canvas.Canvas(FILENAME, pagesize=letter)
    width, height = letter

    # Set margins
    top_margin = 1.0 * inch
    bottom_margin = 1.0 * inch
    line_height = 0.25 * inch

    # Initial position for writing content
    y_position = height - top_margin
    page_number = 1
    
    draw_header(c, page_number)

    for day_data in SAMPLE_DATA:
        # Check if there's enough space for the next block (date + accounts)
        block_height = (len(day_data["accounts"]) + 2) * line_height
        if y_position - block_height < bottom_margin:
            # Not enough space, create a new page
            draw_footer(c)
            c.showPage()
            page_number += 1
            y_position = height - top_margin
            draw_header(c, page_number)
            
        # Draw the date
        c.setFont('Helvetica-Bold', 12)
        c.drawString(inch, y_position, f"DATE: {day_data['date']}")
        y_position -= line_height * 1.5

        # Draw the accounts for the day
        c.setFont('Helvetica', 11)
        for name, value in day_data["accounts"].items():
            # Format value as a string with commas and two decimal places
            value_str = f"{value:,.2f}"
            
            # This simulates the "Name ....... Value" format our parser expects
            # It uses a long string of dots that the regex `\.{2,}` can match.
            line_text = f"{name} ............................................................. {value_str}"
            
            c.drawString(1.2 * inch, y_position, name)
            c.drawRightString(width - inch, y_position, value_str)
            y_position -= line_height

        y_position -= line_height # Add extra space between blocks

    # Finalize the last page
    draw_footer(c)
    c.save()
    print(f"Successfully created '{FILENAME}'")


if __name__ == '__main__':
    create_financial_pdf()
