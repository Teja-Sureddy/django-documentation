from django.urls import path, include
from django.shortcuts import redirect, reverse
from .views import get_view, put_view, post_view, delete_view

curd_patterns = [
    path('', lambda request: redirect(reverse('my_app1:get')), name='redirect_home_to_get'),
    path("get/", get_view, name="get"),
    path("get/<int:pk>/", get_view, name="get-one"),
    path("put/<int:pk>/<str:color>/", put_view, name="put"),
    path("post/<str:color>/<int:m_id1>/<int:m_id2>/<int:m_id3>/", post_view, name="post"),
    path("delete/<int:pk>/", delete_view, name="delete")
]

app_name = "my_app1"
urlpatterns = [
    path("crud/", include(curd_patterns), name="crud")
]
