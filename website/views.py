from django.shortcuts import render
from django.contrib.auth.views import LoginView, FormView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import users.models
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .forms import UserRegisterForm, PostForm, ReplyForm, PostLike, ReportForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Post, MyUser, Reply_for_post, Report_post
from django.contrib.auth.models import User
from django.db.models import Q


from django.contrib import messages


class RegisterFunction(FormView):
    template_name = 'website/register.html'
    redirect_authenticated_user = True
    form_class = UserRegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()

        if user is not None:
            login(self.request, user)
        return super(RegisterFunction, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterFunction, self).get(request, *args, **kwargs)


# class LoginFunction(LoginView):
#     template_name = 'website/login.html'
#     redirect_authenticated_user = True
#     next_page = 'index'

def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
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


    context = {'detail_post' : detail_post}

    return render(request, 'website/detail_view.html', context)

@login_required(login_url='login')
def index(request):
    get_id = request.POST.get("post_id")


#if author is friend
    friends = request.user.friends.all()
    # posts = Post.objects.all().order_by('-post_date')
    # print(friends)
    # posts1 = Q(author__contains=friends)
    # posts2 = Q(author_contains=request.user)
    # print(posts1)
    posts = Post.objects.filter(Q(author__in=friends) | Q(author=request.user)).order_by('-post_date')
    # print(posts1)
    # print(posts)

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



    context = {'friends': friends, 'form_post': form_post, 'posts': posts}
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
    form_post = PostForm(request.POST or None)
    # form_post.post_content = Post.objects.values_list('post_content').get(id=id)
    # print(form_post.post_content)
    if form_post.is_valid():
        if request.user == post.author:
            form_post.save()
            return HttpResponseRedirect(reverse('detail_view', args=[id]))

        else:
            return redirect('index')

    context = {'form_post' : form_post, 'post' : post}
    return render(request, 'website/update_post.html', context)

def Report_function(request, id):

    form_report = ReportForm(request.POST or None)
    form_report.instance.post = Post.objects.get(id=id)
    form_report.instance.applicant = request.user
    if request.method == "POST":
        if form_report.is_valid():
            if Report_post.objects.filter(post=id, applicant=form_report.instance.applicant, reason=form_report.instance.reason).exists():
                messages.success(request, ("Post already reported!"))
                return redirect('index')
            else:
                form_report.save()
                messages.success(request, ("Post Reported successfully"))
                return redirect('index')
    context = {'form_report' : form_report}
    return render(request, 'website/report_post.html', context)

@login_required(login_url='login')
def like_post(request, id):
    post = get_object_or_404(Post, id=request.POST.get("post_id_like"))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    # Changed because after like in profile redirected to the index page
    return HttpResponseRedirect(reverse('index'))

# class Report_for_post(CreateView):
#     model = Report_post
#     form_class = ReportForm
#     # fields = ['post', 'reason']
#     template_name = 'website/report_post.html'
#     success_url = reverse_lazy('index')
#
#     print(form_class)
    # def form_valid(self, form):
    #     form.instance.post = Post.objects.get(id=id)
    #     ReportForm.save()
    #     print(form.instance.Post)
    #     return super(Report_for_post, self).form_valid(form)

# def Report_for_post(request, id):
#     post = Post.objects.get(id=id)
#     form_report = ReportForm(request.POST or None)
#     if form_report.is_valid:
#         form_report.instance = post
#
#         form_report.save()
#         return redirect('index')
#     context = {'form_report' : form_report}
#     return render(request, 'website/report_post.html', context)

    #
    # def mount(self):
    #     self.author = MyUser.objects.get(email=self.request.user)
    #     self.posts = Post.objects.all().order_by('-post_date')
    #     return super().mount()
    #
    # def submit(self):
    #     if len(self.content) >= 3:
    #         Post.objects.create(
    #             author=self.author,
    #             post_content=self.content
    #         )
    #         self.content = ""
    #         self.posts = Post.objects.all().order_by('-post_date')
    #     else:
    #         messages.success(self.request, "Length of the comment must be at least 3 signs")





# def LikeView(request, pk):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     post.likes.add(request.user)
#



# def authenticate_user(email, password):
#     try:
#         user = User.objects.get(email=email)
#     except User.DoesNotExist:
#         return None
#     else:
#         if user.check_password(password):
#             return user
#
#     return None
#
# class LoginFunction(FormView):
#     template_name = 'website/login.html'
#
#     def get(self, request):
#         return render(request, self.template_name)
#
#     def post(self, request):
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate_user(email, password)
#
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#
#                 return redirect(self.request.GET.get('next', '/'))
#             else:
#                 messages.success(self.request, "user is not active")
#                 return redirect(self.request.GET.get('next', '/'))
#         else:
#             messages.success(self.request, "email or password not correct")
#             return redirect(self.request.GET.get('next', '/'))



# class IndexWebsite(ListView):
#     model = Post
#     template_name='website/index.html'
#
#     form = PostForm
#
#     def post(self, request, *args ,**kwargs):
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = self.get_object()
#             form.instance.user = request.user
#             form.instance.post = post
#             form.save()
#
#             return super(IndexWebsite, self).form_valid(form)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         Post_data = Post.objects.all()
#         context = super().get_context_data(**kwargs)
#         context['add_comment'] = self.form
#         return context
#



# class Posts(ListView, CreateView, DeleteView):
#     model = Post
#     template_name = 'website/index.html'
#
#     def show_post(self, request):
#         context_object_name = 'post_view'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['posts'] = Post.objects.filter(user=self.request.user)
#
#         return context
#     #
    # def postCreate(self, request):
    #     fields = ['post_context']
    #
    #     def form_valid(self, form):
    #         form.instance.user = self.request.user
    #         return super(postCreate, self).form_valid(form)


# class PostCreate(CreateView):
#     model = Post
#     template_name = 'website/index.html'
#     fields = ['post_context']
#     context_object_name = 'post_create'
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(PostCreate, self).form_valid(form)
#
# class PostDelete(DeleteView):
#     model = Post
#     template_name = 'website/index.html'
#     context_object_name = 'post_delete'
# # def index(request):
# #     return render(request, 'website/index.html')
#
#


