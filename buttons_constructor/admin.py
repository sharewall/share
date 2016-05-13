from django.contrib import admin
#from buttons_constructor.models import ButtonsConstructorModel, SocialNetworks
from buttons_constructor.models import SocialNetworks, BtnsImages, ButtonsConstructorModel, AdvertBtnImage, Advert

admin.site.register(ButtonsConstructorModel)
admin.site.register(BtnsImages)
admin.site.register(SocialNetworks)
admin.site.register(AdvertBtnImage)
admin.site.register(Advert)
