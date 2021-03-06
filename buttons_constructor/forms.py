from buttons_constructor.models import ButtonsConstructorModel, BtnsImages
from django import forms

class ButtonsConstructorForm(forms.ModelForm):
    #name_constructor = forms.CharField(max_length=50)
    with_counter = forms.BooleanField(required=False)
    mobile_view = forms.BooleanField(required=False)
    with_background = forms.BooleanField(required=False)
    background_color = forms.CharField(required=False)

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
    form_buttons = forms.ChoiceField(choices=FORM_CHOICES, required=False)

    BIG = 'BIG'
    MEDIUM = 'MED'
    SMALL = 'SML'
    SIZE_CHOICES=(
        (BIG,'Большие'),
        (MEDIUM,'Средние'),
        (SMALL,'Маленькие'),
    )
    size_buttons = forms.ChoiceField(choices=SIZE_CHOICES, required=False)

    page_url = forms.URLField(required=False)
    page_title = forms.CharField(max_length=200, required=False)
    page_description = forms.CharField(widget=forms.Textarea, required=False)#initial

    def __init__(self, *args, **kwargs):
        super(ButtonsConstructorForm, self).__init__(*args, **kwargs)
        self.fields['btns_images'] = forms.ModelChoiceField(queryset=BtnsImages.objects.all())

    class Meta:
        model = ButtonsConstructorModel
        fields = ('btns_images', 'with_counter', 'mobile_view', 'with_background', 'background_color', 'size_buttons', 'social_networks', 'location_buttons', 'form_buttons', 'page_url', 'page_title', 'page_description')
