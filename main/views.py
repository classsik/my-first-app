from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template import TemplateDoesNotExist
from django.template.loader import get_template, render_to_string
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.base import View, TemplateResponseMixin
from django.contrib.auth import logout, login
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from .models import News, Shedule
from django.core.paginator import Paginator
from .models import Comment, Call
from .forms import CommentForm, ModuleFormSet
from django.views.generic.list import ListView
from .models import Course, Module, Content
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.models import modelform_factory
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from .models import Subject
from django.views.generic.detail import DetailView
from students.forms import CourseEnrollForm

def index(request):
    if request.user.is_authenticated:
        last = News.objects.order_by("-id")[0:5]
        return render(request, 'main/index.html', {'last': last})
    else:
        return HttpResponseRedirect("accounts/login/")

def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

class SPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:index')
    success_message = 'Пароль успешно изменен!'

class SLoginView(LoginView):
    template_name = 'registration/login.html'

class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

def news_list(request):
    news = News.objects.all()
    paginator = Paginator(news, 4)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'news': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, 'main/news.html', context=context)




def like_news(request):
    news = get_object_or_404(News, id=request.POST.get('id'))
    is_liked = False
    if news.likes.filter(id=request.user.id).exists():
        news.likes.remove(request.user)
        is_liked = False
    else:
        news.likes.add(request.user)
        is_liked = True
    context = {
        'news': news,
        'is_liked': is_liked,
        'total_likes': news.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('main/like_section.html', context, request=request)
        return JsonResponse({'form': html})




def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    comments = news.comments.filter(active=True)
    is_liked = False
    new_comment = None
    if news.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.news = news

            new_comment.name = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'main/news_detail.html', {'news': news, 'comments': comments, 'comment_form': comment_form, 'is_liked': is_liked, 'total_likes': news.total_likes(), 'new_comment': new_comment})

def lessons_shedule(request):
    shedule = Shedule.objects.all()
    return render(request, 'main/shedule.html', {'shedule': shedule})

def call_shedule(request):
    call = Call.objects.all()
    return render(request, 'main/call.html', {'call': call})

class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('main:manage_course_list')
    template_name = 'course/manage/form.html'

class ManageCourseListView(PermissionRequiredMixin, OwnerCourseMixin, ListView):
    template_name = 'course/manage/list.html'
    permission_required = 'main.view_course'

class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = 'main.add_course'

class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    permission_required = 'main.change_course'

class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    template_name = 'course/manage/delete.html'
    success_url = reverse_lazy('main:manage_course_list')
    permission_required = 'main.delete_course'

class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'course/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('main:manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})

class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'course/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='main', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super(ContentCreateUpdateView,self).dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj)
            return redirect('main:module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})

class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('main:module_content_list', module.id)

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'course/manage/module/content_list.html'
    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})

class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})

class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})

class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'
    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(total_courses=Count('courses'))
        courses = Course.objects.annotate(total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({'subjects': subjects, 'subject': subject, 'courses': courses})

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course':self.object})
        return context 
