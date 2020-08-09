from django.db import models
from django.utils import timezone
from django.urls import reverse
from django import forms
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from taggit.managers import TaggableManager

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description  = RichTextField(blank = True, null = "")
    tags = TaggableManager()
    text = RichTextField(blank = True, null = True)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})

    
class createPost(forms.ModelForm):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget = forms.Textarea, required=False, max_length=200)
    text=forms.CharField(widget = CKEditorWidget())

    def __init__(self, *args, **kwargs):
        super(createPost, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'titleclass'})
        self.fields['description'].widget.attrs.update({'class' : 'descriptionclass'})
        self.fields['text'].widget.attrs.update({'class' : 'textclass'})
    
    def set_disable(self,*args,**kwargs):
        super(createPost,self).__init__(*args,**kwargs)
        self.fields['title'].disabled=True
        self.fields['text'].disabled=True
        self.fields['description'].disabled=True
        self.fields['tags'].disabled=True

    class Meta:
        model=Post
        fields=('title','tags','description','text')
        labels = {
            "title":"titleclass",
            "description":"descriptionclass"
        }


class Comment(models.Model) :
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name = 'commenter')
    body  = RichTextField(blank = True, null = "")
    create_date = models.DateTimeField('time',auto_now_add=True)
    belong = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank = True, null = True)


    class Meta:
        verbose_name = 'commentor'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']
    

class createComment(forms.ModelForm):
    text=forms.CharField(widget = CKEditorWidget())

    class Meta:
        model=Comment
        fields=('text',)