from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
@login_required
def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)


@csrf_exempt
def about(request):
    return render(request, "blog/about.html", {"title": "About"})


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = [
        "-date_posted"
    ]  # here we are specifing the blog home to have newer tweets in the start of the page, minus is from newer to older
    paginate_by = 5  # here we specifying to have 2 objects per page


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_post.html"
    context_object_name = "posts"
    paginate_by = 3  # here we specifying to have 2 objects per page

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView):
    model = Post
    # <app>/<model>_<viewtype>.html  i.e blog/post_detail.html , here if we mention the template name as per django convention, no need to specify in the view, it will takecare in the background
    # context_object_name will be - object (which we have mention in the template)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]
    # here the template name will be post_form.html bec both create and update will use the same form, so the convention is to name <app>/<model>_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # here we are overiding the class form by setting the author equals to the signed in user


# similar to createview
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]
    # here the template name will be post_form.html bec both create and update will use the same form, so the convention is to name <app>/<model>_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()  # to get the object of the current logedin user
        if self.request.user == post.author:
            return True
        return False

    # here the UserPassesTestMixin will run the test_func method to check only the current logedin user can update his post but not others


# similar to detailview
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"  # we are adding this bec, to tell django where to go after deleting the post, in the earlier in create and update it was routed to the detail page

    def test_func(self):
        post = self.get_object()  # to get the object of the current logedin user
        if self.request.user == post.author:
            return True
        return False