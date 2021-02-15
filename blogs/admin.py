from django.contrib import admin

# Register your models here.
from .models import Post, Favorite, FileItem, FileTest
from django.contrib import messages
from .tasks import admin_post_send, admin_post_send_to_admin
from django.conf import settings
from django.contrib.sites.models import Site


def blog_approved(modeladmin, request, queryset):
    queryset.update(approved='Y')


blog_approved.short_description = "Mark selected blogs as approved"


def post_send_mail(modeladmin, request, queryset):
    qs = queryset

    for obj in qs:
        blog_name = obj.title
        blog_author = obj.author.first_name
        if not blog_author:
            blog_author = obj.author.username
        if settings.SITE_ID == 1:
            current_site = Site.objects.get_current()
            print(current_site)
            protocol = "https://"+str(current_site)+"/blog/"
            url = protocol + str(obj.slug)
            # print(url)
        else:
            current_site = Site.objects.get_current()
            protocol = "http://"+str(current_site)+"/blog/"
            url = protocol + str(obj.slug)
            # print(url)
        #print(blog_name,blog_author, url)
        admin_post_send.delay(blog_name, blog_author, url)
    # subject = f' Posted new Blogs'
    # body    = '''New Post has been posted by user !!!
    #             '''
    # email = 'tagnev.vengat@gmail.com'
    # send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,[email],fail_silently=False)
    pass


post_send_mail.short_description = "Send Email"


def post_admin_send_mail(modeladmin, request, queryset):
    qs = queryset

    for obj in qs:
        blog_name = obj.title
        blog_author = obj.author.first_name
        if not blog_author:
            blog_author = obj.author.username
        if settings.SITE_ID == 1:
            current_site = Site.objects.get_current()
            print(current_site)
            protocol = "https://www."+str(current_site)+"/blog/"
            url = protocol + str(obj.slug)
            # print(url)
        else:
            current_site = Site.objects.get_current()
            protocol = "http://"+str(current_site)+"/blog/"
            url = protocol + str(obj.slug)
            # print(url)
        #print(blog_name,blog_author, url)
        admin_post_send_to_admin.delay(blog_name, blog_author, url)
    # subject = f' Posted new Blogs'
    # body    = '''New Post has been posted by user !!!
    #             '''
    # email = 'tagnev.vengat@gmail.com'
    # send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,[email],fail_silently=False)
    pass


post_admin_send_mail.short_description = "Admin Send Email"


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'approved',
        'publish',
        'blog_image',
        'date_posted']
    search_fields = ['title']

    actions = [blog_approved, post_send_mail, post_admin_send_mail]


admin.site.register(Post, PostAdmin)
admin.site.register(Favorite)
admin.site.register(FileItem)
admin.site.register(FileTest)
