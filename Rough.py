# create_complex_pdf.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from PIL import Image, ImageDraw, ImageFont
import datetime
import os

# --- Configuration ---
FILENAME = "complex_financials.pdf"
LOGO_FILENAME = "company_logo.png"

# --- New, more complex data structure ---
COMPLEX_SAMPLE_DATA = [
    {
        "date": "01-APR-2023",
        "sections": [
            {"title": "TYPES OF CREDIT", "type": "summary", "data": {"Cash Sales": 8500.50, "Online Sales": 12345.25}},
            {"title": "TYPES OF DEBIT", "type": "summary", "data": {"Cost of Goods": -6700.00, "Salaries": -4500.00, "Rent": -2000.00}},
            {"title": "CREDIT TRANSACTIONS", "type": "transactions", "data": [("Payment from Client A", 3500.00), ("Web Store Batch #1138", 6210.15), ("Cash Deposit", 2290.35)]},
            {"title": "DEBIT TRANSACTIONS", "type": "transactions", "data": [("Supplier ABC Payment", -2500.00), ("Office Supplies", -155.75), ("Payroll Run", -4500.00)]},
        ]
    },
    {
        "date": "02-APR-2023",
        "sections": [
            {"title": "TYPES OF CREDIT", "type": "summary", "data": {"Cash Sales": 7200.00, "Service Fees": 1500.00}},
            {"title": "CREDIT TRANSACTIONS", "type": "transactions", "data": [("Walk-in Customer", 500.00), ("Service for Client B", 1500.00), ("Cash Deposit", 6700.00)]},
        ]
    },
    {
        "date": "03-APR-2023",
        "sections": [
            {"title": "TYPES OF DEBIT", "type": "summary", "data": {"Marketing": -1200.00, "Utilities": -450.25}},
            {"title": "DEBIT TRANSACTIONS", "type": "transactions", "data": [("Google Ads Campaign", -1000.00), ("Electricity Bill", -320.10), ("Internet Bill", -130.15), ("Facebook Ads", -200.00)]},
        ]
    }
]

def create_placeholder_logo():
    """Generates a simple placeholder logo image if it doesn't exist."""
    if os.path.exists(LOGO_FILENAME):
        return
    
    img = Image.new('RGB', (120, 60), color = (73, 109, 137))
    d = ImageDraw.Draw(img)
    try:
        # Use a common font, fallback if not found
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    d.text((10,15), "LOGO", font=font, fill=(255,255,255))
    img.save(LOGO_FILENAME)
    print(f"Created placeholder logo: {LOGO_FILENAME}")

def draw_header(c, page_num):
    """Draws a complex header with a logo and two horizontal lines."""
    c.saveState()
    width, height = letter

    # Draw logo
    c.drawImage(LOGO_FILENAME, 0.75 * inch, height - 1.0 * inch, width=1.2*inch, height=0.6*inch)

    # Draw company text
    c.setFont('Helvetica-Bold', 14)
    c.drawString(2.2 * inch, height - 0.7 * inch, "My Global Corporation")
    c.setFont('Helvetica', 9)
    c.drawString(2.2 * inch, height - 0.9 * inch, "123 Automation Lane, Suite 404, Techville, 12345")

    # Draw page number
    c.drawRightString(width - 0.75 * inch, height - 0.7 * inch, f"Page {page_num}")

    # --- Draw the two horizontal lines that define the header boundary ---
    y1 = height - 1.2 * inch
    y2 = height - 1.25 * inch
    c.line(0.5 * inch, y1, width - 0.5 * inch, y1)
    c.line(0.5 * inch, y2, width - 0.5 * inch, y2)
    
    c.restoreState()
    # Return the y-coordinate of the bottom line, which is the start of our content area
    return y2


def draw_section(c, y_pos, section_data):
    """Draws a full section with title, line, and data."""
    width, _ = letter
    line_height = 0.22 * inch
    
    # Draw section title and line
    c.setFont('Helvetica-Bold', 12)
    c.drawString(inch, y_pos, section_data["title"])
    y_pos -= 0.1 * inch
    c.line(inch, y_pos, width - inch, y_pos)
    y_pos -= 0.25 * inch
    
    # Draw data based on type
    c.setFont('Helvetica', 10)
    if section_data["type"] == "summary":
        for key, value in section_data["data"].items():
            value_str = f"{value:,.2f}"
            c.drawString(1.2 * inch, y_pos, key)
            c.drawRightString(width - inch, y_pos, value_str)
            y_pos -= line_height
    
    elif section_data["type"] == "transactions":
        # Draw column headers
        c.setFont('Helvetica-Oblique', 10)
        c.drawString(1.2 * inch, y_pos, "Description")
        c.drawRightString(width - inch, y_pos, "Amount")
        y_pos -= line_height * 0.8
        c.setFont('Helvetica', 10)
        for desc, value in section_data["data"]:
            value_str = f"{value:,.2f}"
            c.drawString(1.2 * inch, y_pos, desc)
            c.drawRightString(width - inch, y_pos, value_str)
            y_pos -= line_height
            
    return y_pos


def create_complex_financial_pdf():
    """Generates the multi-section, multi-page PDF."""
    create_placeholder_logo() # Make sure logo exists
    
    c = canvas.Canvas(FILENAME, pagesize=letter)
    width, height = letter
    bottom_margin = 0.75 * inch
    page_number = 1

    # Start the first page
    content_top_y = draw_header(c, page_number)
    y_pos = content_top_y - 0.3 * inch

    for day_data in COMPLEX_SAMPLE_DATA:
        # --- Page Break Logic ---
        # A rough estimate of the height for the date line
        if y_pos < bottom_margin + 0.5 * inch:
            c.showPage()
            page_number += 1
            content_top_y = draw_header(c, page_number)
            y_pos = content_top_y - 0.3 * inch

        # Draw the date
        c.setFont('Helvetica-Bold', 14)
        c.drawString(inch, y_pos, f"DATE: {day_data['date']}")
        y_pos -= 0.4 * inch

        # Draw all sections for the day
        for section in day_data["sections"]:
             # Estimate section height for page break check
            num_lines = len(section["data"]) + 2
            est_height = num_lines * 0.25 * inch
            if y_pos - est_height < bottom_margin:
                c.showPage()
                page_number += 1
                content_top_y = draw_header(c, page_number)
                y_pos = content_top_y - 0.3 * inch

            y_pos = draw_section(c, y_pos, section)
            y_pos -= 0.2 * inch # Space between sections
    
    c.save()
    print(f"Successfully created '{FILENAME}'")


if __name__ == '__main__':
    create_complex_financial_pdf()
