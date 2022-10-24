from django.contrib.auth.decorators import login_required
from friends.models import FriendRequest
from website.models import MyUser
from django.shortcuts import redirect


def send_friend_request(request, id):
    from_user = request.user
    to_user = MyUser.objects.get(id=id)
    if to_user in request.user.friends.all():
        pass
    else:
        friend_request, created = FriendRequest.objects.get_or_create(request_from_user=from_user,
                                                                      request_to_user=to_user)

    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def decline_friend_request(request, id):
    friend_request = FriendRequest.objects.get(id=id)
    friend_request.delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def cancel_friend_request(request, id):
    friend_request = FriendRequest.objects.get(id=id)
    friend_request.delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def accept_friend_request(request, id):
    friend_request = FriendRequest.objects.get(id=id)
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
    second_user = MyUser.objects.get(id=id)
    if request.method == "POST":
        current_user.friends.remove(second_user)
        second_user.friends.remove(current_user)

    return redirect(request.META['HTTP_REFERER'])


