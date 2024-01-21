from django.shortcuts import render
from django_tables2 import SingleTableView, RequestConfig
from django_filters.views import FilterView
from .models import MyModel4
from .tables import MyModel4Table
from .filters import MyModel4Filter


# Create your views here.
class GetView(SingleTableView, FilterView):
    model = MyModel4
    table_class = MyModel4Table
    template_name = 'crud.html'
    filterset_class = MyModel4Filter
    table_pagination = {'per_page': 50}

    def get_table_data(self):
        return MyModel4.objects.filter(
            my_model1__name__startswith="Person",
            my_model1__created_at__year=2024,
            my_model1__age__gt=18,
            my_model3__hair_description__contains="description",
            hair_color__isnull=False
        ).order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_table_data())
        table = MyModel4Table(context['filter'].qs)
        RequestConfig(self.request, paginate=self.table_pagination).configure(table)
        context['table'] = table
        return context


def put_view(request, pk: int, color: str):
    pass


def post_view(request, color: str, m_id1: int, m_id2: int, m_id3: int):
    pass


def delete_view(request, pk: int):
    pass
