from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    context = {"form": form}
    return render(request, 'news/register.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('login')


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    context = {"form": form}
    return render(request, 'news/login.html', context=context)


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'],
                      form.cleaned_data['content'],
                      'nikolajkozich@gmail.com',
                      ['nikolajkozich@gmail.com'],
                      fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
    else:
        form = ContactForm()
    context = {"form": form}
    return render(request, 'news/test.html', context=context)


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 2
    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    paginate_by = 2
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'],
                                   is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id'


class CreateNews(LoginRequiredMixin, CreateView):
    login_url = '/admin/'
    # raise_exception = True
    form_class = NewsForm
    template_name = 'news/add_news.html'


"""
def index(request):
    news = News.objects.order_by('-created_at')
    context = {'news': news,
               'title': 'Список новостей-ей-ей'}
    return render(request, template_name='news/index.html', context=context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    context = {'news': news,
               'category': category}
    return render(request, template_name='news/category.html', context=context)


def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})


def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # news = News.objects.create(**form.cleaned_data)
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()
    context = {'form': form,
               }
    return render(request, 'news/add_news.html', context=context)"""
