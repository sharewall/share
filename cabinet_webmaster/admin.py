from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from cabinet_webmaster.models import CabinetWebmasterModel, Chat, ChatMessage, ChatMessageFile, Balance

# Define an inline admin descriptor for CabinetWebmasterModel model
# which acts a bit like a singleton
class CabinetWebmasterModelInline(admin.StackedInline):
    model = CabinetWebmasterModel
    can_delete = False
    verbose_name_plural = 'cabinet webmaster'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (CabinetWebmasterModelInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(CabinetWebmasterModel)
admin.site.register(Chat)
admin.site.register(ChatMessage)
admin.site.register(ChatMessageFile)
admin.site.register(Balance)
