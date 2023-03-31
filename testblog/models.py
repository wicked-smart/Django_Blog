from django.db import models
from django.contrib.auth.models import AbstractUser
from pytz import timezone
from datetime import datetime

# Create your models here.

class User(AbstractUser):
    pass 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="This bio needs to be changed!")
    followers = models.ManyToManyField(User, blank=True, related_name="following")
    following = models.ManyToManyField(User, blank=True, related_name="followers")
    #avatar = models.ImageField(upload_to='imgs', default='avatar.jpg')

    def __str__(self):
        return f"{self.user.username}"


def get_default_user():
    return User.objects.get(pk=1)


class Blog(models.Model):
    title = models.CharField(max_length=500)
    author = models.ForeignKey(User, related_name="blogs", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True, default=None)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def is_published(self):
        return self.created_at != None
    
    def publish(self):
        self.created_at = datetime.now(timezone('Asia/calcutta'))


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    blog = models.ManyToManyField(Blog, related_name="tags")




class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    written_by = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")

    def __str__(self):
        return f"{self.written_by.user.username} commented on blog titled {self.blog} created at {self.created_at}"
    
    class Meta:
        ordering=['-created_at']
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self)
    
    @property
    def is_parent(self):
        return self.parent is None 
