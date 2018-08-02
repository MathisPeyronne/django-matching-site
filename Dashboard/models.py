from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import Profile

#this is for the messaging system

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name= 'conversations')
    created = models.DateField(auto_now_add=True, db_index=True)



class Message(models.Model):
    conversation = models.ForeignKey(Conversation,related_name='messages', on_delete=models.CASCADE, default=1)
    user_from = models.ForeignKey(User,related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    content = models.CharField(max_length=150, blank=False, null=False, default='empty message')
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta:
        ordering = ('-created',)


    def __str__(self):
        return '{} sent a message to {}'.format(self.user_from, self.user_to)




