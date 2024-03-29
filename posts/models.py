from django.db import models
from django.utils.text import slugify
from django.core.files import File
import os, bs4

import shutil

from django.conf import settings

default_tex = """\\documentclass{article}
%\\documentclass{book}
\\usepackage[margin=2cm]{geometry}
\\usepackage{geometry}
\\usepackage{amsmath}
\\usepackage{amsthm}
\\usepackage{amssymb}
\\usepackage{mathtools}
\\usepackage{url}
\\usepackage{cite}
\\usepackage{caption}
\\usepackage{subcaption}
\\usepackage[title]{appendix}
\\usepackage[colorlinks]{hyperref}
\\usepackage[capitalize,nameinlink,noabbrev]{cleveref}
\\usepackage[nottoc,notlot,notlof]{tocbibind}
\\usepackage{graphicx}


\\title{Default}

\\theoremstyle{definition}

\\newtheorem{definition}{Definition}[section]

\\newtheorem{example}[definition]{Example}
\\newtheorem{prop}[definition]{Proposition}
\\newtheorem{lemma}[definition]{Lemma}
\\newtheorem{thm}[definition]{Theorem}
\\newtheorem{cor}[definition]{Corollary}
\\newtheorem{rmk}[definition]{Remark}

\\begin{document}
\\maketitle
\\section{Introduction}

This is the default post

\\end{document}
"""


class TitleElement(models.Model):
    """
        Text to be rendered at the top of every page, for example the name of the blog
    """
    text = models.CharField(max_length=200)
    size = models.IntegerField()

    def __str__(self):
        return self.text


class HeadElement(models.Model):
    """
        HTML to be added into the <head></head> at the top of the page, for example google analytics
    """
    html = models.TextField()

class SocialLink(models.Model):
    """
        Links which appear in some pages, eg about or at the bottom of the page in the mobile view.
    """
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Category(models.Model):
    """
        Category for the posts. Posts are categorised in the /collections page
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title



class AboutSection(models.Model):
    """
        Text to be added to the about section

        TODO: Allow images etc.
    """
    title = models.CharField(max_length=200)
    text = models.TextField()
    order_int = models.IntegerField()


class Post(models.Model):
    """
        Post objects
    """
    title = models.CharField(max_length=200)
    publication_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(editable=False, unique=True)
    latex = models.TextField(default=default_tex)
    categories = models.ManyToManyField(Category, blank=True)
    abstract = models.TextField()
    share_pdf = models.BooleanField()

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        path = os.path.join(settings.MEDIA_ROOT, f'posts/{self.slug}')
        shutil.rmtree(path)

    def save(self, *args, **kwargs):
        #first save the images etc
        #render_html
        #check to see if there is already a post with this slug
        if len(Post.objects.filter(slug=slugify(self.title))) > 0 and self.slug == "":
            hits = len(Post.objects.filter(slug__contains=slugify(self.title)))
            self.slug = slugify(self.title + ' ' + str(hits + 1))
        elif self.slug == "":
            self.slug = slugify(self.title)


        
        path = os.path.join(settings.MEDIA_ROOT, f'posts/{self.slug}')
        
        #get the directory of the files - needs to work when there are no additional files.
        original_dir = os.getcwd()                 
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        os.chdir(path)


        with open(self.slug + '.tex', 'w') as f:
            f.write(self.latex)
        
        os.system('make4ht ' + self.slug + '.tex "mathml,mathjax"')

        os.system('pdflatex -interaction=nonstopmode ' + self.slug)
        os.system('pdflatex -interaction=nonstopmode ' + self.slug)
        
        super().save(*args, **kwargs)

        #deal with generated css and images 
        filetypes = ['jpg', 'svg', 'css', 'png', 'pdf']
        images = [filename for filename in os.listdir() if filename.split('.')[-1].lower() in filetypes]
        urls = {}
        saved_files = PostMedium.objects.filter(post=self)
        saved_file_names = [f.media.name for f in saved_files]
        for image in images:
            name = f'posts/{self.slug}/{image}'
            media = PostMedium(post=self)
            #check if this already exists
            if name in saved_file_names: 
                file = saved_files[saved_file_names.index(name)]
                urls[image] = file.media.url
                continue
            media.media.name = name
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





class RenderedPage(models.Model):
    """
        Model to hold the rendered html of a post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.SlugField() #name of the html file - used for links
    head = models.TextField()  #to link the stylesheets etc and pages
    body = models.TextField()  #main page rendering

    def __str__(self):
        return f'{self.post.slug}/{self.name}'

def post_file_path(instance, filename):
    return 'posts/' + instance.post.slug + '/' + filename

class  PostMedium(models.Model):
    """
        Model to handle post dependencies, for example stylesheets and images
    """
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
