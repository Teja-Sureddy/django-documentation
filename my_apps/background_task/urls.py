from django.urls import path
from my_apps.background_task.views import (
    ThreadingView,
    DjangoQView,
    AsyncioView,
    MultiProcessingView,
    CeleryView,
)
from django.contrib.auth.decorators import login_required

app_name = "background"

urlpatterns = [
    path("threading/", login_required(ThreadingView.as_view()), name="threading"),
    path("django_q/", login_required(DjangoQView.as_view()), name="django_q"),
    path("asyncio/", login_required(AsyncioView.as_view()), name="asyncio"),
    path(
        "multiprocessing/",
        login_required(MultiProcessingView.as_view()),
        name="multiprocessing",
    ),
    path("celery/", login_required(CeleryView.as_view()), name="celery"),
]
