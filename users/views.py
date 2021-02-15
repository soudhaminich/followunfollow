from support.models import ReplyNotification
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from .models import Techion
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import UserRegisterForm, ForgotPassword, PasswordReset
from django.contrib import messages
from django.views.generic import CreateView, DetailView, View
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from .forms import UserUpdateForm, ProfileUpdateForm, FollowForm
from blogs.models import Post
from .models import Profile, UserFollower
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.conf import settings
from django.core.mail import send_mail

from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from support.models import Question
from meta.views import Meta
from comments.models import Comment
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = Site.objects.get_current()
            print(current_site.domain)
            # current_site.domain='blogs.virtual2buy.in'
            if settings.SITE_ID == 1:
                mail_subject = 'Activate your blog account.'
                message = render_to_string('users/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                print(settings.DEFAULT_FROM_EMAIL)
                send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [
                          to_email], fail_silently=False)
                # email = EmailMessage(
                #             mail_subject, message, to=[to_email]
                # )
                # email.send()
                messages.success(
                    request, 'Please confirm your email address to complete the registration')
                return redirect('login')
            else:

                mail_subject = 'Activate your blog account.'
                message = render_to_string('users/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                print(settings.DEFAULT_FROM_EMAIL)
                send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [
                          to_email], fail_silently=False)
                # email = EmailMessage(
                #             mail_subject, message, to=[to_email]
                # )
                # email.send()
                messages.success(
                    request, 'Please confirm your email address to complete the registration')
                return redirect('login')

            # return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        messages.success(
            request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        messages.warning(request, 'Activation link is invalid!')
        return redirect('login')
        # return HttpResponse('Activation link is invalid!')


def register_old(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            g = Group.objects.get(name='Enduser')
            user1 = User.objects.get(username=username)
            g.user_set.add(user1)
            messages.success(
                request, f'Account has been created for {username}')
            subject = f'{username} account has been created'
            body = '''Account created. Please reach out to vengateswaran for any
                        issues !!!
                        '''
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                      [email], fail_silently=False)

            return redirect('login')
            # return HttpResponseRedirect(reverse('blogs:detail', args=[1]))
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# class RegisterView(SuccessMessageMixin, CreateView):

#     form_class = UserRegisterForm

#     success_url = reverse_lazy('login')
#     template_name = 'users/register.html'
#     success_message = "%(username)s account has been created! You are now able to log in"

    # def add_user(self):
    #    g = Group.objects.get(name='Enduser')
    #    user = User.objects.get(username=username)
    #    g.user_set.add(user)
    #    print(g)

    # def form_valid(self, form):
    #     # c = {'form': form, }
    #     # user = form.save(commit=False)
    #     # Cleaned(normalized) data
    #     username = form.cleaned_data['username']
    #     g = Group.objects.get(name='Enduser')
    #     user1 = User.objects.get(username=username)
    #     g.user_set.add(user1)

    # Create UserProfile model
    # UserProfile.objects.create(user=user, phone_number=phone_number, date_of_birth=date_of_birth)

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['username'] = request.POST.get('username')
    #     print(context)
    #     return context

def login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email, username)

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            return redirect('blogs:blog-home')
        else:
            messages.warning(
                request, "Please provide correct username & password")
    # else:
    #     messages.error(request,"Please provide correct username & password")
        # return render(request, 'users/login.html',{})

    return render(request, 'users/login.html', {})


def logout(request):
    logout(request)
    return HttpResponseRedirect('/')
    # print(dir(request.session.session_key))
    # try:
    #     del request.session['member_id']
    # except KeyError:
    #     pass
    # return HttpResponse("You're logged out.")


class ProfileView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        # u_form = UserUpdateForm(instance=self.request.user)
        print(args, kwargs)
        if self.request.user.username == kwargs['username']:
            p_form = ProfileUpdateForm(instance=self.request.user.profile)
            # test = Profile.objects.get_techion()
            meta = Meta(
                # title="Teciky - Place for Techions",
                title='Techion Edit Profile ' + str(kwargs['username']),
                keywords=['python', 'django', 'developer', 'support'],
                extra_props={
                    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
                },
                extra_custom_props=[
                    ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                ]

            )
            context = {
                # 'u_form': u_form,
                'p_form': p_form,
                'meta': meta
                # 'test': test
            }
            if self.request.user.is_authenticated:
                notify_list = ReplyNotification.objects.filter(
                    user=self.request.user).distinct()
                notify_list.update(read=True)
                context['notify_list'] = notify_list
            return render(self.request, 'users/edit_profile.html', context)
        else:
            return redirect('users:profile', username=self.request.user)

    def post(self, *args, **kwargs):
        print(args, kwargs)
        # u_form = UserUpdateForm(self.request.POST, instance=self.request.user)
        p_form = ProfileUpdateForm(self.request.POST,
                                   self.request.FILES,
                                   instance=self.request.user.profile)
        print(kwargs)

        try:
            if p_form.is_valid():
                # u_form.save()
                p_form.save()
                messages.success(
                    self.request, 'Your account has been updated!')
                return redirect('users:profile', username=self.request.user)
            else:
                if p_form['image'].errors:
                    messages.error(
                        self.request, 'Error in Image Upload ' + str(p_form['image'].errors.get_json_data()[0]['message']))
                    return redirect('users:edit', username=self.request.user)
                else:
                    error = ""
                    if p_form['fb_url'].errors:
                        error = error + 'Facebook URL is not Valid. Please enter valid URL \n'

                    if p_form['tw_url'].errors:
                        error = error + 'Twitter URL is not Valid. Please enter valid URL \n'

                    if p_form['lki_url'].errors:
                        error = error + 'LinkedIn URL is not Valid. Please enter valid URL'

                    messages.error(
                        self.request, error)
                    return redirect('users:edit', username=self.request.user)
        except Exception as e:
            messages.error(self.request, 'Something Went Wrong while update')
            return redirect('users:edit', username=self.request.user)

            # if u_form['username'].errors.as_data():
            #     messages.warning(
            #         self.request, u_form['username'].errors.get_json_data()[0]['message'])
            #     return redirect('users:profile', username=self.request.user)

        #     else:
        #         messages.warning(
        #             self.request, u_form['email'].errors.get_json_data()[0]['message'])
        #         return redirect('users:profile', username=self.request.user)
        # except Exception as e:
        #     # p_form['image'].errors.get_json_data()[0]['message']
        #     # print(p_form['image'].errors.as_data())
        #     messages.warning(
        #         self.request,  p_form['image'].errors.get_json_data())
        #     return redirect('users:profile', username=self.request.user)


class ViewUserProfile(LoginRequiredMixin, View):


    # model=Profile
    # template_name = 'users/profile-head.html'

    # def get_object(self,**kwargs):
    #     user_id = User.objects.get(username=kwargs['username'])
    #     # profile_instance = Profile.objects.get(user=user_id)
    #     # pk = self.kwargs.get('pk')
    #     view_profile = Profile.objects.get(user=user_id)
    #     return view_profile

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     view_profile = self.get_object()
    #     my_profile = Profile.objects.get(user=self.request.user)
    #     if view_profile.user  in my_profile.following.all():
    #         follow=True
    #     else:
    #         follow=False
    #     context["follow"]=follow
    #     return context
    



       
    def get(self, *args, **kwargs):
        user_id = User.objects.get(username=kwargs['username'])
        profile_instance = Profile.objects.get(user=user_id)
        # profile_instance = get_object_or_404(Profile, slug=kwargs['slug'])
        user_instance = get_object_or_404(
            User, id=profile_instance.user_id)
        ticket_instance = Question.objects.filter(
            user=user_instance).count()
        ticket_details = Question.objects.filter(
            user=user_instance)
        techion_points = Techion.objects.filter(
            profile=profile_instance).aggregate(Sum('points'))
        post_instance = Post.objects.filter(
            author=user_instance).order_by('-date_posted')
        # print(techion_points['points__sum'])
        # print(ticket_instance)
        print(post_instance)
        meta = Meta(
            # title="Teciky - Place for Techions",
            title='Techion Profile '+str(profile_instance.user),
            img=profile_instance.image.url,
            keywords=['python', 'django', 'developer', 'support'],
            extra_props={
                'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
            },
            extra_custom_props=[
                ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
            ]

        )
        context = {
            'profile': profile_instance,
            'user_instance': user_instance,
            'ticket_instance_count': ticket_instance,
            'ticket_details': ticket_details,
            'points': techion_points['points__sum'],
            'posts': post_instance,
            'meta': meta
        }

        if self.request.user.is_authenticated:
            notify_list = ReplyNotification.objects.filter(
                user=self.request.user).distinct()
            notify_list.update(read=True)
            context['notify_list'] = notify_list

        return render(self.request, 'users/profile-summary.html', context)
        # else:
        #     raise Http404("Page Not Found")


@login_required
def profilesummary(request, *args, **kwargs):
    user_id = User.objects.get(username=kwargs['username'])
    user_instance = get_object_or_404(
        User, id=user_id.id)
    profile_instance = Profile.objects.get(user=user_id)
    post_instance = Post.objects.filter(
        author=user_instance, approved='Y').order_by('-date_posted')
    ticket_details = Question.objects.filter(
        user=user_instance, approved='Y')
    content_type = ContentType.objects.get_for_model(Question)

    comment = Comment.objects.filter(
        content_type=content_type, user=user_instance).values('object_id').distinct().count()
    meta = Meta(
        # title="Teciky - Place for Techions",
        title='Techion Profile '+str(profile_instance.user),
        img=profile_instance.image.url,
        keywords=['python', 'django', 'developer', 'support'],
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
        },
        extra_custom_props=[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    )
   
    context = {}
    context['profile'] = profile_instance
    context['posts'] = post_instance
    context['tickets'] = ticket_details
    context['answered'] = comment
    context['meta'] = meta
    context['user_instance'] = user_instance
    if request.user.is_authenticated:
        notify_list = ReplyNotification.objects.filter(
            user=request.user).distinct()
        notify_list.update(read=True)
        context['notify_list'] = notify_list
    return render(request, 'users/profile-summary.html', context)


@ login_required
def profilepost(request, *args, **kwargs):
    user_id = User.objects.get(username=kwargs['username'])
    user_instance = get_object_or_404(
        User, id=user_id.id)
    profile_instance = Profile.objects.get(user=user_id)
    post_instance = Post.objects.filter(
        author=user_instance).order_by('-date_posted')
    meta = Meta(
        # title="Teciky - Place for Techions",
        title='Techion Profile '+str(profile_instance.user),
        img=profile_instance.image.url,
        keywords=['python', 'django', 'developer', 'support'],
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
        },
        extra_custom_props=[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    )
    context = {}
    context['profile'] = profile_instance
    context['posts'] = post_instance
    context['meta'] = meta
    context['user_instance'] = user_instance

    if request.user.is_authenticated:
        notify_list = ReplyNotification.objects.filter(
            user=request.user).distinct()
        notify_list.update(read=True)
        context['notify_list'] = notify_list
    return render(request, 'users/profile-posts.html', context)


@ login_required
def profileticket(request, *args, **kwargs):
    user_id = User.objects.get(username=kwargs['username'])
    user_instance = get_object_or_404(
        User, id=user_id.id)
    profile_instance = Profile.objects.get(user=user_id)
    if request.user.username == kwargs['username']:
        ticket_details = Question.objects.filter(
            user=user_instance)
    else:
        ticket_details = Question.objects.filter(
            user=user_instance, approved='Y')
    meta = Meta(
        # title="Teciky - Place for Techions",
        title='Techion Profile '+str(profile_instance.user),
        img=profile_instance.image.url,
        keywords=['python', 'django', 'developer', 'support'],
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
        },
        extra_custom_props=[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    )
    context = {}
    context['profile'] = profile_instance
    context['ticket_details'] = ticket_details
    context['meta'] = meta
    context['user_instance'] = user_instance

    if request.user.is_authenticated:
        notify_list = ReplyNotification.objects.filter(
            user=request.user).distinct()
        notify_list.update(read=True)
        context['notify_list'] = notify_list
    return render(request, 'users/profile-ticket.html', context)


@ login_required
def profiletechion(request, *args, **kwargs):
    user_id = User.objects.get(username=kwargs['username'])
    user_instance = get_object_or_404(
        User, id=user_id.id)
    profile_instance = Profile.objects.get(user=user_id)
    ticket_details = Question.objects.filter(
        user=user_instance, approved='Y')
    techion_points = Techion.objects.filter(
        profile=profile_instance).aggregate(Sum('points'))
    meta = Meta(
        # title="Teciky - Place for Techions",
        title='Techion Profile '+str(profile_instance.user),
        img=profile_instance.image.url,
        keywords=['python', 'django', 'developer', 'support'],
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
        },
        extra_custom_props=[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    )
    context = {}
    context['profile'] = profile_instance
    context['points'] = techion_points['points__sum']
    context['meta'] = meta
    context['user_instance'] = user_instance

    if request.user.is_authenticated:
        notify_list = ReplyNotification.objects.filter(
            user=request.user).distinct()
        notify_list.update(read=True)
        context['notify_list'] = notify_list
    return render(request, 'users/profile-techion.html', context)


def forgot_password(request):
    form = PasswordReset()
    return render(request, 'users/registration/password_reset_form.html', {'form': form})


from .models import Profile
def follow_unfollow_profile(request):
    if request.method == "POST":
     my_profile = Profile.objects.get(user=request.user)
    #  user_id = User.objects.get(username=kwargs['username'])
    #     profile_instance = Profile.objects.get(user=user_id)
     pk = request.POST.get('profile_pk')
     obj=Profile.objects.get(pk=pk)

     if obj.user in my_profile.following.all():
        my_profile.following.remove(obj.user)
     else:
        my_profile.following.add(obj.user)
        # return redirect('users:profile-summary')
     return redirect(request.META.get('HTTP_REFERER'))
    return redirect('users:profile-summary')
    
# def follow_unfollow_profile(request):
#     if request.method=="POST":
#         my_profile=Profile.objects.get(user=request.user)
#         pk=request.POST.get('profile_pk')
#         obj=Profile.objects.get(pk=pk)

#         if obj.user in my_profile.following.all():
#             my_profile.following.remove(obj.user)
#         else:
#             my_profile.following.add(obj.user)
#         return redirect(request.META.get('HTTP_REFERER'))
#     return redirect('users: profile-summary.html')
    # return redirect('profiles:profile-list-view')

from tecsee.models import TecseeVideo

@ login_required
def profilevideos(request, *args, **kwargs):
    user_id = User.objects.get(username=kwargs['username'])
    user_instance = get_object_or_404(
        User, id=user_id.id)
    profile_instance = Profile.objects.get(user=user_id)
    if request.user.username == kwargs['username']:
        video_details = TecseeVideo.objects.filter(
            user=user_instance)
    else:
        video_details = TecseeVideo.objects.filter(
            user=user_instance, approved='Y')
    meta = Meta(
        # title="Teciky - Place for Techions",
        title='Techion Profile '+str(profile_instance.user),
        img=profile_instance.image.url,
        keywords=['python', 'django', 'developer', 'support'],
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
        },
        extra_custom_props=[
            ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
        ]
    )
    context = {}
    context['profile'] = profile_instance
    context['video_details'] = video_details
    context['meta'] = meta
    context['user_instance'] = user_instance

    if request.user.is_authenticated:
        notify_list = ReplyNotification.objects.filter(
            user=request.user).distinct()
        notify_list.update(read=True)
        context['notify_list'] = notify_list
    return render(request, 'users/profile-videos.html', context)



# class ProfileDetailView(DetailView):
#     model=Profile
#     template_name = 'users/profile-head.html'

#     def get_object(self,**kwargs):
#         pk = self.kwargs.get('pk')
#         view_profile = Profile.objects.get(pk=pk)
#         return view_profile

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         view_profile = self.get_object()
#         my_profile = Profile.objects.get(user=self.request.user)
#         if view_profile.user  in my_profile.following.all():
#             follow=True
#         else:
#             follow=False
#         context["follow"]=follow
#         return context
