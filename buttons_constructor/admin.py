from django.contrib import admin
#from buttons_constructor.models import ButtonsConstructorModel, SocialNetworks
from buttons_constructor.models import SocialNetworks, BtnsImages, ButtonsConstructorModel, AdvertBtnImage, Advert

admin.actions.delete_selected.short_description = "Удалить"

#def yesProduct(modeladmin, request, queryset):
#   queryset.update(in_stock=True) 

#yesProduct.short_description = "В наличии"

class ButtonsConstructorModelAdmin(admin.ModelAdmin):
    list_display=('id','getCabinetID','getBtnsImagesID','social_networks','with_counter','mobile_view','with_background','form_buttons','location_buttons','size_buttons')
    list_filter=('with_counter', 'btns_images__id','mobile_view','with_background','form_buttons','location_buttons','size_buttons')
    search_fields=['id', 'cabinet_webmaster__id', 'btns_images__id']
    #fields=('id', 'getImage', 'image', ('label','the_type', 'nut_type'),('price','count','in_stock'))
    #readonly_fields=('id', 'getImage')
    #actions=[yesProduct, noProduct]

    def getCabinetID(self, obj):
        return str(obj.cabinet_webmaster.id)
    getCabinetID.short_description = 'relatedCabinetID'
    getCabinetID.admin_order_field = 'cabinet_webmaster__id'

    def getBtnsImagesID(self, obj):
        return str(obj.btns_images.id)
    getBtnsImagesID.short_description = 'relatedBtnsImagesID'
    getBtnsImagesID.admin_order_field = 'btns_images__id'

class BtnsImageAdmin(admin.ModelAdmin):
    list_display=('id','name','path','type_image')
    list_filter=('name','type_image')
    search_fields=['id', 'type_image']

class AdvertBtnImageAdmin(admin.ModelAdmin):
    list_display=('id','name','path','bg_position','bg_position_med','bg_position_sml')
    list_filter=('bg_position','bg_position_med','bg_position_sml','name')
    search_fields=['id', 'name']

class SocialNetworksAdmin(admin.ModelAdmin):
    list_display=('id','shortcut','url','img_bd_pos','img_bd_pos_med','img_bd_pos_sml')
    list_filter=('shortcut','url')
    search_fields=['id', 'shortcut','url']

class AdvertAdmin(admin.ModelAdmin):
    list_display=('id','getCabinetID','getBtnConstructID','getBtnImageID','ad_type','ad_allow')
    list_filter=('ad_type','ad_allow')
    search_fields=['id', 'cabinet_webmaster__id','buttons_constructor__id','btn_images__id']

    def getCabinetID(self, obj):
        return str(obj.cabinet_webmaster.id)
    getCabinetID.short_description = 'relatedCabinetID'
    getCabinetID.admin_order_field = 'cabinet_webmaster__id'

    def getBtnConstructID(self, obj):
        if obj.buttons_constructor:
            return str(obj.buttons_constructor.id)
        else:
            return str('no constructor')
    getBtnConstructID.short_description = 'relatedBtnConstructID'
    getBtnConstructID.admin_order_field = 'buttons_constructor__id'

    def getBtnImageID(self, obj):
        return str(obj.btn_image.id)
    getBtnImageID.short_description = 'relatedBtnImageID'
    getBtnImageID.admin_order_field = 'btn_image__id'

admin.site.register(ButtonsConstructorModel, ButtonsConstructorModelAdmin)
admin.site.register(BtnsImages, BtnsImageAdmin)
admin.site.register(SocialNetworks, SocialNetworksAdmin)
admin.site.register(AdvertBtnImage, AdvertBtnImageAdmin)
admin.site.register(Advert, AdvertAdmin)
