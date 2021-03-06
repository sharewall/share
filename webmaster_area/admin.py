from django.contrib import admin
from webmaster_area.models import WebmasterAreaModel, PageDetail, AreaCategory, AreaToday, PageToday, Faq

admin.actions.delete_selected.short_description = "Удалить"

class WebmasterAreaModelAdmin(admin.ModelAdmin):
    list_display=('id','getBtnConstructID', 'name_area', 'url', 'ad_type', 'area_category', 'total_share_counter', 'total_social_counter')
    list_filter=('area_category', 'ad_type')
    search_fields=['id', 'buttons_constructor__id', 'name_area', 'url']

    def getBtnConstructID(self, obj):
        return str(obj.buttons_constructor.id)
    getBtnConstructID.short_description = 'relatedBtnConstructID'
    getBtnConstructID.admin_order_field = 'buttons_constructor__id'

class FaqAdmin(admin.ModelAdmin):
    list_display=('id','header', 'text')
    search_fields=['id', 'header', 'text']

class AreaCategoryAdmin(admin.ModelAdmin):
    list_display=('id','name')
    search_fields=['id', 'name']

class AreaTodayAdmin(admin.ModelAdmin):
    list_display=('id','getWMAreaID', 'date', 'today_share_counter', 'today_social_counter', 'today_show_counter', 'today_click_counter', 'today_money')
    search_fields=['id', 'webmaster_area__id', 'date']

    def getWMAreaID(self, obj):
        if obj.webmaster_area:
            return str(obj.webmaster_area.id)
        else:
            return str("Without Webmaster Area")
    getWMAreaID.short_description = 'relatedWebmasterAreaID'
    getWMAreaID.admin_order_field = 'webmaster_area__id'

class PageDetailAdmin(admin.ModelAdmin):
    list_display=('id','getWMAreaID', 'title', 'url', 'total_social_counter', 'total_share_counter')
    search_fields=['id', 'webmaster_area__id', 'title', 'url']

    def getWMAreaID(self, obj):
        if obj.webmaster_area:
            return str(obj.webmaster_area.id)
        else:
            return str("Without Webmaster Area")
    getWMAreaID.short_description = 'relatedWebmasterAreaID'
    getWMAreaID.admin_order_field = 'webmaster_area__id'

class PageTodayAdmin(admin.ModelAdmin):
    list_display=('id','getPageDetailID', 'date', 'getOddShare', 'getOddSocial', 'today_share_counter', 'default_today_share_counter', 'today_social_counter', 'default_today_social_counter', 'today_show_counter', 'default_today_show_counter', 'today_click_counter', 'default_today_click_counter', 'today_money', 'default_today_money')
    search_fields=['id', 'page_detail__id', 'date']
    fields=('id', 'getPageDetailID', 'date', ('getOddShare', 'getOddSocial'), ('today_share_counter', 'default_today_share_counter'), ('today_social_counter', 'default_today_social_counter'), ('today_show_counter','default_today_show_counter'), ('today_click_counter','default_today_click_counter'), ('today_money','default_today_money') )
    readonly_fields=('id', 'getPageDetailID', 'date', 'getOddShare', 'getOddSocial')

    def getPageDetailID(self, obj):
        if obj.page_detail:
            return str(obj.page_detail.id)
        else:
            return str("Without Page Detail")
    getPageDetailID.short_description = 'relatedPageDetailID'
    getPageDetailID.admin_order_field = 'page_detail__id'

admin.site.register(WebmasterAreaModel, WebmasterAreaModelAdmin)
admin.site.register(PageDetail, PageDetailAdmin)
admin.site.register(AreaCategory, AreaCategoryAdmin)
admin.site.register(AreaToday, AreaTodayAdmin)
admin.site.register(PageToday, PageTodayAdmin)
admin.site.register(Faq, FaqAdmin)
