from django.contrib import admin
from dashboard.models import DataModel, ColorModel, HairModel, FullDataModel

admin.site.register(DataModel)
admin.site.register(ColorModel)
admin.site.register(HairModel)
admin.site.register(FullDataModel)
