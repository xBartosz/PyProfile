from django.shortcuts import render
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required()
def profile(request):
    if request.method == "POST":
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your Profile has been updated!')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'p_form' : profile_form}

    return render(request, 'users/profile.html', context)
