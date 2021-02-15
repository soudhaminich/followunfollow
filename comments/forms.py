from django import forms

from .models import Comment
from markdownx.fields import MarkdownxFormField
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.ModelForm):
    # email = forms.EmailField()
    # comment = forms.CharField(label='', widget=forms.Textarea)
    # comment =  forms.CharField(
    #     widget=forms.Textarea(
    #             attrs={
    #                 "rows": "4",
    #                 "class": "form-control",
    #                 "placeholder": "Write your comment/question"
    #             }
    #             )
    #     )
    # comment = forms.CharField(widget=CKEditorWidget(
    #     attrs={"placeholder": "Write your comment/question"}))
    # MarkdownWidget()

    class Meta:
        model = Comment

        fields = ['comment', ]

    # def clean_comment(self):
    #     print(dir(self))
    #     data = self.cleaned_data['comment']
    #     return data
