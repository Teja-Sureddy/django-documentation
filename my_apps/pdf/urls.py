from django.urls import path
from my_apps.pdf.views import generate_pdf_view
from django.contrib.auth.decorators import login_required

app_name = "pdf"

urlpatterns = [
    path('generate_pdf/', login_required(generate_pdf_view), name='generate_pdf')
]
