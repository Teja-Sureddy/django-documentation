from django.contrib import admin
from my_apps.dashboard.models import Data, Color, Hair, FullData

admin.site.register(Data)
admin.site.register(Color)
admin.site.register(Hair)
admin.site.register(FullData)
