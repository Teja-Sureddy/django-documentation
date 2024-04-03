from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from django.contrib.staticfiles.finders import find
from my_project.settings import BASE_DIR


def generate_pdf_view(request):
    """
    It uses reportlab to generate the pdf and send it as a response.
    """
    if request.method == 'GET':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="generated_pdf.pdf"'
        pdf = SimpleDocTemplate(response, pagesize=letter)

        # Add a logo to the PDF
        logo_path = find(BASE_DIR.joinpath('static/assets/google.png'))
        logo = ImageReader(logo_path)
        logo_width, logo_height = logo.getSize()
        aspect_ratio = logo_height / logo_width
        logo = logo_path and Image(logo_path, width=1 * inch, height=(1 * inch) * aspect_ratio) or None

        # Create a Paragraph for text
        styles = getSampleStyleSheet()
        text = """Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the 
        industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled 
        it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic 
        typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset 
        sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker 
        including versions of Lorem Ipsum."""
        paragraph = Paragraph(text, styles["Normal"])

        # Create a table with data
        data = [
            ['Column 1', 'Column 2', 'Column 3'],
            ['Data 1', 'Data 2', 'Data 3'],
            ['Data 4', 'Data 5', 'Data 6']
        ]
        col_widths = [(letter[0] - 2 * inch) / len(data[0])] * len(data[0])
        table = Table(data, colWidths=col_widths)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black)])
        table.setStyle(style)

        # Build elements
        elements = []
        if logo:
            elements.append(logo)
            elements.append(Spacer(1, 0.2 * inch))
        elements.append(paragraph)
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(table)

        # Add elements to the PDF
        pdf.build(elements)
        return response
