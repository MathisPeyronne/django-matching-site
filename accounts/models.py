from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



class non_member_user(models.Model): #added by a user
    username = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return str(self.username)


class Profile(models.Model):
    GENDER_CHOICES = {
        ('M', 'Male'),
        ('F', 'Female'),
    }
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    #attention friends goes from a profile to a user, so befriended is a user model attribut
    m_friends = models.ManyToManyField(User, related_name='befriended', symmetrical=False, blank=True) #member friends list
    nm_friends = models.ManyToManyField(non_member_user, related_name='befriended', symmetrical=False, blank=True)  #non member friends list
    # .matches gives a list of all conversations
    pending_messages = models.CharField(max_length=1000, blank=True, default="")
    
    class Meta:
        app_label='accounts'

        
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)






