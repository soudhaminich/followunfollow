from django.http import Http404
from .filters import QuestionFilter
from django.views.generic.base import TemplateResponseMixin
from .models import Order
from paypal.standard.forms import PayPalPaymentsForm
from django.views.generic.detail import BaseDetailView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuestionForm, QuestionCommentForm
from .models import Question, QuestionComment, Answer, ReplyNotification
from blogs.models import Post
from comments.models import Comment
from comments.forms import CommentForm
from django.views.generic import View, ListView, TemplateView, DetailView, CreateView, UpdateView, FormView
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from analytics.mixins import ObjectViewedMixin
from markdownx.utils import markdownify
from meta.views import Meta
from django.core.paginator import Paginator
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.http import JsonResponse
from users.models import UserAction
from analytics.models import ObjectViewed
# Create your views here.


def category(request):
    cat = request.get_host().split('.')[0]
    try:
        tickets = Question.objects.filter(
            category=cat.upper()
        )

        
        return HttpResponse('<h1>Hello to sgfsdg teckiy :)</h1>')
    except:
        return HttpResponseRedirect('http://www.localhost:8000/')
def static_route(request):
    return HttpResponse('<h1>Support teckiy :)</h1>')

class CustomIndex(TemplateView):
    template_name = 'support/notifcations.html'


class SubDomainIndex(TemplateView):
    template_name = 'support/question_list.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        title = 'subdomain tickets'

        # get subdomain and filter tickets
        subdomain = request.META['HTTP_HOST'].split('.', 1)[0]
        print(subdomain)
        tickets = Question.objects.filter(
            category=subdomain[0].upper()
        )
        return HttpResponse('<h1>Hi Sub domian</h1>')
        # context.update({
        #     'tickets': tickets,
        #     'title': title
        # })
        # return self.render_to_response(context)


@login_required
def sub_question(request):
    form = QuestionForm()
    context = {
        'form': form
    }
    return render(request, 'support/question_create.html', context)


class PayTicket(LoginRequiredMixin, BaseDetailView, TemplateResponseMixin):
    model = Question
    template_name = 'support/pay.html'
    slug_field = 'slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if self.object.priority == Question.PRIORITY_HIGH_PENDING:
            price = '5.00'
            status = 'high'
        elif self.object.priority == Question.PRIORITY_URGENT_PENDING:
            price = '10.00'
            status = 'urgent'
        else:
            return redirect(self.object.get_absolute_url())

        Order.objects.filter(question=self.object,
                             payment_id__isnull=True).delete()
        order = Order(question=self.object, amount=price)
        order.save()

        paypal_dict = {
            "business": settings.PAYPAL_ACCOUNT,
            "amount": price,
            "item_name": "payment for {} ticket".format(status),
            "invoice": '{}{}'.format(settings.PAYPAL_PREFIX, order.pk),
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('support:detail', args=(self.object.slug,))),
            "cancel_return": request.build_absolute_uri(reverse('support:detail', args=(self.object.slug,))),
        }

        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        context.update({
            "form": form,
            "status": status,
            "price": price,
        })

        return self.render_to_response(context)


class CreateQuestion(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Question
    # fields = ['title', 'content', 'category', 'priority']
    form_class = QuestionForm
    template_name = 'support/question_create.html'
    # success_url = '/support/'
    success_message = "Question has been successfully submitted and published !!!"

    def get_success_url(self):
        # print(self.object.priority)
        if self.object.priority in [Question.PRIORITY_HIGH_PENDING,
                                    Question.PRIORITY_URGENT_PENDING]:
            self.success_message = "Question has been successfully submitted but not published yet. If payment is done then sometime it would take sometime to reflect.!!!"
            return reverse('support:ticket_pay', args=(self.object.slug,))
        return reverse('support:detail', args=(self.object.slug,))

    # def get_success_url(self):
    #     if self.object.priority in [Ticket.PRIORITY_HIGH_PENDING,
    #                                 Ticket.PRIORITY_URGENT_PENDING]:
    #         return reverse('ticket_pay', args=(self.object.slug,))
    #     return reverse('ticket_detail', args=(self.object.slug,))

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user

        ticket_paid = self.object.orders.filter(
            payment_id__isnull=False).exists()
        if not ticket_paid:
            if self.object.priority == Question.PRIORITY_HIGH:
                self.object.priority = Question.PRIORITY_HIGH_PENDING
                self.object.approved = 'N'

            elif self.object.priority == Question.PRIORITY_URGENT:
                self.object.priority = Question.PRIORITY_URGENT_PENDING
                self.object.approved = 'N'

        # if self.object.priority == Question.PRIORITY_HIGH:
        #     self.object.priority = Question.PRIORITY_HIGH_PENDING
        #     # added this line for approval
        #     self.object.approved = 'N'

        # elif self.object.priority == Question.PRIORITY_URGENT:
        #     self.object.priority = Question.PRIORITY_URGENT_PENDING
        #     self.object.approved = 'N'

        else:
            self.object.approved = 'Y'
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateQuestion, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            notify_list = ReplyNotification.objects.filter(
                user=self.request.user).distinct()
            notify_list.update(read=True)
            context['notify_list'] = notify_list
        return context


class UpdateQuestion(CreateQuestion, UpdateView):

    # def get_object(self):
    #     check_closed = Question.objects.get(slug=self.request.GET.get('slug'))
    #     if check_closed.status != 'C':
    #         return Question.objects.get(slug=self.request.GET.get('slug'))
    #     return Question.objects.get(slug=self.request.GET.get('slug'))
    def get_queryset(self):
        base_qs = super(UpdateQuestion, self).get_queryset()
        from django.db.models import Q
        base_qs= base_qs.filter(~Q(status='C'))
        return base_qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UpdateQuestion, self).get_context_data(**kwargs)
        print('update ', context['object'].status)        
        if self.request.user.is_authenticated:
            notify_list = ReplyNotification.objects.filter(
                user=self.request.user).distinct()
            notify_list.update(read=True)
            context['notify_list'] = notify_list
        return context


        
# class QuestionListView(ListView):
#     template_name = 'support/question_list.html'
#     # queryset = Question.objects.filter(approved='Y')
#     context_object_name = "question_list"
#     # paginate_by = 1

#     def get_queryset(self):
#         queryset = Question.objects.filter(approved='Y')

#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         meta = Meta(
#             # title="Teciky - Place for Techions",
#             title='Teckiy - Place for Techions',
#             image='https://static.teckiy.com/teckiy_200.jpg',
#             description="Teckiy - Learn & Share our knowledge,automations,queries related to technology programming languages,educations, etc. Our Goal to support all levels of developers when they need an third eye for his/her code. We are here to support them when they get stuck on their code. Also we are helping our developer community to fix the issue whenever they need any help/sugestions from techions.",
#             url=self.request.build_absolute_uri(),
#             keywords=['python', 'django', 'developer', 'support'],
#             author="Teckiy",
#             use_title_tag=True,
#             use_facebook=True,
#             use_og=True,
#             type='website',
#             fb=2529807007335836,
#             extra_props={
#                 'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
#             },
#             extra_custom_props=[
#                 ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
#             ]

#         )
#         context = {
#             'meta': meta
#         }
#         return context


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            template_name = 'index.html'
            return render(request, 'index.html')
        else:
            return redirect("support:question")


class QuestionListView(ListView):
    # template_name = 'support/question_list.html'
    queryset = Question.objects.filter(approved='Y').order_by('-date_posted')
    paginate_by = 25

    def get_filter_args(self):
        request = self.request
        filter_args = {}
        # filter_args['priority'] = request.GET.get('priority')
        # filter_args['ticket_type'] = request.GET.get('ticket_type')
        # filter_args['category'] = request.GET.get('category')
        # filter_args['status'] = request.GET.getlist('status')
        # print(filter_args['status'])
        # print(filter_args)
        # To remove filter arg if the value is null. to avoid errors
        filter_args = {key: value
                       for key, value in filter_args.items() if value}
        # print('first ', filter_args)
        return filter_args

    def get_queryset(self):
        filter_args = self.get_filter_args()
        status = self.request.GET.getlist('status')
        priority = self.request.GET.getlist('priority')
        ticket_type = self.request.GET.getlist('ticket_type')
        category = self.request.GET.getlist('category')
        queryset = super().get_queryset().filter(**filter_args)
        if status:
            queryset = queryset.filter(status__in=status)
        if priority:
            queryset = queryset.filter(priority__in=priority)
        if ticket_type:
            queryset = queryset.filter(ticket_type__in=ticket_type)
        if category:
            queryset = queryset.filter(category__in=category)
        return queryset

    def get_template_names(self):
        if self.request.user.is_authenticated:  # a certain check
            return ['support/question_list.html']
        else:
            return ['index.html']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context

        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['filter'] = QuestionFilter(
            self.request.GET, queryset=self.get_queryset())
        project_title = 'Teckiy - Community to Learn & Earn'
        if self.request.user.is_authenticated:
            project_title = 'Teckiy - Where Techions Learn & Earn'
        meta = Meta(
            # title="Teciky - Place for Techions",
            title=project_title,
            # image='https://static.teckiy.com/teckiy_200.jpg',
            image='https://static.teckiy.com/teckiy_logo_fav.jpg',
            description="Teckiy | Online Community for Techions",
            url=self.request.build_absolute_uri(),
            keywords=['python', 'django', 'developer', 'support'],
            author="Teckiy",
            use_title_tag=True,
            use_facebook=True,
            use_og=True,
            type='website',
            fb=2529807007335836,
            extra_props={
                'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
            },
            extra_custom_props=[
                ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
            ]

        )
        from django.contrib.contenttypes.models import ContentType
        # ctype = ContentType.objects.get_for_model('Question')
        # context['objectviewed'] = ObjectViewed.objects.filter(
        #     content_type=ctype)
        context['meta'] = meta
        if self.request.user.is_authenticated:
            notify_list = ReplyNotification.objects.filter(
                user=self.request.user).distinct()
            notify_list.update(read=True)

            context['notify_list'] = notify_list

        return context


class QuestionListAllView(ListView):
    template_name = 'support/question_list.html'
    queryset = Question.objects.filter(approved='Y').order_by('-date_posted')
    paginate_by = 25

    def get_filter_args(self):
        request = self.request
        filter_args = {}
        # filter_args['priority'] = request.GET.get('priority')
        # filter_args['ticket_type'] = request.GET.get('ticket_type')
        # filter_args['category'] = request.GET.get('category')
        # filter_args['status'] = request.GET.getlist('status')
        # print(filter_args['status'])
        # print(filter_args)
        # To remove filter arg if the value is null. to avoid errors
        filter_args = {key: value
                       for key, value in filter_args.items() if value}
        # print('first ', filter_args)
        return filter_args

    def get_queryset(self):
        filter_args = self.get_filter_args()
        status = self.request.GET.getlist('status')
        priority = self.request.GET.getlist('priority')
        ticket_type = self.request.GET.getlist('ticket_type')
        category = self.request.GET.getlist('category')
        queryset = super().get_queryset().filter(**filter_args)
        if status:
            queryset = queryset.filter(status__in=status)
        if priority:
            queryset = queryset.filter(priority__in=priority)
        if ticket_type:
            queryset = queryset.filter(ticket_type__in=ticket_type)
        if category:
            queryset = queryset.filter(category__in=category)
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(QuestionListAllView, self).get_context_data(**kwargs)
        context['filter'] = QuestionFilter(
            self.request.GET, queryset=self.get_queryset())
        meta = Meta(
            # title="Teciky - Place for Techions",
            title='Teckiy - Where Techions Learn & Earn',
            image='https://static.teckiy.com/teckiy_logo_fav.jpg',
            description="Teckiy | Online Community for Techions",
            url=self.request.build_absolute_uri(),
            keywords=['python', 'django', 'developer', 'support'],
            author="Teckiy",
            use_title_tag=True,
            use_facebook=True,
            use_og=True,
            type='website',
            fb=2529807007335836,
            extra_props={
                'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
            },
            extra_custom_props=[
                ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
            ]

        )
        context['meta'] = meta

        return context


def question(request):
    object_list = Question.objects.filter(approved='Y')
    meta = Meta(
        # title="Teciky - Place for Techions",
        title='Teckiy - Where Techions Learn & Earn',
        image='https://static.teckiy.com/teckiy_200.jpg',
        description="Teckiy | Online Community for Techions",
        url=request.build_absolute_uri(),
        keywords=['python', 'django', 'developer', 'support'],
        author="Teckiy",
        use_title_tag=True,
        use_facebook=True,
        use_og=True,
        type='website',
        fb=2529807007335836,
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
        },
        extra_custom_props=[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]

    )
    context = {
        'object_list': object_list,
        'meta': meta
    }
    return render(request, 'support/question_list.html', context)


def question_update(request, slug=None):
    instance = Question.objects.get(slug=slug)
    if instance:
        instance.status = 'C'
        instance.save()
        messages.success(
            request, ('Ticket has been closed as per your request'))
        return redirect('support:detail', instance.slug)

# ObjectViewedMixin


class QuestionDetailView(ObjectViewedMixin, DetailView):
    # model = Post
    template_name = 'support/question_detail.html'

    # def get_queryset(self):
    #     qs = super(QuestionDetailView, self).get_queryset().filter()
    #     return qs.filter(approved='Y')

    def get_object(self, *args, **kwargs):
        request = self.request
        # print(request.session)
        slug = self.kwargs.get('slug')
        # print(slug)
        instance = get_object_or_404(Question, slug=slug)
        if instance.approved == 'N':
            if instance.user == request.user:
                # instance = Question.objects.get(slug=slug)

                if instance is None:
                    raise Http404("Question Doesnt Exists")
                return instance
            else:
                raise Http404()
        else:
            if instance is None:
                raise Http404("Question Doesnt Exists")
            return instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # favorite = Favorite.objects.filter(add_favorite=True)
        form = CommentForm(self.request.POST or None)
        ques_form = QuestionCommentForm(self.request.POST or None)
        reply_form = CommentForm(self.request.POST or None)
        slug = self.kwargs['slug']
        obj_question = Question.objects.get_by_question_id(slug)
        question_comment = QuestionComment.objects.filter(
            question=obj_question.id)

        content_type = ContentType.objects.get_for_model(Question)
        post_list = Post.objects.filter(id__gte=30,  approved='Y')

        # print(self.request.build_absolute_uri())
        from django.utils.html import strip_tags
        meta = Meta(
            # title="Teciky - Place for Techions",
            title='Teckiy - ' + obj_question.title,
            image='https://static.teckiy.com/teckiy_logo_fav.jpg',
            description=strip_tags(obj_question.content),
            url=self.request.build_absolute_uri(),
            keywords=['python', 'django', 'developer', 'support'],
            author="Teckiy",
            use_title_tag=True,
            use_facebook=True,
            use_og=True,
            type='website',
            fb=2529807007335836,
            extra_props={
                'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
            },
            extra_custom_props=[
                ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
            ]

        )
        context['meta'] = meta
        if self.request.user.is_authenticated:
            notify_list = ReplyNotification.objects.filter(
                user=self.request.user).distinct()
            notify_list.update(read=True)
            context['notify_list'] = notify_list

        # print(obj_question)

        # context['meta'] = meta
        comment_obj = obj_question.comments
        try:
            answer_obj = Answer.objects.filter(question=obj_question)
            print('answer_obj ', answer_obj)
        except Exception as e:
            answer_obj = None
        # print(comment_obj)
        context['form'] = form
        context['reply_form'] = reply_form
        context['comment_obj'] = comment_obj
        context['answer_obj'] = answer_obj
        context['content_type'] = content_type
        context['question_comment'] = question_comment
        context['ques_form'] = ques_form

        context['post_list'] = post_list

        return context


@login_required
def question_comment_delete(request, ques_comm_id=None):
    try:
        delete_comment_ques = QuestionComment.objects.get(id=ques_comm_id)
        ques_instance = Question.objects.get(
            id=delete_comment_ques.question.id)
        delete_comment_ques.delete()
        return redirect('support:detail', ques_instance.slug)
    except Exception as e:
        print(e, 'Something went wrong')
        messages.error(
            request, f'Something went wrong')
        return redirect('/')


@login_required
def question_comment_edit(request, ques_comm_id=None):
    if request.method == 'POST':
        try:
            update_content = request.POST.get('content')
            com_instance = QuestionComment.objects.filter(
                id=ques_comm_id).update(content=update_content, edited=True)
            question_instance = QuestionComment.objects.get(id=ques_comm_id)
            return redirect('support:detail', question_instance.question.slug)
        except Exception as e:
            print(e, 'Something went wrong')
            messages.error(
                request, f'Something went wrong')
            return redirect('/')


@login_required
def question_comment(request, object_id=None):
    if request.method == 'POST':
        form = QuestionCommentForm(request.POST)
        if form.is_valid():
            # print('Yes working')
            instance = form.save(commit=False)
            instance.user = request.user  # Set the user object here

            question_instance = Question.objects.get(id=object_id)
            instance.question = question_instance
            if question_instance.status == 'O':
                question_instance.status = 'I'
                question_instance.save()
            instance.save()
            comment_slug = Question.objects.get_by_question_id(
                question_instance.slug)
            commented_user = request.user.username
            question_user_email = comment_slug.user.email
            question_url = comment_slug.get_absolute_url()
            question_title = comment_slug.title
            ticket_id = comment_slug.id
            subject = f'Teckiy New message from {commented_user} -   {question_title} #Ticket{ticket_id}'

            email = question_user_email
            bcc_email = settings.ADMIN_EMAIL
            if settings.DEBUG:
                domain = 'http://localhost:8000'
            else:
                domain = 'https://www.teckiy.com'

            text_content = 'This is an important message.'
            html_content = render_to_string(
                'support/question_clarify.html', {'commented_user': commented_user,
                                                  'domain': domain, 'question_url': question_url, 'to_user': comment_slug.user.username})

            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email],
                                         bcc=[bcc_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect('support:detail', comment_slug.slug)
        else:
            question_instance = Question.objects.get(id=object_id)            
            messages.error(request, 'Message should not be empty!')
            return redirect('support:detail', question_instance.slug)

    return redirect('support:question')


@login_required
def comment_edit(request, object_id=None, question_id=None):
    instance = get_object_or_404(Comment, id=object_id)
    user_instance = instance.user
    # print(user_instance)
    # try:
    # question_instance = Question.objects.get(id=question_id)
    question_detail = Question.objects.get(id=question_id)
    if request.user.username == user_instance.username:
        if request.method == 'POST':
            form = CommentForm(request.POST or None, instance=instance)
            if form.is_valid():
                print('valid')
                form.save()
                question_instance = Question.objects.get(id=question_id)
                return redirect('support:detail', question_instance.slug)
            else:
                print('form ', form)
                question_instance = Question.objects.get(id=question_id)            
                messages.error(request, 'Message should not be empty!')
                return render(request, 'support/question_answer_edit.html', {'form': form, 'question': question_detail})
        else:
            form = CommentForm(request.POST or None, instance=instance)
        return render(request, 'support/question_answer_edit.html', {'form': form, 'question': question_detail})
    else:
        messages.info(request, 'You dont have access to edit the post!')
        return redirect('/')


class QuestionListFilterView(ListView):
    template_name = 'support/question_category_filter.html'
    queryset = Question.objects.filter(approved='Y')
    paginate_by = 15

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(QuestionListFilterView,
                        self).get_context_data(**kwargs)
        meta = Meta(
            # title="Teciky - Place for Techions",
            title='Teckiy - Where Techions Learn & Earn',
            image='https://static.teckiy.com/teckiy_200.jpg',
            description="Teckiy | Online Community for Techions",
            url=self.request.build_absolute_uri(),
            keywords=['python', 'django', 'developer', 'support'],
            author="Teckiy",
            use_title_tag=True,
            use_facebook=True,
            use_og=True,
            type='website',
            fb=2529807007335836,
            extra_props={
                'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
            },
            extra_custom_props=[
                ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
            ]

        )
        context['meta'] = meta
        return context


@login_required
def answer_verified(request, comment_id=None, question_id=None):
    # print(comment_id.split(),question_id)
    total_comments = comment_id.split(',')
    print(total_comments)
    try:
        question_instance = get_object_or_404(Question, id=question_id)
        question_instance.status = 'C'
        question_instance.save()
        for comment in total_comments:
            comment_instance = get_object_or_404(Comment, id=int(comment))
            print(comment_instance)
            answer_instance_create = Answer.objects.update_or_create(
                comment=comment_instance, question=question_instance,
                verified=True
            )
        # print(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # instance = get_object_or_404(Comment, id=object_id)
    # user_instance = instance.user

    # question_detail = Question.objects.get(id=question_id)
    # if request.user.username == user_instance.username:
    #     form = CommentForm(request.POST or None, instance=instance)
    #     if form.is_valid():
    #         form.save()
    #         question_instance = Question.objects.get(id=question_id)
    #         return redirect('support:detail', question_instance.slug)
    #     return render(request, 'support/question_answer_edit.html', {'form': form, 'question': question_detail})
    # else:
    #     messages.info(request, 'You dont have access to edit the post!')
    #     return redirect('/')


@login_required
def vote_comment(request, comment_id=None, vote_type=None):
    if request.user.is_authenticated:
        comment_instance = Comment.objects.get(
            id=comment_id)
        try:
            usercount = UserAction.objects.filter(
                comment=comment_instance, user__username=request.user.username)
            use_obj = UserAction.objects.get(
                comment=comment_instance, user__username=request.user.username)

            # print(up_vote_count)
        except UserAction.DoesNotExist:
            print('Doesnt exists')
        if vote_type == 'up':

            if usercount.count() == 0:
                upvote = UserAction.objects.update_or_create(
                    user=request.user, vote=1, vote_type='U', comment=comment_instance)
                # up_vote_count = usercount
                up_vote_count = UserAction.objects.filter(
                    comment=comment_instance, vote_type='U').count()
                down_vote_count = UserAction.objects.filter(
                    comment=comment_instance, vote_type='D').count()
                total_count = up_vote_count
                data = {'total_up_count': up_vote_count,
                        'total_down_count': down_vote_count}
                return JsonResponse(data)
            elif usercount.count() == 1 and use_obj.vote_type == 'D':
                print('Checking')
                downvote = UserAction.objects.filter(
                    user=request.user,  comment=comment_instance).update(vote=1, vote_type='U')
                up_vote_count = UserAction.objects.filter(
                    comment=comment_instance, vote_type='U').count()
                down_vote_count = UserAction.objects.filter(
                    comment=comment_instance, vote_type='D').count()
                total_count = up_vote_count
                data = {'total_up_count': up_vote_count,
                        'total_down_count': down_vote_count}
                return JsonResponse(data)
            else:
                data = {'Sucsess': 'Vote already updated'}
                return JsonResponse(data)
        elif vote_type == 'down':

            if usercount.count() == 0:
                downvote = UserAction.objects.update_or_create(
                    user=request.user, vote=-1, vote_type='D', comment=comment_instance)
                up_vote_count = UserAction.objects.filter(
                    comment=comment_instance, vote_type='U').count()
                down_vote_count = UserAction.objects.filter(
                    comment=comment_instance, vote_type='D').count()
                total_count = up_vote_count
                data = {'total_up_count': up_vote_count,
                        'total_down_count': down_vote_count}
                return JsonResponse(data)
            elif usercount.count() == 1 and use_obj.vote_type == 'U':
                print('Checking')
                downvote = UserAction.objects.filter(
                    user=request.user,  comment=comment_instance).update(vote=-1, vote_type='D')
                up_vote_count = UserAction.objects.filter(
                    comment=comment_instance, vote_type='U').count()
                down_vote_count = UserAction.objects.filter(
                    comment=comment_instance, vote_type='D').count()
                total_count = up_vote_count
                data = {'total_up_count': up_vote_count,
                        'total_down_count': down_vote_count}
                return JsonResponse(data)
            else:
                data = {'Sucsess': 'Vote already updated'}
                return JsonResponse(data)


@login_required
def notification(request):
    # object_list = ReplyNotification.objects.filter(
    #     question__isnull=False).distinct()
    # object_list = object_list.filter(user=request.user)

    object_list = ReplyNotification.objects.filter(
        user=request.user).distinct()
    object_list.update(read=True)
    context = {}
    context['object_list'] = object_list
    return render(request, 'support/notifications.html', context)


@login_required
def notification_delete(request):
    ReplyNotification.objects.filter(
        user=request.user
    ).delete()
    return redirect('/')
