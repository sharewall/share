from urllib.parse import urlparse
from django.db import models
from buttons_constructor.models import SocialNetworks, ButtonsConstructorModel
#ButtonsConstructorModel, SocialNetworks

class WebmasterAreaModel(models.Model):
    buttons_constructor = models.ForeignKey(ButtonsConstructorModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='related_buttons_constructor', related_name='webmaster_area')
    name_area = models.CharField(max_length=200, default='name area', verbose_name='name area')
    url = models.URLField('url', null=False, blank=False, default='')

    #date(2005, 7, 27)
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
    today_social_counter = models.CharField("today social counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    total_social_counter = models.CharField("total social counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    today_share_counter = models.CharField("today share counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
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
        
class PageDetail(models.Model):
    webmaster_area = models.ForeignKey(WebmasterAreaModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='related webmaster_area', related_name='page_detail')
    title = models.CharField(max_length=300, default='', verbose_name='page title')
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
    today_social_counter = models.CharField("today social counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    total_social_counter = models.CharField("total social counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    today_share_counter = models.CharField("today share counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    total_share_counter = models.CharField("total share counter(%s)"%SOCIAL_DEFAULT, max_length=300, default=COUNTER_DEFAULT)
    db_table = 'PageDetail'

    def __str__(self):
        return str(self.title + ' - ') + self.url
