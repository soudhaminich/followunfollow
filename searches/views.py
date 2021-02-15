from django.shortcuts import render
from .models import SearchQuery
from blogs.models import Post
from support.models import Question
from itertools import chain
# Create your views here.

from django.views.generic import ListView


class SearchView(ListView):
    template_name = 'searches/view.html'
    # paginate_by = 1
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        print(query)
        if query is not None:
            # blog_results = Post.objects.search(query)
            question_results = Question.objects.search(query)
            # lesson_results      = Lesson.objects.search(query)
            # profile_results     = Profile.objects.search(query)

            # combine querysets
            queryset_chain = chain(
                # blog_results,
                question_results
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)  # since qs is actually a list
            # print(qs)
            return qs
        # empty_qs = Post.objects.none() or Question.objects.none()
        empty_qs = Question.objects.none()
        return empty_qs  # just an empty queryset as default


def search_query(request):
    query = request.GET.get('q', None)
    # print(query)
    user = None
    if request.user.is_authenticated:
        user = request.user
    context = {
        'query': query
    }
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        blog_list = Post.objects.search(query=query)
        blog_list = blog_list.distinct()
        # print(blog_list)
        context['blog_list'] = blog_list
        # print(context)
    return render(request, 'searches/view.html', context)
