from urllib.parse import urlparse
from django.db import models
from buttons_constructor.models import ButtonsConstructorModel, SocialNetworks

class WebmasterAreaModel(models.Model):
    buttons_constructor = models.ForeignKey(ButtonsConstructorModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='related buttons_constructor', related_name='webmaster_area')
    name_area = models.CharField(max_length=200, default='name area', verbose_name='name area')
    url = models.URLField('url', default='')
    #date(2005, 7, 27)
    date = models.DateField('date', auto_now_add=True)
    share_today_counter = models.IntegerField('share today counter', default=0)
    share_total_counter = models.IntegerField('share total counter', default=0)
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
    url = models.URLField('page url', default='')
    page_share_counter = models.IntegerField('page share counter', default=0)
    page_social_traffic = models.IntegerField('page social network traffic counter', default=0)

    db_table = 'PageDetail'

    def __str__(self):
        return str(self.title + ' - ') + self.url

