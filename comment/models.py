from django.db import models
from blog.models import Blog  # Replace 'OtherApp' with the actual name of the app where Blog is defined

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.blog.title}"
