from django import forms
from .models import Question, QuestionComment


QUESTION_TYPE_CHOICES = [('', 'select'), ('Q', 'Question'),
                         ('P', 'Problem'), ('T', 'Task')]

QUESTION_CATEGORY_CHOICE = [('', 'select'), ('python', 'Python'), ('django', 'Django'), ('sql', 'SQL'), ('postgresql', 'PostgreSQL'), ('oracle', 'Oracle'), ('mysql', 'MYSQL'),
                            ('javascript', 'Javascript'), ('java', 'Java'),   ('vuejs', 'VueJS'), ('html', 'HTML'), ('css', 'CSS'), ('unix', 'Unix'), ('shellscript', 'Shell Script'), ('other', 'Other')]

QUESTION_PRIORITY_CHOICE = [('', 'select'), ('L', 'Low'), ('M', 'Medium'),
                            ('H', 'High'), ('U', 'Urgent')]


class QuestionForm(forms.ModelForm):
    # email = forms.EmailField()
    title = forms.CharField(label="Title", help_text='Title must be 15 characters minimum(Be Specific)', widget=forms.TextInput(attrs={
                            'placeholder': 'e.g. How to resolve the Error("ValueError: source code string cannot contain null bytes") in Django?'}))

    ticket_type = forms.ChoiceField(
        label="Type", choices=QUESTION_TYPE_CHOICES)

    category = forms.ChoiceField(
        label="Area", choices=QUESTION_CATEGORY_CHOICE)

    priority = forms.ChoiceField(
        label="Priority", choices=QUESTION_PRIORITY_CHOICE)

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['priority'].choices = Question.AVAILABLE_PRIORITY_CHOICES
        if self.instance and self.instance.priority in [
                Question.PRIORITY_HIGH, Question.PRIORITY_URGENT]:
            self.fields['priority'].widget.attrs['disabled'] = True
            self.fields['priority'].required = False
        else:
            self.fields['priority'].choices = Question.AVAILABLE_PRIORITY_CHOICES

    # def __init__(self, *args, **kwargs):
    #     super(QuestionForm, self).__init__(*args, **kwargs)
    #     if self.instance and self.instance.priority in [Question.PRIORITY_HIGH, Question.PRIORITY_URGENT]:
    #         self.fields['priority'].widget.attrs['disabled'] = True
    #     else:
    #         self.fields['priority'].choices = Question.AVAILABLE_PRIORITY_CHOICES

    class Meta:
        model = Question
        # exclude = ('author',)
        fields = ['title', 'content', 'ticket_type', 'category', 'priority', ]

    def clean_title(self):
        # print(self.cleaned_data['username'])
        title = self.cleaned_data['title']
        if len(title) <= 15:
            raise forms.ValidationError(
                "Title must be at least 15 characters.")
        return title


class QuestionCommentForm(forms.ModelForm):
    class Meta:
        model = QuestionComment
        fields = ['content', ]
