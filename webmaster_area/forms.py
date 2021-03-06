from webmaster_area.models import WebmasterAreaModel, AreaCategory
from buttons_constructor.models import ButtonsConstructorModel
from django import forms

class WebmasterAreaForm(forms.ModelForm):
    name_area = forms.CharField(max_length=200)
    url = forms.URLField()
    NORMAL = 'NORM'
    ADULT = 'ADUL'
    AD_TYPES_CHOICES=(
        (NORMAL,'Нормальный'),
        (ADULT,'Для взрослых'),
    )
    ad_type = forms.ChoiceField(choices=AD_TYPES_CHOICES, required=True, initial=NORMAL)
    area_cat_list = AreaCategory.objects.all()
    AREA_CAT_DEFAULT = ''
    for a in area_cat_list:
        if not a.name in AREA_CAT_DEFAULT:
            AREA_CAT_DEFAULT += a.name + ','
    AREA_CAT_DEFAULT = AREA_CAT_DEFAULT[:-1]
    area_category = forms.CharField(max_length=600, initial=AREA_CAT_DEFAULT)
    #def __init__(self, user, *args, **kwargs):
    def __init__(self, *args, **kwargs):
        super(WebmasterAreaForm, self).__init__(*args, **kwargs)
        #self.fields['buttons_constructor'] = ButtonsConstructorModel.objects.filter(cabinet_webmaster=user.cabinet_webmaster).order_by('-pk')[0]
    class Meta:
        model = WebmasterAreaModel
        fields = ('name_area', 'url', 'area_category', 'ad_type')
