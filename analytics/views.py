from django.shortcuts import render
from django.views.generic.edit import CreateView
from . models import SuggestionFeedback, Contact
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from support.models import ReplyNotification
# Create your views here.


class SuggestionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SuggestionFeedback
    fields = ['email_id', 'content']
    success_url = '/'
    success_message = "Thanks for your Sugegstion. We will work on it accordingly!!!"

    def get_context_data(self, **kwargs):
        context = super(SuggestionCreateView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            notify_list = ReplyNotification.objects.filter(
                user=self.request.user).distinct()
            notify_list.update(read=True)
            context['notify_list'] = notify_list
        return context


class ContactCreateView(SuccessMessageMixin, CreateView):
    model = Contact
    fields = ['name', 'email', 'purpose', 'message']
    success_url = '/'
    success_message = "Thanks for contacting us! We will be in touch with you shortly."

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        # purpose = form.cleaned_data.get('purpose')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')
        purpose = form.cleaned_data['purpose']
        purpose = dict(form.fields['purpose'].choices)[purpose]
        # print(purpose)
        subject = f"{name} contacted for {purpose}"
        text_content = 'This is an important message.'
        html_content = render_to_string(
            'analytics/contact_email.html', {'contact_user': name, 'purpose': purpose,
                                             'message': message
                                             })
        email = "developerteckiy@gmail.com"
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email],
                                     )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return super(ContactCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContactCreateView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            notify_list = ReplyNotification.objects.filter(
                user=self.request.user).distinct()
            notify_list.update(read=True)
            context['notify_list'] = notify_list
        return context
