from django.db import models
from django.utils import timezone
from django import forms

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
class createPost(forms.ModelForm):
    title = forms.CharField(max_length=200)
    text=forms.CharField(widget=forms.Textarea)

    def set_disable(self,*args,**kwargs):
        super(createPost,self).__init__(*args,**kwargs)
        self.fields['title'].disabled=True
        self.fields['text'].disabled=True

    class Meta:
        model=Post
        fields=('title','text',)