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
