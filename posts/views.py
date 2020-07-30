from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Post
from follow.models import Follow
# all we need to paginate query sets
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from .forms import CommentForm
# operate post, class based view
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    # match the post text
    if query:
        queryset = queryset.filter(
            # title that contains the query
            Q(title__icontains=query)|  # or
            Q(overview__icontains=query)
        ).distinct()  # if the same post, only get one
    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)

def get_category_count():
    # all the categories of posts. annotate returns a dict where each key is each category
    #Count() counts the num of posts whose category is category
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset

def index(request):
    # grab the post with true featured
    featured = Post.objects.order_by('-timestamp')
    featured = featured.filter(featured=True)[0:3]
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_follow = Follow()
        new_follow.email = email
        new_follow.save()

    context = {
        'object_list': featured,
        'latest': latest
    }
    return render(request, 'index.html', context)

def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    # how many it should hold in one page
    paginator = Paginator(post_list, 4)
    # page passed in the url, like ?page==1. page is the page number, 1234...
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    # check whether the page is empty or page parameter is wrong
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        # go to the page 1
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        # return the num of pages. e.g 100 posts, per 4, so it should be 25 pages, the last page
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
        'most_recent': most_recent,
        'category_count': category_count
    }
    return render(request, 'blog.html', context)

def post(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'id': post.id
            }))

    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'post.html', context)

def contact(request):
    return render(request, 'contact.html')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'

    fields = ['thumbnail', 'title', 'categories', 'overview', 'content']
    # get the author of this post
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['thumbnail', 'title', 'categories', 'overview', 'content']
    # get the author of this post
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)
    # check whether user is the author of the post?(maybe need some changes)
    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    # if success, redirect to home page
    success_url = '/'

    # check whether user is the author of the post?(maybe need some changes)
    def test_func(self):
        post = self.get_object()
        if self.request.user.profile == post.author:
            return True
        return False

# class based view
# class PostListView(ListView):
#     model = Post
#     template_name = 'index.html'
#     context_object_name = 'latest'
#     ordering = ['-timestamp']
