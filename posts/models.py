from django.db import models
from django.utils.text import slugify
from django.core.files import File
import os, bs4

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title



class AboutSection(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()


class Post(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(editable=False, unique=True)
    latex = models.TextField()
    categories = models.ManyToManyField(Category, blank=True)
    abstract = models.TextField()


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        #render_html
        #check to see if there is already a post with this slug
        if len(Post.objects.filter(slug=slugify(self.title))) > 0 and self.slug == "":
            hits = len(Post.objects.filter(slug__contains=slugify(self.title)))
            self.slug = slugify(self.title + ' ' + str(hits + 1))
        elif self.slug == "":
            self.slug = slugify(self.title)
        
        path = 'media/posts/' + self.slug
        
        #get the directory of the files - needs to work when there are no additional files.
        original_dir = os.getcwd()                 
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        os.chdir(path)


        with open(self.slug + '.tex', 'w') as f:
            f.write(self.latex)
        
        os.system('make4ht ' + self.slug + '.tex "html,mathjax"')

        os.system('pdflatex ' + self.slug)


        super().save(*args, **kwargs)
        #deal with generated css and images 
        images = [filename for filename in os.listdir() if self.slug in filename and ('.svg' in filename or '.css' in filename)]
        urls = {}
        for image in images:
            with open(image) as f:
                django_file = File(f)
                media = PostMedium(post=self, media=django_file)
                media.save()
                urls[image] = media.media.url
        #load html into the database
        html_files = [filename for filename in os.listdir() if self.slug in filename and '.html' in filename]
        for html_file in html_files:
            with open(html_file) as f:
                txt = f.read()
            #webpage = bs4.BeautifulSoup(txt)

            head = txt.split('<head>')[1] 
            head = head.split('</head>')[0] 
            
            body = txt.split('<body>')[1] 
            body = body.split('</body>')[0] 
            slug = slugify(html_file[:-5])
            
            for image, url in urls.items():
                head = f'src=\'{url}\''.join(head.split(f'src=\'{image}\''))
                head = f'href=\'{url}\''.join(head.split(f'href=\'{image}\''))
                body = f'src=\'{url}\''.join(body.split(f'src=\'{image}\''))
                body = f'href=\'{url}\''.join(body.split(f'href=\'{image}\''))
            try:
                page = self.renderedpage_set.filter(name=slug)[0]
                page.head = head
                page.body = body
            except IndexError:
                page = RenderedPage(post=self, name=slug, head=head, body=body)
            page.save()
        os.chdir(original_dir)


#model to hold the rendered html, keeping the latex page structure
class RenderedPage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.SlugField() #name of the html file - used for links
    head = models.TextField()  #to link the stylesheets etc and pages
    body = models.TextField()  #main page rendering

    def __str__(self):
        return f'{self.post.slug}/{self.name}'

def post_file_path(instance, filename):
    return 'posts/' + instance.post.slug + '/' + filename

#model to handle post dependencies, for example stylesheets and images
class  PostMedium(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    media = models.FileField(upload_to=post_file_path)
    class Meta:
        verbose_name_plural = "post media"

    def __str__(self):
        import os
        return os.path.basename(self.media.path)


    
class SeeAlso(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    related_posts = models.ManyToManyField(Post, blank=True, related_name='related_posts')
