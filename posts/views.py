from django.shortcuts import render
from django.http import Http404

from .models import Post, AboutSection, Category, TitleElement, SocialLink

def get_title_data():
    headers = TitleElement.objects.all()
    socials = SocialLink.objects.all()
    return {'titles': headers, 'socials': socials}
    


def index(request):
    data = get_title_data()
    data['post_list'] = Post.objects.all().order_by('-publication_date')
    return render(request, 'posts/index.html', data)

def post(request, post_slug):
    data = get_title_data()
    try:
        post = Post.objects.get(slug=post_slug)
        content = post.renderedpage_set.all()[0] 
        header = content.head 
        body = content.body
    
        data['post'] = post
        data['header'] = header
        data['body'] = body
        return render(request, 'posts/post.html', data)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")



def post_page(request, post_slug, html_slug):
    data = get_title_data()
    try:
        post = Post.objects.get(slug=post_slug)
        content = post.renderedpage_set.filter(name='.'.join(html_slug.split('.')[:-1]))[0] 
        header = content.head 
        body = content.body
        data['post'] = post
        data['header'] = header
        data['body'] = body
        return render(request, 'posts/post.html', data)
    except IndexError:
        raise Http404("Page does not exist")
    except Page.DoesNotExist:
        raise Http404("Post does not exist")


def collections(request):
    #get collections and <=5 most recent posts from each, order by recently updated
    data = get_title_data() 
    try:
        collections = Category.objects.all()
        posts = {}
        for collection in collections: 
            posts[collection] = collection.post_set.all().reverse()[:5]

        data['collections'] = posts

        return render(request, 'posts/collections.html', data)
    except:
        raise Http404("Collection Missing")

def collection(request, collection_slug):
    data = get_title_data()
    try:
        collection = Category.objects.get(slug = collection_slug) 
        posts = {collection: collection.post_set.all()} 

    except Collection.DoesNotExist:
        raise Http404('Collection does not exit') 
    
    data['collections'] = posts

    return render(request, 'posts/collections.html', data)

def about(request):

    data = get_title_data()
    try:
        sections = AboutSection.objects.all()
        data['sections'] = sections
        return render(request, 'posts/about.html', data)
    except:
        raise Http404('About page does not exist')
    
