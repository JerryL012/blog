from django.shortcuts import render, redirect
from .models import Post
from follow.models import Follow
# all we need to paginate query sets
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q

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
    featured = Post.objects.filter(featured=True)
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
    return render(request, 'post.html', {})
