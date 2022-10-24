from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Value as V
from django.db.models.functions import Concat
from website.models import Post, MyUser
from users.models import Profile
from friends.models import FriendRequest
from website.forms import ReplyForm


def search_users(request):
    if request.method == "POST":
        search = request.POST['search']
        users_results = Profile.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')). \
            filter(full_name__icontains=search)
        context = {'search': search, 'users_results': users_results}
        return render(request, 'users/search_users.html', context)


@login_required(login_url='login')
def profile_settings(request):
    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your Profile has been updated!')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'p_form': profile_form}

    return render(request, 'users/profile_settings.html', context)


@login_required(login_url='login')
def users_profile(request, username):
    user_id = MyUser.objects.get(user_name=username).id
    profiles = Profile.objects.get(id=user_id)
    user_posts = len(Post.objects.filter(author=profiles.user))

    if profiles.mobile is None:
        profiles.mobile = "Unknown"
    elif profiles.mobile_visibility == "False":
        profiles.mobile = 'Hidden'

    if profiles.email_visibility == "False":
        profiles.user.email = 'Hidden'

    is_friend = False
    if request.user.friends.filter(user_name=profiles.user.user_name).exists():
        is_friend = True

    friend_request_sent = FriendRequest.objects.filter(request_from_user=request.user, request_to_user=user_id)
    friend_request_received = FriendRequest.objects.filter(request_from_user=user_id, request_to_user=request.user)

    friend_request_sent_exists = False
    friend_request_received_exists = False

    if friend_request_sent.exists():
        friend_request_sent_exists = True
    elif friend_request_received.exists():
        friend_request_received_exists = True

    context = {'user_posts': user_posts, 'profiles': profiles,
               'friend_request_sent_exists': friend_request_sent_exists,
               'friend_request_received_exists': friend_request_received_exists,
               'friend_request_received': friend_request_received,
               'friend_request_sent': friend_request_sent, 'is_friend': is_friend}
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def friend_request(request):
    show_friend_request = FriendRequest.objects.filter(request_to_user=request.user)

    context = {'show_friend_request': show_friend_request}

    return render(request, 'users/friend_request.html', context)


def friend_list(request, username):
    user_being_viewed = MyUser.objects.get(user_name=username)
    friends = user_being_viewed.friends.all().order_by('first_name')
    context = {'friends': friends, 'user_being_viewed': user_being_viewed}
    return render(request, 'users/friend_list.html', context)


def post_list(request, username):
    user_being_viewed = MyUser.objects.get(user_name=username)
    posts = Post.objects.filter(author=user_being_viewed).order_by('-post_date')
    get_id = request.POST.get("post_id")
    form_reply = ReplyForm(request.POST or None)

    if request.method == 'POST':
        if form_reply.is_valid():
            form_reply.instance.reply_author = MyUser.objects.get(id=request.user.id)
            form_reply.instance.post = Post.objects.get(id=get_id)
            form_reply.save()
            return redirect(request.META['HTTP_REFERER'])
    context = {'posts': posts, 'user_being_viewed': user_being_viewed}

    return render(request, 'users/post_list.html', context)
