from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from cabinet_webmaster.models import CabinetWebmasterModel, Chat, ChatMessage, ChatMessageFile, Balance

# start
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
# end

admin.actions.delete_selected.short_description = "Удалить"

class CabinetWebmasterModelAdmin(admin.ModelAdmin):
    list_display=('id','getUserID', 'wmr', 'mobile_phone', 'skype', 'money')
    search_fields=['id', 'user__id', 'wmr', 'mobile_phone', 'skype']

    def getUserID(self, obj):
        return str(obj.user.id)
    getUserID.short_description = 'relatedUserID'
    getUserID.admin_order_field = 'user__id'

class BalanceAdmin(admin.ModelAdmin):
    list_display=('id','getUserID', 'wmr', 'date_create','date_update', 'money')
    search_fields=['id', 'user__id', 'wmr', 'date_create', 'date_update']

    def getUserID(self, obj):
        return str(obj.user.id)
    getUserID.short_description = 'relatedUserID'
    getUserID.admin_order_field = 'user__id'

class ChatAdmin(admin.ModelAdmin):
    list_display=('id','getUserID', 'to_user_pk', 'date_create','date_update', 'header', 'department', 'status')
    list_filter=('department', 'status')
    search_fields=['id', 'user__id', 'to_user_pk', 'date_create', 'date_update', 'header']

    def getUserID(self, obj):
        return str(obj.user.id)
    getUserID.short_description = 'relatedUserID'
    getUserID.admin_order_field = 'user__id'

class ChatMessageAdmin(admin.ModelAdmin):
    list_display=('id','getUserID', 'getChatID', 'name','date_update', 'email', 'is_staff')
    search_fields=['id', 'user__id', 'chat__id', 'name', 'date_update', 'email']

    def getUserID(self, obj):
        return str(obj.user.id)
    getUserID.short_description = 'relatedUserID'
    getUserID.admin_order_field = 'user__id'

    def getChatID(self, obj):
        return str(obj.chat.id)
    getChatID.short_description = 'relatedChatID'
    getChatID.admin_order_field = 'chat__id'

class ChatMessageFileAdmin(admin.ModelAdmin):
    list_display=('id','getUserID', 'getChatMessageID', 'file_name', 'file_store')
    search_fields=['id', 'user__id', 'chat_message__id', 'file_name']

    def getUserID(self, obj):
        return str(obj.user.id)
    getUserID.short_description = 'relatedUserID'
    getUserID.admin_order_field = 'user__id'

    def getChatMessageID(self, obj):
        return str(obj.chat_message.id)
    getChatMessageID.short_description = 'relatedChatMessageID'
    getChatMessageID.admin_order_field = 'chat_message__id'

admin.site.register(CabinetWebmasterModel, CabinetWebmasterModelAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(ChatMessageFile, ChatMessageFileAdmin)
admin.site.register(Balance, BalanceAdmin)
