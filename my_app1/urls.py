from django.urls import path
from .views import GetView


app_name = "my_app1"
urlpatterns = [
    path("crud/", GetView.as_view(), name="crud")
]
