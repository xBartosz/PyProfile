from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Value as V
from django.db.models.functions import Concat
from website.models import Post, MyUser
from users.models import Profile
from friends.models import Friend_Request
from website.forms import ReplyForm

def search_users(request):
    if request.method == "POST":
        search = request.POST['search'] #input type from template
        users_results = Profile.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).\
                filter(full_name__icontains=search)
        context = {'search' : search, 'users_results' : users_results}
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

    context = {'p_form' : profile_form}

    return render(request, 'users/profile_settings.html', context)

@login_required(login_url='login')
def users_profile(request, user_id):
    get_id = request.POST.get("post_id")
    profiles = Profile.objects.get(id=user_id)
    user_posts = Post.objects.filter(author=profiles.user).order_by('-post_date')
    form_reply = ReplyForm(request.POST or None)


    is_friend = False
    if request.user.friends.filter(email = profiles.user.email).exists():
        is_friend = True

    # print("Tak") if profiles.user.id in friend_list else print("Nie")
    # print(friend_list)
    #
    # # print(x for x in request.user.friends.all())
    # friend = False
    # friend = True if profiles.user.email in friend_list else False
    # print(friend)

    Friend_request_show = Friend_Request.objects.filter(from_user=request.user, to_user=user_id)

    Friend_Request_exists = False

    if Friend_request_show.exists():
        Friend_Request_exists = True



    # if Friend_Request.objects.get(from_user=user_id, to_user=request.user).exists():
    #     print("istnieje")

    if request.method == 'POST':
      if form_reply.is_valid():
          form_reply.instance.reply_author = MyUser.objects.get(id=request.user.id)
          form_reply.instance.post = Post.objects.get(id=get_id)
          form_reply.save()
          return HttpResponseRedirect(request.path_info)

    context = {'user_posts' : user_posts, 'profiles' : profiles, 'Friend_Request_exists' : Friend_Request_exists,
               'Friend_request_show' : Friend_request_show, 'is_friend' : is_friend}
    return render(request, 'users/profile.html', context)




@login_required(login_url='login')
def friend_request(request):
    show_friend_request = Friend_Request.objects.filter(to_user=request.user)

    context = {'show_friend_request': show_friend_request}

    return render(request, 'users/friend_request.html', context)
