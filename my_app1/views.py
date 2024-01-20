from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from .models import MyModel4


# Create your views here.
def get_view(request, pk: int = None):
    if pk:
        data = [MyModel4.objects.get(pk=pk)]
    else:
        data = MyModel4.objects.filter(
            my_model1__name__startswith="Person",
            my_model1__created_at__year=2024,
            my_model1__age__gt=18,
            my_model3__hair_description__contains="description",
            hair_color__isnull=False
        ).order_by("my_model1__id")[:10]

    response = generate_table(data)

    return HttpResponse(response)


def put_view(request, pk: int, color: str):
    pass


def post_view(request, color: str, m_id1: int, m_id2: int, m_id3: int):
    pass


def delete_view(request, pk:int):
    pass


def generate_table(data):
    response = """<table border='1'><tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Favorite Color</th>
                    <th>Is Hair Styled</th></tr>"""
    for d in data:
        response += f"""<tr><td>{d.my_model1.id}</td>
                        <td>{d.my_model1.name}</td>
                        <td>{", ".join(instance.favorite_color for instance in d.my_model2.all())}</td>
                        <td>{d.my_model3.is_hair_styled}</td></tr>"""
    response += "</table>"
    return response
