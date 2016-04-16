#import uuid
from django.db import models
from cabinet_webmaster.models import CabinetWebmasterModel

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

class SocialNetworks(models.Model):
    shortcut = models.CharField('shortcut for network', max_length=2)
    url = models.URLField('url for network', null=False, blank=False, default='')
    img_bd_pos = models.CharField('img background position', max_length=400)
    db_table = 'SocialNetworks'

    def __str__(self):
        return str('shortcut: %s' % self.shortcut + ' url: %s' % self.url)

class ButtonsConstructorModel(models.Model):
    cabinet_webmaster = models.ForeignKey(CabinetWebmasterModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name="related cabinet webmaster", related_name="buttons_constructor")
    btns_images = models.ForeignKey(BtnsImages, on_delete=models.CASCADE, null=True, blank=True, verbose_name="related btns images", related_name="buttons_constructor")
    name_constructor = models.CharField("name_constructor", max_length=50, default="Default constructor")
    sn_list = SocialNetworks.objects.all()
    SOCIAL_DEFAULT = ''
    for s in sn_list:
        if not s.shortcut in SOCIAL_DEFAULT:
            SOCIAL_DEFAULT += s.shortcut + ','
    SOCIAL_DEFAULT = SOCIAL_DEFAULT[:-1]
    social_networks = models.CharField(max_length=300, default=SOCIAL_DEFAULT)
    with_counter = models.BooleanField(default=True)
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
    size_buttons = models.CharField(max_length=3, choices=SIZE_CHOICES, default=MEDIUM)
    mobile_view = models.BooleanField(default=False)
    with_background = models.BooleanField(default=False)
    background_color = models.TextField(default='rgb(255, 255, 255)')
    page_url = models.URLField(blank=True, default='')
    page_title = models.CharField(blank=True, max_length=200, default='')
    page_description = models.TextField(blank=True, default='')
    db_table = 'ButtonsConstructorModel'

    def __str__(self):
        return str(self.name_constructor + " <<== %s" % self.cabinet_webmaster)
