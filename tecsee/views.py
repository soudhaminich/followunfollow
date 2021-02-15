from django.shortcuts import render, get_object_or_404, redirect
from meta.views import Meta
from .models import TecseeVideo
from django.views.generic import View, ListView, TemplateView, DetailView, CreateView, UpdateView, FormView
from support.models import ReplyNotification
from comments.models import Comment
from comments.forms import CommentForm
from django.http import Http404
from analytics.mixins import ObjectViewedMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from .forms import S3DirectUploadForm
from django.urls import reverse
# Create your views here.


class Create(LoginRequiredMixin, CreateView):
    model = TecseeVideo
    form_class = S3DirectUploadForm
    template_name = 'tecsee/tecsee_create_new.html'    

    def get_success_url(self):
        return reverse('tecsee:detail', args=(self.object.slug,))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def detail(request, pk):
    media = get_object_or_404(TecseeVideo, pk=pk)
    context = {
        'media': media
    }
    return render(request, 'tecsee/tekvideo_detail.html', context)

class MyView(FormView):
    template_name = 'tecsee/tecsee_create.html'
    form_class = S3DirectUploadForm

def storeUrl(request):
    image_url = request.POST.get('img_url')
    video_url = request.POST.get('vid_url')

    TecseeVideo.objects.create(image=image_url,video=video_url,user=request.user)

    return redirect('tecsee:all-videos')

def tecsee_list(request):
    return render(request, 'tecsee/tekvideolist.html', {})


class TecseeListView(ListView):
    template_name = 'tecsee/tekvideolist.html'
    queryset = TecseeVideo.objects.filter(
        approved='Y').order_by('-created_date')
    paginate_by = 25

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context

        context = super(TecseeListView, self).get_context_data(**kwargs)
        project_title = 'Tecsee- New Trend in Learning Videos'
        if self.request.user.is_authenticated:
            project_title = 'Tecsee- New Trend in Learning Videos'
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


class TecseeDetailView(ObjectViewedMixin,DetailView):
    # model = Post
    template_name = 'tecsee/tekvideo_detail.html'

    # def get_queryset(self):
    #     qs = super(QuestionDetailView, self).get_queryset().filter()
    #     return qs.filter(approved='Y')

    def get_object(self, *args, **kwargs):
        request = self.request
        # print(request.session)
        slug = self.kwargs.get('slug')
        # print(slug)
        instance = get_object_or_404(TecseeVideo, slug=slug)
        if instance.approved == 'N':
            if instance.user == request.user:
                # instance = Question.objects.get(slug=slug)

                if instance is None:
                    raise Http404("Video Doesnt Exists")
                return instance
            else:
                raise Http404()
        else:
            if instance is None:
                raise Http404("Video Doesnt Exists")
            return instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # favorite = Favorite.objects.filter(add_favorite=True)
        form = CommentForm(self.request.POST or None)
        # ques_form = QuestionCommentForm(self.request.POST or None)
        reply_form = CommentForm(self.request.POST or None)
        slug = self.kwargs['slug']
        obj_tecsee = TecseeVideo.objects.get_by_tecsee_id(slug)
        # question_comment = QuestionComment.objects.filter(
        #     question=obj_question.id)

        # content_type = ContentType.objects.get_for_model(Question)
        # post_list = Post.objects.filter(id__gte=30,  approved='Y')

        # print(self.request.build_absolute_uri())
        from django.utils.html import strip_tags
        meta = Meta(
            # title="Teciky - Place for Techions",
            title='Tecsee Video - ' + obj_tecsee.title,
            image=obj_tecsee.image,
            image_width= "1200",
            image_height="600",
            image_type="image/jpeg",
            # description=strip_tags(obj_question.content),
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

        video_list = TecseeVideo.objects.exclude(id=obj_tecsee.id)
        # print(video_list)

        # context['meta'] = meta
        comment_obj = obj_tecsee.comments
        # try:
        #     answer_obj = Answer.objects.get(question=obj_question)
        # except Exception as e:
        #     answer_obj = None
        # print(comment_obj)
        context['form'] = form
        # context['reply_form'] = reply_form
        context['comment_obj'] = comment_obj
        context['video_list'] =video_list
        # context['answer_obj'] = answer_obj
        # context['content_type'] = content_type
        # context['question_comment'] = question_comment
        # context['ques_form'] = ques_form

        # context['post_list'] = post_list

        return context
