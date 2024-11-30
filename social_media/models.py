from django.core.exceptions import ValidationError
from django.db import models

from user.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="profile")
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/",
                                        blank=True,
                                        null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.user


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("Users cannot follow themselves.")

    def save(self, *args, **kwargs):
        # Ensure `clean` is called before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Followed: {self.follower} -> {self.following}"


class Post(models.Model):
    user = models.ForeignKey(User,
                             related_name="posts",
                             on_delete=models.CASCADE)
    content = models.TextField()
    media = models.FileField(upload_to="post_media/",
                             blank=True,
                             null=True)
    hashtags = models.ManyToManyField("Hashtag",
                                      related_name="posts",
                                      blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}\n{self.content}"


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User,
                             related_name="likes",
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             related_name="likes",
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"],
                                    name="unique_like")
        ]

    def __str__(self):
        return f"Liked: {self.user} -> {self.post}"


class Comment(models.Model):
    user = models.ForeignKey(User,
                             related_name="comments",
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             related_name="comments",
                             on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Commented: {self.user} -> {self.content}"
