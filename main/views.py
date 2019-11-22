from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.contrib.auth import logout, login
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from .models import News, Shedule
from django.core.paginator import Paginator
from .models import Comment
from .forms import CommentForm

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

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    comments = news.comments.filter(active=True)

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
    return render(request, 'main/news_detail.html', {'news': news, 'comments': comments, 'comment_form': comment_form})

def lessons_shedule(request):
    shedule = Shedule.objects.all()
    return render(request, 'main/shedule.html', {'shedule': shedule})
