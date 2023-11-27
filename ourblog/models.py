from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=255)
    post_image = models.ImageField(null=True, blank=True, upload_to='images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    post_video = models.FileField(null=True, blank=True, upload_to='videos')
    update_date = models.DateTimeField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    dislikes = models.ManyToManyField(User, related_name='blog_posts_dislikes')


    def save(self, *args, **kwargs):
        if not self.id:  # If it's a new post
            self.update_date = None  # Set to None on creation
        else:
            self.update_date = timezone.now()  # Set to current time when updated
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()


    def __str__(self) :
        return self.title + ' | ' + str(self.author)


    def get_absolute_url(self):
        return reverse('home')