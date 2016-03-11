from buttons_constructor.models import ButtonsConstructorModel
from django import forms

class ButtonsConstructorForm(forms.ModelForm):
    name_constructor = forms.CharField(max_length=50)
    with_counter = forms.BooleanField(required=False)
    LOCATION_CHOICES=(
        ('HO', 'Horizontal'),
        ('VE', 'Vertical'),
    )
    SOCIAL_NETWORKS_CHOICES = (
        ('vk','vkontakte'),
        ('fb','facebook'),
        ('tw','twitter'),
        ('od','odnoklassniki'),
        ('gp','google plus'),
        ('ma','mail'),
        ('li','linkedin'),
        ('lj','livejournal'),
    )
    social_networks = forms.MultipleChoiceField(choices=SOCIAL_NETWORKS_CHOICES, widget=forms.CheckboxSelectMultiple())
    location_buttons = forms.ChoiceField(choices=LOCATION_CHOICES, required=True)
    page_url = forms.URLField(required=False)
    page_title = forms.CharField(max_length=200, required=False)
    page_description = forms.CharField(widget=forms.Textarea, required=False)#initial
    class Meta:
        model = ButtonsConstructorModel
        fields = ('name_constructor', 'with_counter', 'social_networks', 'location_buttons', 'page_url', 'page_title', 'page_description')
