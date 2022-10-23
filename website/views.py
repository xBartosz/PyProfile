import unidecode
from django.shortcuts import render
from django.contrib.auth.views import LoginView, FormView
import random
import string
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .forms import UserRegisterForm, PostForm, ReplyForm, PostLike, ReportForm
from django.contrib.auth.decorators import login_required
from .models import Post, MyUser, Reply_for_post, Report_post, Likes
from django.db.models import Q
from django.contrib import messages
from chat.models import Message
from friends.models import Friend_Request
from notifications.models import Notification



class RegisterFunction(FormView):
    template_name = 'website/register.html'
    redirect_authenticated_user = True
    form_class = UserRegisterForm
    success_url = reverse_lazy('index')
    def form_valid(self, form):
        digits = string.digits
        form.instance.user_name = form.instance.first_name + (''.join(random.choice(digits) for i in range(5)))
        form.instance.user_name = unidecode.unidecode(form.instance.user_name)
        form.instance.email = form.instance.email.lower()
        user = form.save()

        if user is not None:
            login(self.request, user)
        return super(RegisterFunction, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterFunction, self).get(request, *args, **kwargs)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email.lower(), password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.success(request, ("Wrong password or login"))
                return redirect('login')
        else:
            return render(request, 'website/login.html')

@login_required(login_url='login')
def detail_view(request, pk):
    detail_post = Post.objects.filter(id=pk)
    likes = Likes.objects.all()


    context = {'detail_post' : detail_post, 'likes': likes}

    return render(request, 'website/detail_view.html', context)

@login_required(login_url='login')
def index(request):
    get_id = request.POST.get("post_id")

    #if author is friend
    friends = request.user.friends.all().order_by('first_name')
    posts = Post.objects.filter(Q(author__in=friends) | Q(author=request.user)).order_by('-post_date')
    likes = Likes.objects.all()





    # post = Post.objects.filter(id=get_id)
    # print(get_id)
    # liked = False
    # if Likes.objects.get(post=post, user=request.user).exists():
    #     liked = False
    # else:
    #     liked = True

    form_post = PostForm(request.POST or None)
    form_reply = ReplyForm(request.POST or None)



    if request.method == 'POST':
        if form_post.is_valid():
            form_post.instance.author = MyUser.objects.get(id=request.user.id)
            form_post.save()
            return redirect('index')

        if form_reply.is_valid():
            form_reply.instance.reply_author = MyUser.objects.get(id=request.user.id)
            form_reply.instance.post = Post.objects.get(id=get_id)
            form_reply.save()
            return redirect('index')

    context = {'friends': friends, 'form_post': form_post, 'posts': posts, 'likes': likes}
    return render(request, 'website/index.html', context)

@login_required(login_url='login')
def delete_post(request, id):

    post = Post.objects.get(id=id)
    if post.author == request.user:
        post.delete()
        return redirect('index')
    else:
        return redirect('index')

@login_required(login_url='login')
def update_post(request, id):
    post = Post.objects.get(id=id)
    form_post = PostForm(request.POST or None, instance=post)
    # form_post.post_content = Post.objects.values_list('post_content').get(id=id)
    # print(form_post.post_content)
    if form_post.is_valid():
        if request.user == post.author:
            post.edited = True
            form_post.save()
            # return HttpResponseRedirect(reverse('detail_view', args=[id]))
            messages.success(request, 'Your Post has been updated!')
            return redirect('index')

        else:
            return redirect('index')

    context = {'form_post': form_post, 'post': post}
    return render(request, 'website/update_post.html', context)


def Report_function(request, id):
    form_report = ReportForm(request.POST or None)
    form_report.instance.post = Post.objects.get(id=id)
    form_report.instance.applicant = request.user
    if request.method == "POST":
        if form_report.is_valid():
            if Report_post.objects.filter(post=id, applicant=form_report.instance.applicant,
                                          reason=form_report.instance.reason).exists():
                messages.success(request, "Post already reported!")
                return redirect('index')
            else:
                form_report.save()
                messages.success(request, "Post Reported successfully")
                return redirect('index')
    context = {'form_report': form_report}
    return render(request, 'website/report_post.html', context)


@login_required(login_url='login')
def like_post(request, id):
    # post = get_object_or_404(Post, id=request.POST.get("post_id_like"))
    post = Post.objects.get(id=id)
    post_is_liked = Likes.objects.filter(post=post, user=request.user)
    number_of_likes = post.likes
    liked = False
    if post_is_liked.exists():
        post_is_liked.delete()
        post.user_likes.remove(request.user)
        number_of_likes -= 1
        liked = False
    else:
        Likes.objects.create(post=post, user=request.user)
        post.user_likes.add(request.user)
        number_of_likes += 1
        liked = True
    post.likes = number_of_likes
    post.save()


    # if post.likes.filter(id=request.user.id).exists():
    #     post.likes.remove(request.user)
    #     liked = False
    # else:
    #     post.likes.add(request.user)
    #     liked = True

    # Changed because after like in profile redirected to the index page
    return redirect(request.META['HTTP_REFERER'])

