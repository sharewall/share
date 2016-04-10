from django.contrib import admin
from webmaster_area.models import WebmasterAreaModel, PageDetail, AreaCategory, AreaToday, PageToday

admin.site.register(WebmasterAreaModel)
admin.site.register(PageDetail)
admin.site.register(AreaCategory)
admin.site.register(AreaToday)
admin.site.register(PageToday)
