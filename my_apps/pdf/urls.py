from django.urls import path
from my_apps.pdf.views import generate_pdf_view, processing_pdf_view
from django.contrib.auth.decorators import login_required

app_name = "pdf"

urlpatterns = [
    path('generate/', login_required(generate_pdf_view), name='generate'),
    path('process/', login_required(processing_pdf_view), name='process')
]
