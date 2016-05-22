from django.db import models
from cabinet_webmaster.models import CabinetWebmasterModel
from django.contrib.auth.models import User

class BtnsImages(models.Model):
    name = models.CharField('name image', max_length=200)
    path = models.CharField('path to image', max_length=200)

    CIRCLE = 'CI'
    SQUARE = 'SQ'
    TYPES_IMAGES=(
        (CIRCLE,'Circle'),
        (SQUARE,'Square'),
    )

    type_image = models.CharField(max_length=2, choices=TYPES_IMAGES, default=CIRCLE)
    db_table = 'BtnsImages'

    def __str__(self):
        return str('Name: %s' % self.name + ' type: %s' % self.type_image)

class AdvertBtnImage(models.Model):
    name = models.CharField('name image', max_length=100)
    path = models.CharField('path to image', max_length=200)
    bg_position = models.CharField('background position big', max_length=100, default='background-position: -370px 0px;')
    bg_position_med = models.CharField('background position medium', max_length=100, default='background-position: -280px 0px;')
    bg_position_sml = models.CharField('background position small', max_length=100, default='background-position: -190px 0px;')

    def __str__(self):
        return str('Name: %s' % self.name)

class Advert(models.Model):
    cabinet_webmaster = models.ForeignKey(CabinetWebmasterModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="related cabinet webmaster", related_name="advert")
    buttons_constructor = models.OneToOneField('ButtonsConstructorModel', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="related buttons constructor", related_name="advert")
    btn_image = models.ForeignKey('AdvertBtnImage', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="related advert btn image", related_name="advert")

    BUY = 'BUY' # Show btn and wait click event
    SHOW = 'SHO' # Hide btn, auto show advert after delay(fix value)
    AD_TYPE_CHOICES=(
        (BUY,'Купить'),
        (SHOW,'Выходящая реклама'),
    )
    ad_type = models.CharField(max_length=3, choices=AD_TYPE_CHOICES, default=SHOW)

    TIZER_1 = 'TI1'
    TIZER_2 = 'TI2'
    TIZER_3 = 'TI3'
    MEDIA_1 = 'ME1'
    MEDIA_2 = 'ME2'
    MEDIA_3 = 'ME3'
    AD_ALLOW_CHOICES=(
        (TIZER_1,'1 Блок'),
        (TIZER_2,'2 Блока'),
        (TIZER_3,'3 Блока'),
        (MEDIA_1,'240x400'),
        (MEDIA_2,'728x90'),
        (MEDIA_3,'300x250'),
    )
    ad_allow = models.CharField(max_length=3, choices=AD_ALLOW_CHOICES, default=MEDIA_1)

    show_counter = models.IntegerField('show counter', default=0)
    click_counter = models.IntegerField('click counter', default=0)

    def __str__(self):
        return str('PK: %s' % self.pk)

class SocialNetworks(models.Model):
    shortcut = models.CharField('shortcut for network', max_length=2)
    url = models.URLField('url for network', null=False, blank=False, default='')
    img_bd_pos = models.CharField('img background position big', max_length=400, default='background-position: 0px 0px;')
    img_bd_pos_med = models.CharField('img background position med', max_length=400, default='background-position: 0px 0px;')
    img_bd_pos_sml = models.CharField('img background position sml', max_length=400, default='background-position: 0px 0px;')

    db_table = 'SocialNetworks'

    def __str__(self):
        return str('shortcut: %s' % self.shortcut + ' url: %s' % self.url)

class ButtonsConstructorModel(models.Model):
    cabinet_webmaster = models.ForeignKey(CabinetWebmasterModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name="related cabinet webmaster", related_name="buttons_constructor")
    btns_images = models.ForeignKey(BtnsImages, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="related btns images", related_name="buttons_constructor")
    name_constructor = models.CharField("name_constructor", max_length=50, default="Default constructor")

    sn_list = SocialNetworks.objects.all()
    SOCIAL_DEFAULT = ''

    for s in sn_list:
        if not s.shortcut in SOCIAL_DEFAULT:
            SOCIAL_DEFAULT += s.shortcut + ','
    SOCIAL_DEFAULT = SOCIAL_DEFAULT[:-1]

    social_networks = models.CharField(max_length=300, default=SOCIAL_DEFAULT)

    with_counter = models.BooleanField(default=True)
    mobile_view = models.BooleanField(default=False)
    with_background = models.BooleanField(default=False)
    background_color = models.TextField(default='rgb(255, 255, 255)')

    CIRCLE = 'CI'
    SQUARE = 'SQ'
    FORM_CHOICES=(
        (CIRCLE,'Circle'),
        (SQUARE,'Square'),
    )
    form_buttons = models.CharField(max_length=2, choices=FORM_CHOICES, default=CIRCLE)

    HORIZONTAL = 'HO'
    VERTICAL = 'VE'
    LOCATION_CHOICES=(
        (HORIZONTAL,'Horizontal'),
        (VERTICAL,'Vertical'),
    )
    location_buttons = models.CharField(max_length=2, choices=LOCATION_CHOICES, default=HORIZONTAL)

    BIG = 'BIG'
    MEDIUM = 'MED'
    SMALL = 'SML'
    SIZE_CHOICES=(
        (BIG,'Big'),
        (MEDIUM,'Medium'),
        (SMALL,'Small'),
    )
    size_buttons = models.CharField(max_length=3, choices=SIZE_CHOICES, default=BIG)

    page_url = models.URLField(blank=True, default='')
    page_title = models.CharField(blank=True, max_length=200, default='')
    page_description = models.TextField(blank=True, default='')

    db_table = 'ButtonsConstructorModel'

    def __str__(self):
        return str(self.name_constructor + " <<== %s" % self.cabinet_webmaster)
