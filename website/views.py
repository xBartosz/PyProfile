from django.shortcuts import render
from django.contrib.auth.views import LoginView, FormView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import UserRegisterForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Post
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


@login_required(login_url='login')
def index(request):
    return render(request, 'website/index.html')

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


