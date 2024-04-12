from django.http import HttpResponse, HttpResponseRedirect
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from my_apps.pdf.utils import InvoiceReportLabPlatypus
from my_apps.pdf.models import Invoice
from django.core.mail import EmailMessage
import tempfile
import os
from django.contrib import messages


def generate_pdf_view(request):
    """
    It uses reportlab to generate the pdf and send it as a response.
    """
    if request.method == 'GET':
        # 'inline' will render the pdf, 'attachment' will download the pdf
        disposition = 'attachment' if request.GET.get('download') else 'inline'
        offset = int(request.GET.get('offset', 0))

        response = generate_pdf(disposition, offset)
        if request.GET.get('email'):
            send_email_with_attachment(response, request.user)
            messages.success(request, f'Invoice sent to {request.user.email}.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return response


def generate_pdf(disposition, offset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'{disposition}; filename="Invoice.pdf"'
    pdf = SimpleDocTemplate(response, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50, title="Invoice")

    # get invoice data
    invoices = Invoice.objects.prefetch_related('item_set').all()
    offset = offset if len(invoices) > offset else 0
    invoice = invoices[offset:offset + 1][0]
    items = invoice.item_set.all()

    instance = InvoiceReportLabPlatypus(invoice, items)
    header_content = instance.get_pdf_content()
    pdf.build(header_content)
    return response


def send_email_with_attachment(response, user):
    # save the file to the os temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', prefix='Invoice_') as temp_pdf:
        temp_pdf.write(response.content)
        temp_pdf_path = temp_pdf.name
        temp_pdf.close()

    # send an email with attachment
    email = EmailMessage('Invoice', 'Please find the attached invoice.', to=[user.email])
    email.attach_file(temp_pdf_path)
    # email.send()

    # delete the file from os temp location
    os.unlink(temp_pdf_path)
