from django import forms
from .models import Post
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

class PostCreationForm(forms.ModelForm):
    # email = forms.EmailField()
    tags = forms.CharField(label="Tags", widget=forms.TextInput(attrs={'placeholder': 'Add up to 4 tags ...'}))
    class Meta:
        model = Post
        # exclude = ('author',)
        fields = ['title', 'content', 'blog_image', 'tags']

    def clean_tags(self):
        tn = self.cleaned_data.get('tags', [])
        total_tag = tn.split(',')
        # print(total_tag)
        # print(len(tn))
        if len(total_tag) > 4:
            raise ValidationError('tag_list: exceed the maximum of 4 tags', code='invalid')
        for t in total_tag:
            if not t.isalpha():
                raise ValidationError('Tags should be character shouldnot be any special characters or numbers')
        # print(tn)
        return total_tag

    # def send_email(self):
    #     send_mail('Test from blog 1', 'body', settings.EMAIL_HOST_USER,['tagnev.vengat@gmail.com'],fail_silently=False)

    #     print(True)
    #     return True


# class LoginForm(UserCreationForm):

#     class Meta:
#          model = User
#         fields = ['username', 'password1']

class PostUpdateForm(forms.ModelForm):
    # email = forms.EmailField()
    
    class Meta:
        model = Post
        # exclude = ('author',)
        fields = ['title', 'content', 'blog_image', 'tags']

    def clean_tags(self):
        tn = self.cleaned_data.get('tags', [])
        if len(tn) > 4:
            raise ValidationError('tag_list: exceed the maximum of 4 tags', code='invalid')
        for t in tn:
            if not t.isalpha():
                raise ValidationError('Tags should be character shouldnot be any special characters or numbers')
        return tn