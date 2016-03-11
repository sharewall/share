from webmaster_area.models import WebmasterAreaModel
from buttons_constructor.models import ButtonsConstructorModel
from django import forms

class WebmasterAreaForm(forms.ModelForm):
    name_area = forms.CharField(max_length=200)
    url = forms.URLField()
    def __init__(self, user, *args, **kwargs):
        super(WebmasterAreaForm, self).__init__(*args, **kwargs)
        self.fields['buttons_constructor'] = forms.ModelChoiceField(queryset=ButtonsConstructorModel.objects.filter(cabinet_webmaster=user.cabinet_webmaster))
    class Meta:
        model = WebmasterAreaModel
        fields = ('buttons_constructor', 'name_area', 'url')
