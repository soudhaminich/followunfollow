from django import forms
from s3direct.widgets import S3DirectWidget
from ckeditor.widgets import CKEditorWidget
from tecsee.models import TecseeVideo

class S3DirectUploadForm(forms.ModelForm):
    class Meta:
        model = TecseeVideo
        fields = [
            'title',
            'description',
            'image',
            'video',   
            'duration',
            'tags'
        ]
        widgets = {'image': forms.URLField(widget=S3DirectWidget(dest='destination')), 
                   'video': forms.URLField(widget=S3DirectWidget(dest='destination')),
                   }


