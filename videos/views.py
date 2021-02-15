from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from . models import Course, PartCourse
from comments.forms import CommentForm
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from meta.views import Meta
from orders.models import Order
import json
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
# Create your views here.


class CourseListView(ListView):
    model = Course
    queryset = Course.objects.all()


class CourseDetailView(LoginRequiredMixin, MultipleObjectMixin, DetailView):
    model = Course
    queryset = Course.objects.filter(published=True)
    paginate_by = 1

    def get_context_data(self, **kwargs):

        object_list = PartCourse.objects.filter(course=self.get_object())

        context = super(CourseDetailView, self).get_context_data(
            object_list=object_list,  **kwargs)
        obj = context['object']
        print(obj.slug)

        # print(obj.course_image)
        # print(obj.description)
        # order_detail = Order.objects.get(
        #     course=object)
        order_obj = ''
        try:
            order_obj = Order.objects.get(
                course=obj, customer=self.request.user)
        except Exception as e:
            print(e)
        meta = Meta(
            # title="Teciky - Place for Techions",
            title=obj.name,
            img=obj.course_image.url,
            description=obj.description,
            keywords=['python', 'django', 'developer', 'support'],
            extra_props={
                'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
            },
            extra_custom_props=[
                ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
            ]

        )
        comment_obj = ''
        context['meta'] = meta
        context['order_obj'] = order_obj
        context['comment_obj'] = comment_obj
        return context


@login_required
def checkout(request, slug, *args, **kwargs):
    course_object = Course.objects.get(slug=slug)
    context = {
        'course_object': course_object
    }
    return render(request, 'videos/checkout.html', context)


@login_required
def process_order(request):
    data = json.loads(request.body)
    print(data)
    if data['payment'] == 'Done':
        if request.user.is_authenticated:
            customer = request.user
            course_object = get_object_or_404(Course, slug=data['course_slug'])
            response = {}
            try:
                order = Order.objects.get(
                    customer=customer, course=course_object)
                if order:
                    order.payment = True
                    order.save()
                    response['Output'] = 'Existing Order Updated the payment Successfully'
                    return JsonResponse(response, safe=False)
            except Exception as e:
                Order.objects.create(
                    customer=customer, payment=True, course=course_object)
                response['Output'] = 'New Order created Successfully'
                return JsonResponse(response, safe=False)
    return JsonResponse('Something went wrong')


class PartDetailView(LoginRequiredMixin, MultipleObjectMixin, DetailView):
    model = PartCourse


def partdetailview(request,  course, slug):
    context = {}
    part_object = get_object_or_404(PartCourse, slug=slug)
    course_object = get_object_or_404(Course, slug=course)

    try:
        next_part = PartCourse.objects.get(
            course=course_object, part_num=part_object.part_num + 1)

        # next_part = next_part_object.part_num + 1

    except Exception as e:
        print(e)
        next_part = 1

    # print(part_object)
    # print(course_object)
    print(next_part)
    context['part_object'] = part_object
    context['course_object'] = course_object
    context['next_part'] = next_part

    return render(request, 'videos/partcourse_detail.html', context)
