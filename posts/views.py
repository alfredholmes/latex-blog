from django.shortcuts import render

from .models import Post, AboutSection, Category

def index(request):
    return render(request, 'posts/index.html', {'post_list': Post.objects.all()})

def post(request, post_slug):
    try:
        post = Post.objects.get(slug=post_slug)
        content = post.renderedpage_set.all()[0] 
        header = content.head 
        body = content.body
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, 'posts/post.html', {'post': post, 'header': header, 'body': body})


def post_page(request, post_slug, html_slug):
    try:
        post = Post.objects.get(slug=post_slug)
        content = post.renderedpage_set.filter(name='.'.join(html_slug.split('.')[:-1]))[0] 
        header = content.head 
        body = content.body
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, 'posts/post.html', {'post': post, 'header': header, 'body': body})

def collections(request):
    #get collections and <=5 most recent posts from each, order by recently updated
    collections = Category.objects.all()
    posts = {}
    for collection in collections: 
        posts[collection] = collection.post_set.all()

    return render(request, 'posts/collections.html', {'collections': posts})


def collection(request, collection_slug):
    try:
        collection = Category.objects.get(slug = collection_slug) 
        title = collection.title
        posts = collection.posts 

    except Collection.DoesNotExist:
       raise Http404('Collection does not exit') 
    return render(request, 'posts/collection.html', {'collections': collections})

def about(request):
    sections = AboutSection.objects.all()
    return render(request, 'posts/about.html', {'sections': sections})
    
