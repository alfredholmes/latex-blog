from django.db import models
from django.utils.text import slugify
from django.core.files import File

class Category(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField()


class Post(models.Model):
	title = models.CharField(max_length=200)
	publication_date = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(editable=False, unique=True)
	latex = models.TextField()
	categories = models.ManyToManyField(Category, blank=True)


	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		#render_html
		
		self.latex
		#check to see if there is already a post with this slug
		if len(Post.objects.filter(slug=slugify(self.title))) > 0:
			hits = len(Post.objects.filter(slug__contains=slugify(self.title)))
			self.slug = slugify(self.title + ' ' + str(hits + 1))
		else:
			self.slug = slugify(self.title)
		
		path = 'media/posts/' + self.slug
		import os
		
		#get the directory of the files - needs to work when there are no additional files.
		
		os.mkdir(path)
		os.chdir(path)


		with open(self.slug + '.tex', 'w') as f:
			f.write(self.latex)
		
		os.system('make4ht ' + self.slug + '.tex "html,svg"')
		os.system('pdflatex ' + self.slug)


		#deal with html
		
		#deal with css

		super().save(*args, **kwargs)
		#deal with generated images 
		images = [filename for filename in os.listdir() if self.slug in filename and '.svg' in filename]
		for image in images:
			with open(image, 'rb') as f:
				django_file = File(f)
				media = PostMedia(post=self, media=django_file)
				media.save()
		os.chdir('../')


#model to hold the rendered html, keeping the latex page structure
class RenderedPage(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	name = models.SlugField() #name of the html file - used for links
	body = models.TextField()  #to link the stylesheets etc and pages
	head = models.TextField()  #main page rendering

def post_file_path(instance, filename):
	return 'media/posts/' + instance.post.slug + '/' + filename

#model to handle post dependencies, for example stylesheets and images
class  PostMedia(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	media = models.FileField(upload_to=post_file_path)




	
