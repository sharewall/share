# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1n$$^)=jkjba*#g!!ps9e0(_+6og37u@+r#(=ul3)ogy9$h%pv'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'share_db',
        'USER': 'freeman',
        'PASSWORD': 'my3777',
        'HOST': '37.1.207.26',
    }
}
ALLOWED_HOSTS = ['127.0.0.1',]
