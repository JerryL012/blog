from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce import HTMLField

User = get_user_model()
class Author(models.Model):
    profile_picture = models.ImageField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

# one post card
class Post(models.Model):
    categories = models.ManyToManyField(Category)
    title = models.CharField(max_length=100)
    overview = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    # image on the right
    thumbnail = models.ImageField()
    # tinymce
    content = HTMLField()

    # if true, render it on the latest post on the page
    featured = models.BooleanField(default=True)

    # previous post and next post
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'id': self.id
        })
