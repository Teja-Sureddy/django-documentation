from django.urls import path
from dashboard.views import DataView, DataModifyView
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView


app_name = "dashboard"
urlpatterns = [
    path("", RedirectView.as_view(url='data/'), name='data_redirect'),
    path("data/", login_required(DataView.as_view()), name="data"),
    path("data/add/", login_required(DataModifyView.as_view()), name="data-add"),
    path("data/edit/<pk>/", login_required(DataModifyView.as_view()), name="data-edit"),
    path("data/delete/<int:pk>/", login_required(DataView.as_view()), name="data-delete"),
]
