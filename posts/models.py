from django.db import models
from django.utils.text import slugify


class Post(models.Model):
	title = models.CharField(max_length=200)
	publication_date = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(editable=False)
	html = models.TextField(editable=False)
	latex = models.TextField()

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		#render_html
		self.html = self.latex
		self.slug = slugify(self.title)
		super().save(*args, **kwargs)


#model to hold the rendered html, keeping the latex page structure
class RenderedPage(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	name = models.CharField(max_length=200) #name of the html file - used for links
	body = models.TextField()  #to link the stylesheets etc and pages
	head = models.TextField()  #main page rendering

def post_file_path(instance, filename):
	return 'posts/' + instance.post.slug + '/' + filename

#model to handle post dependencies, for example stylesheets and images
class  PostMedia(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	media = models.FileField(upload_to=post_file_path)
