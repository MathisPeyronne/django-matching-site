from django.contrib import admin
from .models import Message, Conversation

class MessageAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'content']

class ConversationAdmin(admin.ModelAdmin):
     model= Conversation
     filter_horizontal = ('participants',) #If you don't specify this, you will get a multiple select widget.

admin.site.register(Message, MessageAdmin)
admin.site.register(Conversation, ConversationAdmin)



