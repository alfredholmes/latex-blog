from django.contrib import admin

from .models import Post, PostMedia

admin.site.register(Post)
admin.site.register(PostMedia)
