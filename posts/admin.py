from django.contrib import admin

from .models import Post, PostMedium, RenderedPage, AboutSection, Category, TitleElement, SocialLink



class PostMediumInline(admin.StackedInline):
    model = PostMedium

class PostAdmin(admin.ModelAdmin):
    inlines = [PostMediumInline]

    def delete_queryset(self, request, queryset):
        for post in queryset:
            post.delete()
            

admin.site.register(Post, PostAdmin)
admin.site.register(PostMedium)
admin.site.register(RenderedPage)
admin.site.register(AboutSection)
admin.site.register(Category)
admin.site.register(TitleElement)
admin.site.register(SocialLink)
