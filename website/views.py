from django.shortcuts import render
from django.contrib.auth.views import LoginView, FormView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import users.models
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .forms import UserRegisterForm, PostForm, ReplyForm, PostLike
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Post, MyUser, Reply_for_post
from django.contrib.auth.models import User


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


class LoginFunction(LoginView):
    template_name = 'website/login.html'
    redirect_authenticated_user = True
    next_page = 'index'



@login_required(login_url='login')
def index(request):
    get_id = request.POST.get("post_id")
    get_id2 = request.POST.get("id_post")


    friends = users.models.Profile.objects.exclude(id=request.user.id)
    posts = Post.objects.all().order_by('-post_date')


    form_post = PostForm(request.POST or None)
    form_reply = ReplyForm(request.POST or None)


    liked = False




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



    context = {'friends': friends, 'form_post': form_post, 'posts': posts, 'liked' : liked
               }
    return render(request, 'website/index.html', context)

def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('index')

def update_post(request, id):
    post = Post.objects.get(id=id)
    form_post = PostForm(request.POST or None, instance=post)

    if form_post.is_valid():
        form_post.save()
        return redirect('index')

    context = {'form_post' : form_post, 'post' : post}
    return render(request, 'website/update_post.html', context)

def like_post(request, id):
    post = get_object_or_404(Post, id=request.POST.get("post_id_like"))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('index'))

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


