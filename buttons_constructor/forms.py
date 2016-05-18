from buttons_constructor.models import ButtonsConstructorModel, BtnsImages
from django import forms

class ButtonsConstructorForm(forms.ModelForm):
    #name_constructor = forms.CharField(max_length=50)
    with_counter = forms.BooleanField(required=False)

    LOCATION_CHOICES=(
        ('HO', 'Horizontal'),
        ('VE', 'Vertical'),
    )
    location_buttons = forms.ChoiceField(choices=LOCATION_CHOICES, required=True)

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

    CIRCLE = 'CI'
    SQUARE = 'SQ'
    FORM_CHOICES=(
        (CIRCLE,'Circle'),
        (SQUARE,'Square'),
    )
    form_buttons = forms.ChoiceField(max_length=2, choices=FORM_CHOICES, default=CIRCLE)

    page_url = forms.URLField(required=False)
    page_title = forms.CharField(max_length=200, required=False)
    page_description = forms.CharField(widget=forms.Textarea, required=False)#initial

    def __init__(self, *args, **kwargs):
        super(ButtonsConstructorForm, self).__init__(*args, **kwargs)
        self.fields['btns_images'] = forms.ModelChoiceField(queryset=BtnsImages.objects.all())

    class Meta:
        model = ButtonsConstructorModel
        fields = ('btns_images', 'with_counter', 'social_networks', 'location_buttons', 'form_buttons', 'page_url', 'page_title', 'page_description')
