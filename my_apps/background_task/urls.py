from django.urls import path
from my_apps.background_task.views import ThreadingView
from django.contrib.auth.decorators import login_required

app_name = "background"

urlpatterns = [
    path('threading/', login_required(ThreadingView.as_view()), name='bg_threading')
]
