from django import template
from users.models import Profile
from support.models import ReplyNotification
from django.db.models import Count
register = template.Library()


@register.simple_tag
def paginate_url(field_name, value, urlencode=None):
    get_query = f'{field_name}={value}'
    if urlencode:
        qs = urlencode.split('&')
        _filtered = filter(lambda p: p.split('=')[0] != field_name, qs)
        querystring = '&'.join(_filtered)
        get_query = f'{get_query}&{querystring}'
    return get_query


@register.simple_tag
def display_name(object_user):
    if object_user:
        profile = Profile.objects.get(user=object_user)
        if profile.display_name:
            return profile.display_name
        return object_user.username


@register.simple_tag
def notify_count(object_user):
    if object_user:
        output_count = 0
        for out in ReplyNotification.objects.filter(
                user=object_user):
            if out.question:
                if out.user == out.author:
                    output_count += 1
            else:
                if out.user != out.author:
                    output_count += 1
        return output_count

        # nt_cnt = ReplyNotification.objects.filter(
        #     user=object_user, question__isnull=False).distinct()
        # if nt_cnt.count() > 0:
        #     return nt_cnt.count()


# {% display_name request obj.user  %}
