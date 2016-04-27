import uuid
from django.db import models
from django.contrib.auth.models import User

def generate_filename(self, filename):
    path = "%s/%s" % ( str(self.user.pk), str(uuid.uuid4()) + '-' + filename )
    return path

class CabinetWebmasterModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="related user", related_name="cabinet_webmaster")
    wmr = models.CharField("wmr", max_length=100, null=True, blank=True, default="")
    mobile_phone = models.CharField("mobile phone", max_length=200, blank=True, default="")
    skype = models.CharField("skype", max_length=200, blank=True, default="")
    money = models.FloatField("money in rub", default=0.0)
    db_table = 'CabinetWebmasterModel'

    def __str__(self):
        return str("user.name: %s" % self.user.username + " , user.email: %s" % self.user.email)

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="related_user", related_name="chat")
    #to_user_pk = models.IntegerField('to_user_pk', blank=True, null=True)
    header = models.CharField('message_header', max_length=100, blank=True, default='')
    text = models.TextField('message_text', default='')
    date_create = models.DateTimeField('date_create', auto_now_add=True)#DateField
    date_update = models.DateTimeField('date_update', auto_now=True)

    def showCreateDate(self):
        return str(self.date_create.strftime('%d.%m.%Y %H:%M'))

    def showUpdateDate(self):
        return str(self.date_update.strftime('%d.%m.%Y %H:%M'))

    BILLING = 'BIL'
    SUPPORT = 'SUP'
    DEPARTMENT_CHOICES=(
        (BILLING,'Billing'),
        (SUPPORT,'Support'),
    )
    department = models.CharField(max_length=3, choices=DEPARTMENT_CHOICES, default=BILLING)
    
    CLOSE = 'CLO'
    ACTIVE = 'ACT'
    ANSWERED = 'ANS'
    STATUS_CHOICES=(
        (CLOSE,'CLOSE'),
        (ACTIVE,'ACTIVE'),
        (ANSWERED,'ANSWERED'),
    )
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=ACTIVE)

    def showDepartment(self):
        return str('Служба поддержки' if self.department == self.SUPPORT else 'Биллинг')

    def showStatus(self):
        if self.status == self.CLOSE:
            return 'Закрыт'
        elif self.status == self.ACTIVE:
            return 'В процессе'
        else:
            return 'Отвечен'

    def __str__(self):
        return str('From: %s' % self.user.username + '; Header: %s' % self.header + '; Status: %s' % self.status + '; Date_update: %s ' % self.date_update.strftime('%d/%m/%Y %H:%M'))

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="related_user", related_name="chat_message")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name="related_chat", related_name="chat_message")
    name = models.CharField('from_name', max_length=100, blank=True, default='')
    text = models.TextField('message_text', default='')
    is_staff = models.BooleanField('is_staff', editable=False, default=False)
    date_update = models.DateTimeField('date_update', auto_now=True)

    def save(self, *args, **kwargs):
        self.is_staff = self.user.is_staff 
        self.chat.save()
        super(ChatMessage, self).save(*args, **kwargs)

    def __str__(self):
        return str('Chat: %s' % self.chat + ' ---- From_name: %s' % self.name + '; Is_staff: %s ' % self.is_staff + '; Date_update: %s ' % self.date_update.strftime('%d/%m/%Y %H:%M'))

class ChatMessageFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="related_user", related_name="chat_message_file")
    chat_message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, verbose_name="related_chat_message", related_name="chat_message_file")
    file_store = models.FileField(upload_to=generate_filename)
    
    def __str__(self):
        return str('Chat_message: %s' % self.chat_message + '; File_store: %s ' % self.file_store)
