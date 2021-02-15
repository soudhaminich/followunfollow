import django_filters
from django import forms
from . models import Question


class QuestionFilter(django_filters.FilterSet):
    STATUS_CHOICE = [('I', 'In-Progress'), ('O', 'Opened'),
                     ('C', 'Closed'), ]
    PRIORITY_LOW = 'L'
    PRIORITY_MEDIUM = 'M'
    PRIORITY_HIGH = 'H'
    PRIORITY_URGENT = 'U'
    PRIORITY_CHOICES = [(PRIORITY_LOW, 'Low'), (PRIORITY_MEDIUM, 'Medium'),
                        (PRIORITY_HIGH, 'High'), (PRIORITY_URGENT, 'Urgent')]
    TYPE_CHOICE = [('Q', 'Question'), ('P', 'Problem'), ('T', 'Task')]
    CATEGORY_CHOICE = [('python', 'Python'), ('django', 'Django'), ('sql', 'SQL'), ('postgresql', 'PostgreSQL'), ('oracle', 'Oracle'), ('mysql', 'MYSQL'),
                       ('javascript', 'Javascript'), ('java', 'Java'),  ('vuejs', 'VueJS'), ('html', 'HTML'), ('css', 'CSS'), ('unix', 'Unix'), ('shellscript', 'Shell Script'), ('other', 'Other')]
    status = django_filters.MultipleChoiceFilter(
        field_name='status', choices=STATUS_CHOICE, conjoined=True, widget=forms.CheckboxSelectMultiple)
    priority = django_filters.MultipleChoiceFilter(
        field_name='priority', choices=PRIORITY_CHOICES, conjoined=True, widget=forms.CheckboxSelectMultiple)
    ticket_type = django_filters.MultipleChoiceFilter(field_name='ticket_type', choices=TYPE_CHOICE, conjoined=True,
                                                      widget=forms.CheckboxSelectMultiple)
    category = django_filters.MultipleChoiceFilter(field_name='category', choices=CATEGORY_CHOICE, conjoined=True,
                                                   widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Question
        fields = ('status', 'priority', 'ticket_type',
                  'category',)
