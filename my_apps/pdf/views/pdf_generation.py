from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from my_apps.pdf.utils import InvoiceReportLabPlatypus
from my_apps.pdf.models import Invoice


def generate_pdf_view(request):
    """
    It uses reportlab to generate the pdf and send it as a response.
    """
    if request.method == 'GET':
        # disposition: 'inline' will render the pdf, 'attachment' will download the pdf
        disposition = 'attachment' if request.GET.get('download') else 'inline'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'{disposition}; filename="Invoice.pdf"'
        pdf = SimpleDocTemplate(response, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)

        invoices = Invoice.objects.prefetch_related('item_set').all()
        offset = int(request.GET.get('offset', 0))
        offset = offset if len(invoices) > offset else 0
        invoice = invoices[offset:offset + 1][0]
        items = invoice.item_set.all()

        instance = InvoiceReportLabPlatypus(invoice, items)
        header_content = instance.get_pdf_content()
        pdf.build(header_content)
        return response
