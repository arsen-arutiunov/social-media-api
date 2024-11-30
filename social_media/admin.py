from django.contrib import admin

from social_media.models import (
    Post,
    Profile,
    Follow,
    Hashtag,
    Like,
    Comment
)


admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Hashtag)
admin.site.register(Like)
admin.site.register(Comment)
