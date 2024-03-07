from django.shortcuts import get_object_or_404
from django_tables2 import SingleTableView, RequestConfig
from django_filters.views import FilterView
from dashboard.models import FullDataModel
from dashboard.utils import FullDataTable, FullDataFilter
from django.contrib import messages
from django.http import JsonResponse
from users.utils import is_authorized


class DataView(SingleTableView, FilterView):
    model = FullDataModel
    table_class = FullDataTable
    template_name = 'data.html'
    filterset_class = FullDataFilter
    table_pagination = {'per_page': 50}

    def __init__(self, *args, **kwargs):
        self.object_list = kwargs.pop('queryset', None)
        super().__init__(*args, **kwargs)

    # # Custom filtering
    # def get_queryset(self):
    #     return FullDataModel.objects.filter(
    #         data__name__startswith="Person",
    #         data__created_at__year=2024,
    #         data__age__gt=18,
    #         hair__hair_description__contains="description",
    #         hair_color__isnull=False
    #     ).order_by("id")

    def get_table_data(self):
        return self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_table_data())
        table = FullDataTable(context['filter'].qs)
        RequestConfig(self.request, paginate=self.table_pagination).configure(table)
        context['table'] = table
        context['title'] = 'Data'
        return context

    @staticmethod
    @is_authorized(permissions=['delete_data'])
    def delete(request, pk):
        if request.method == 'DELETE':
            instance = get_object_or_404(FullDataModel, pk=pk)
            data = instance.data
            instance.delete()
            data.delete()
            messages.success(request, "Deleted.")
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
