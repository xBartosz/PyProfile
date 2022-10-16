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
    if to_user in request.user.friends.all():
        pass
    else:
        friend_request, created = Friend_Request.objects.get_or_create(request_from_user=from_user, request_to_user=to_user)
    # profile_username = to_user.user_name

    # return HttpResponseRedirect('/profile/%s'%profile_username)
    return redirect(request.META['HTTP_REFERER'])
@login_required(login_url='login')
def decline_friend_request(request, id):
    friend_request = Friend_Request.objects.get(id=id)
    friend_request.delete()
    # return redirect('friend_request')
    return redirect(request.META['HTTP_REFERER'])
@login_required(login_url='login')
def cancel_friend_request(request, id):
    # profile_username = request.POST.get("profile_username")
    friend_request = Friend_Request.objects.get(id=id)
    friend_request.delete()
    # return HttpResponseRedirect('/profile/%s'%profile_username)
    return redirect(request.META['HTTP_REFERER'])
@login_required(login_url='login')
def accept_friend_request(request, id):
    friend_request = Friend_Request.objects.get(id=id)
    from_user = MyUser.objects.get(email=friend_request.request_from_user)
    to_user = MyUser.objects.get(email=friend_request.request_to_user)
    if request.user == friend_request.request_to_user:
        to_user.friends.add(friend_request.request_from_user)
        from_user.friends.add(friend_request.request_to_user)
        friend_request.delete()
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def delete_friend(request, id):
    current_user = MyUser.objects.get(email=request.user)
    #profil uzytkownika i z niego wyslac id
    # second_user_id = request.POST.get("second_user_id")
    second_user = MyUser.objects.get(id=id)
    if request.method == "POST":
        current_user.friends.remove(second_user)
        second_user.friends.remove(current_user)

    # return HttpResponseRedirect('/profile/%s' % second_user.user_name)
    return redirect(request.META['HTTP_REFERER'])



# def accept_friend_request(request, id):
    #when to_user == request_user
