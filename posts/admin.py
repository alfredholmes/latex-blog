from django.contrib import admin

from .models import Post, PostMedium, RenderedPage, AboutSection, Category, TitleElement, SocialLink

admin.site.register(Post)
admin.site.register(PostMedium)
admin.site.register(RenderedPage)
admin.site.register(AboutSection)
admin.site.register(Category)
admin.site.register(TitleElement)
admin.site.register(SocialLink)
