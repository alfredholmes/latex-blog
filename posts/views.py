from django.shortcuts import render

from .models import Post

def index(request):
	return render(request, 'posts/index.html', {'post_list': Post.objects.all()})
def post(request, post_slug):
	try:
		post = Post.objects.get(slug=post_slug)
	except Post.DoesNotExist:
		raise Http404("Post does not exist")
	return render(request, 'posts/post.html', {'post': post})
