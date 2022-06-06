from django.contrib import admin

from .models import Post, PostMedium, RenderedPage, AboutSection, Category

admin.site.register(Post)
admin.site.register(PostMedium)
admin.site.register(RenderedPage)
admin.site.register(AboutSection)
admin.site.register(Category)
