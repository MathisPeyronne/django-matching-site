from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, non_member_user
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

#for the user login form
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Authenticated successfully')
                    return HttpResponseRedirect('/') 
                else:
                    messages.warning(request, 'Disabled account')
                    return HttpResponseRedirect('/accounts/register/')            
            else:
                messages.error(request, 'Invalid login')
                return HttpResponseRedirect('/accounts/login/')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

#for the user register form
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = Profile.objects.create(user=new_user)
            # ajouter ca list de befriended si il a un nm account
            nm_account = non_member_user.objects.filter(username = new_user.username) #attention list
            if nm_account.exists():
                #faire le transfet
                nm_account = nm_account[0] #c'était une list avant
                for befriended in nm_account.befriended.all(): #la variable befriended est un profile
                    #on ajoute les befriended du nm compte au nouveau compte
                    profile.user.befriended.add(befriended) #donc on ajoute de profile a befriended
                nm_account.delete() #on delete le vieux compte
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return HttpResponseRedirect("/profile/")
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})

@login_required
def delete_friend(request, username):
    try:
        user_to_delete = User.objects.filter(username = username)[0]
        request.user.profile.m_friends.remove(user_to_delete)
        messages.success(request, username + ' successfully removed')
    except:
        user_to_delete = request.user.profile.nm_friends.filter(username = username)[0]
        request.user.profile.nm_friends.remove(user_to_delete)
        messages.success(request, username + ' successfully removed')        

    return HttpResponseRedirect("/friends/")

def delete_account(request):
    try:
        u = request.user
        u.delete()
        messages.success(request, "The user is deleted") 
    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")    
        return render(request, 'Dashboard.html')
    except Exception as e: 
        return render(request, 'Dashboard.html',{'err':e.message})

    return HttpResponseRedirect("/")
