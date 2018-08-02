from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import FriendsEditForm, MessageForm
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import non_member_user
from .models import Conversation



@login_required
def matches(request):     #matches, list of convs
    #request.user.conversations.all
    pending_messages = request.user.profile.pending_messages
    if pending_messages != "":
        messages.success(request, pending_messages)
        pending_messages = ""
        request.user.profile.pending_messages = pending_messages
        request.user.profile.save()
    
    friends= {}
    username = request.user.username
    for conversation in request.user.conversations.all():
        friend = conversation.participants.exclude(username=username)[0]
        friends[friend] = conversation.messages.filter(read=False).filter(user_to=request.user).count()
    return render(request, 'dashboard/matches.html', {'section': 'matches', 'friends': friends})


@login_required
def profile(request): 
    user = request.user
    return render(request, 'dashboard/profile.html', {'section': 'profile', 'user': user})

@login_required
def friends(request):
    if request.method == 'POST':  #add friend
        friends_form = FriendsEditForm(data=request.POST,
                                       files=request.FILES)
        if friends_form.is_valid():
            cd = friends_form.cleaned_data
            if request.user.profile.m_friends.count() + request.user.profile.nm_friends.count() < 10: # ca fera max 10 car on ajoute apres
                try:
                    #member friend
                    friend_to_add = User.objects.filter(username=cd['friend'])[0]  #if this fails it means that it is a nm_friend
                    request.user.profile.m_friends.add(friend_to_add) 
                    try:
                        if request.user.befriended.filter(user__username = cd['friend']).exists():
                            # les ajouter chaqu'un dans la list des matches de l'autre
                            conversation = Conversation()
                            conversation.save()
                            conversation.participants.set([request.user, friend_to_add])
                            pending_messages = friend_to_add.profile.pending_messages
                            if pending_messages != "":
                                pending_messages += ", "
                            pending_messages += (request.user.get_full_name() + " like you too ! go in the matches menu")
                            friend_to_add.profile.pending_messages = pending_messages
                            friend_to_add.profile.save()
                            """

                                ADD instagram DM sending here

                            """
                            messages.success(request, friend_to_add.get_full_name() + " likes you too ! go in the matches menu")
                        else:
                            messages.success(request, cd['friend'] + ' has been added')
                    except Exception as e:
                        messages.error(request, e)    
                        print(e)
                except:
                    #non-member friend
                    nm_user = non_member_user.objects.filter(username=cd['friend'])  #attention list
                    if not nm_user.exists():
                        #existe pas encore
                        request.user.profile.nm_friends.create(username=cd['friend'])  #crée un nm_user si pas de user
                        messages.success(request, cd['friend'] + ' has been added' )
                    else:
                        #exist deja
                        request.user.profile.nm_friends.add(nm_user[0])
                        messages.success(request, "il existait deja")    
            else:
                messages.info(request, 'you cannot add more than 10 friends')
        else:
            messages.error(request, 'Error adding your friend')

        #friends_form = FriendsEditForm(instance=request.user.profile)
    m_friends = request.user.profile.m_friends.all() 
    nm_friends = request.user.profile.nm_friends.all()
    friends_form = FriendsEditForm()
    return render(request, 'dashboard/friends.html', {'section': 'friends',
        'friends_form': friends_form,'m_friends': m_friends,'nm_friends': nm_friends})

@login_required
def chat(request, username):
    if request.method=='POST':
        message_form = MessageForm(request.POST)          
        if message_form.is_valid():
            #conversation = Conversation.objects.filter(participants=request.user).get(participants = receiver)
            cd = message_form.cleaned_data
            receiver = User.objects.filter(username=username)[0]
            conversation = Conversation.objects.filter(participants=request.user).get(participants = receiver)            
            conversation.messages.create(user_from= request.user, user_to= receiver, content=cd['message'])
            messages.success(request, 'your message has been sent')
            return HttpResponseRedirect("/chat/" + username + "/#bottom")
        else:
            messages.error(request, 'Error sending this message')
    message_form = MessageForm()
    receiver = User.objects.get(username = username)
    #conversation = request.user.filter(conversation__participants=user).filter(participants=receiver)[0]
    conversation = Conversation.objects.filter(participants=request.user).get(participants = receiver)
    un_reads = conversation.messages.filter(read=False).filter(user_to=request.user)
    for un_read in un_reads:
        un_read.read = True
        un_read.save()
    return render(request, 'dashboard/chat.html', {'section': 'matches', 'receiver': receiver, 'message_form': message_form, 'conversation': conversation})



