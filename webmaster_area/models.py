from urllib.parse import urlparse
from django.db import models
from buttons_constructor.models import ButtonsConstructorModel, SocialNetworks
from cabinet_webmaster.models import CabinetWebmasterModel

class Faq(models.Model):
    header = models.CharField("header", max_length=200, null=False, blank=False, default=" ")
    text = models.TextField("text", blank=True, default=" ")

class AreaCategory(models.Model):
    name = models.CharField("name", max_length=200)
    db_table = "AreaCategory"

    def __str__(self):
        return str("Category name: %s" % self.name)

class WebmasterAreaModel(models.Model):
    buttons_constructor = models.ForeignKey(ButtonsConstructorModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='related_buttons_constructor', related_name='webmaster_area')

    name_area = models.CharField(max_length=200, default='name area', verbose_name='name area')
    url = models.URLField('url', null=False, blank=False, default='')

    NORMAL = 'NORM'
    ADULT = 'ADUL'
    AD_TYPES_CHOICES=(
        (NORMAL,'Нормальный'),
        (ADULT,'Для взрослых'),
    )
    ad_type = models.CharField("ad_type", max_length=4, choices=AD_TYPES_CHOICES, default=NORMAL)

    area_cat_list = AreaCategory.objects.all()
    AREA_CAT_DEFAULT = ''
    for a in area_cat_list:
        if not a.name in AREA_CAT_DEFAULT:
            AREA_CAT_DEFAULT += a.name + ','
    AREA_CAT_DEFAULT = AREA_CAT_DEFAULT[:-1]
    area_category = models.CharField('area_category', max_length=600, default=AREA_CAT_DEFAULT)

    sn_list = SocialNetworks.objects.all()
    SOCIAL_DEFAULT = ''
    COUNTER_DEFAULT = ''
    for s in sn_list:
        if not s.shortcut in SOCIAL_DEFAULT:
            SOCIAL_DEFAULT += s.shortcut + ','
            COUNTER_DEFAULT += '0,'
    SOCIAL_DEFAULT = SOCIAL_DEFAULT[:-1]
    COUNTER_DEFAULT = COUNTER_DEFAULT[:-1]

    total_social_counter = models.CharField("total social counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    total_share_counter = models.CharField("total share counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)

    db_table = 'WebmasterAreaModel'
    
    def __str__(self):
        return str("Area name: %s" % self.name_area + ", area url: %s" % self.url + " <<== %s" % self.buttons_constructor)

    #TODO:log to log_table
    def save(self, *args, **kwargs):
        if 'http' not in self.url:
            self.url = 'http://'+self.url
        host = urlparse(self.url)
        if not host.netloc:
            return
        self.url = host.netloc
        super(WebmasterAreaModel, self).save(*args, **kwargs)
        
class AreaToday(models.Model):
    webmaster_area = models.ForeignKey(WebmasterAreaModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='related_webmaster_area', related_name='area_today')

    date = models.DateField('date', auto_now_add=True)

    sn_list = SocialNetworks.objects.all()

    SOCIAL_DEFAULT = ''
    COUNTER_DEFAULT = ''
    for s in sn_list:
        if not s.shortcut in SOCIAL_DEFAULT:
            SOCIAL_DEFAULT += s.shortcut + ','
            COUNTER_DEFAULT += '0,'
    SOCIAL_DEFAULT = SOCIAL_DEFAULT[:-1]
    COUNTER_DEFAULT = COUNTER_DEFAULT[:-1]

    today_share_counter = models.CharField("today share counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    today_social_counter = models.CharField("today social counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    # Adv
    today_show_counter = models.IntegerField('today show counter', default=0)
    today_click_counter = models.IntegerField('today click counter', default=0)
    today_money = models.FloatField("today money in rub", default=0.0)
    
    db_table = 'AreaToday'
    
    def __str__(self):
        if self.webmaster_area:
            return str('Date: %s ' % self.date.strftime('%d/%m/%Y') + '; <<== %s' % self.webmaster_area)
        else:
            return str("Without webmaster_area")

class PageDetail(models.Model):
    webmaster_area = models.ForeignKey(WebmasterAreaModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='related webmaster_area', related_name='page_detail')

    title = models.CharField(max_length=512, default='', verbose_name='page title')
    url = models.URLField('page url', null=False, blank=False, default='')

    sn_list = SocialNetworks.objects.all()

    SOCIAL_DEFAULT = ''
    COUNTER_DEFAULT = ''

    for s in sn_list:
        if not s.shortcut in SOCIAL_DEFAULT:
            SOCIAL_DEFAULT += s.shortcut + ','
            COUNTER_DEFAULT += '0,'

    SOCIAL_DEFAULT = SOCIAL_DEFAULT[:-1]
    COUNTER_DEFAULT = COUNTER_DEFAULT[:-1]

    total_social_counter = models.CharField("total social counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    total_share_counter = models.CharField("total share counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)

    db_table = 'PageDetail'

    def __str__(self):
        return str(self.title + ' - ') + self.url

class PageToday(models.Model):
    page_detail = models.ForeignKey(PageDetail, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='related_page_detail', related_name='page_today')

    date = models.DateField('date', auto_now_add=True)

    sn_list = SocialNetworks.objects.all()
    SOCIAL_DEFAULT = ''
    COUNTER_DEFAULT = ''
    for s in sn_list:
        if not s.shortcut in SOCIAL_DEFAULT:
            SOCIAL_DEFAULT += s.shortcut + ','
            COUNTER_DEFAULT += '0,'
    SOCIAL_DEFAULT = SOCIAL_DEFAULT[:-1]
    COUNTER_DEFAULT = COUNTER_DEFAULT[:-1]

    today_share_counter = models.CharField("today share counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    today_social_counter = models.CharField("today social counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    # Adv
    today_show_counter = models.IntegerField('today show counter', default=0)
    today_click_counter = models.IntegerField('today click counter', default=0)
    today_money = models.FloatField("today money in rub", default=0.0)

    # Default
    default_today_share_counter = models.CharField("default today share counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    default_today_social_counter = models.CharField("default today social counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    # Adv
    default_today_show_counter = models.IntegerField('default today show counter', default=0)
    default_today_click_counter = models.IntegerField('default today click counter', default=0)
    default_today_money = models.FloatField("default today money in rub", default=0.0)

    def getOddShare(self):
        r = ''

        for i1, i2 in zip(self.today_share_counter.split(','), self.default_today_share_counter.split(',')):
            if int(i1)-int(i2) < 0:
                r += str(0) + ','

            else:
                r += str(int(i1)-int(i2)) + ','
            #r += str(int(i1)-int(i2)) + ','

        r = r[:-1]
        return str(r)

    getOddShare.allow_tags = True

    def getOddSocial(self):
        r = ''

        for i1, i2 in zip(self.today_social_counter.split(','), self.default_today_social_counter.split(',')):
            if int(i1)-int(i2) < 0:
                r += str(0) + ','

            else:
                r += str(int(i1)-int(i2)) + ','
            #r += str(int(i1)-int(i2)) + ','

        r = r[:-1]
        return str(r)

    getOddSocial.allow_tags = True

    db_table = 'PageToday'
    
    def __str__(self):
        return str("PageToday <- Page detail: %s" % self.page_detail)
