from django.shortcuts import render
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Value as V
from django.db.models.functions import Concat
from website.models import Post
from users.models import Profile

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
    profiles = Profile.objects.get(id=user_id)
    user_posts = Post.objects.filter(author=profiles.user)

    context = {
                'user_posts' : user_posts,
                'profiles' : profiles
               }

    return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def users_list(request):
    whole_list = Profile.objects.all()
    context = {'whole_list' : whole_list}

    return render(request, 'users/users_list.html', context)
