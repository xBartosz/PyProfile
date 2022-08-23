from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from friends.models import Friend_Request
from website.models import MyUser
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect

# Create your views here.



def send_friend_request(request, id):
    #from logged user to user that i will send id
    from_user = request.user
    to_user = MyUser.objects.get(id=id)
    friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)


    # return redirect('index')
    return HttpResponseRedirect('/profile/%d'%id)

@login_required(login_url='login')
def decline_friend_request(request, id):
    friend_request = Friend_Request.objects.get(id=id)
    friend_request.delete()
    return redirect('friend_request')

@login_required(login_url='login')
def cancel_friend_request(request, id):
    profile_id = request.POST.get("profile_id")
    friend_request = Friend_Request.objects.get(id=id)
    friend_request.delete()
    return HttpResponseRedirect('/profile/%d'%int(profile_id))

@login_required(login_url='login')
def accept_friend_request(request, id):
    friend_request = Friend_Request.objects.get(id=id)
    from_user = MyUser.objects.get(email=friend_request.from_user)
    to_user = MyUser.objects.get(email=friend_request.to_user)
    if request.user == friend_request.to_user:
        to_user.friends.add(friend_request.from_user)
        from_user.friends.add(friend_request.to_user)
        # FriendList.add(friend_request.to_user, friend_request.from_user)
        # FriendList.friends.add(user=friend_request.from_user, friends=friend_request.to_user)
        # friend_request.to_user.add(friend_request.from_user)
        # friend_request.from_user.add(friend_request.to_user)
        friend_request.delete()
    return redirect('friend_request')

@login_required(login_url='login')
def delete_friend(request, id):
    current_user = MyUser.objects.get(email=request.user)
    #profil uzytkownika i z niego wyslac id
    # second_user_id = request.POST.get("second_user_id")
    second_user = MyUser.objects.get(id=id)
    if request.method == "POST":
        current_user.friends.remove(second_user)
        second_user.friends.remove(current_user)

    return HttpResponseRedirect('/profile/%d' % int(id))



# def accept_friend_request(request, id):
    #when to_user == request_user
