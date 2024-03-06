Для добавления постраничного вывода на странице с новостями (/news/), следует сделать следующие шаги:

1. Импортировать класс Paginator из модуля django.core.paginator:

python
from django.core.paginator import Paginator


2. Получить все новости и создать экземпляр класса Paginator, указав список новостей и количество элементов на каждой странице (10):

python
news_list = News.objects.all()
paginator = Paginator(news_list, 10)


3. Получить номер запрошенной страницы из GET-параметра и получить объект этой страницы:

python
page_number = request.GET.get('page')
page_obj = paginator.get_page(page_number)


4. В контекст шаблона добавить объект page_obj:

python
context = {'page_obj': page_obj}


5. В шаблоне /news/ использовать цикл для вывода новостей из page_obj:

html
{% for news in page_obj %}
    {{ news.title }}
    {{ news.date }}
    {{ news.author }}
    ...
{% endfor %}


6. Добавить в шаблон пагинацию, чтобы выводить номера ближайших страниц и ссылки на них:

html
{% if page_obj.has_previous %}
    <a href="?page=1">First</a>
    <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
{% endif %}

<span class="current-page">{{ page_obj.number }}</span>

{% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}">Next</a>
    <a href="?page={{ page_obj.paginator.num_pages }}">Last</a>
{% endif %}


Теперь на странице /news/ будет отображаться максимум 10 новостей, а номера лишь ближайших страниц будут видны, а также будет доступна возможность переходить к первой или последней странице.

---
Чтобы реализовать страницу /news/search/, где можно искать новости по определенным критериям, следует сделать следующие шаги:

1. Установить пакет django-filter:


pip install django-filter


2. Создать файл filters.py в папке приложения и определить в нем фильтр для модели News:

python
import django_filters

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='contains')
    author = django_filters.CharFilter(lookup_expr='contains')
    date = django_filters.DateFilter(lookup_expr='gte')

    class Meta:
        model = News
        fields = ['title', 'author', 'date']


3. В представлении страницы /news/search/ импортировать класс фильтра NewsFilter:

python
from .filters import NewsFilter


4. Создать экземпляр фильтра, передав GET-параметры запроса:

python
news_filter = NewsFilter(request.GET, queryset=News.objects.all())


5. В контекст шаблона добавить объект news_filter:

python
context = {'filter': news_filter}


6. В шаблоне /news/search/ вывести форму фильтрации и результаты:

html
<form method="get">
    {{ filter.form.as_p }}
    <button type="submit">Search</button>
</form>

{% for news in filter.qs %}
    {{ news.title }}
    {{ news.date }}
    {{ news.author }}
    ...
{% empty %}
    No news found.
{% endfor %}


Теперь на странице /news/search/ будет доступна форма для фильтрации новостей по названию, имени автора и более поздней даты. Вы сможете выполнять фильтрацию сразу по нескольким критериям.

---
Для добавления страниц создания, редактирования и удаления новостей и статей следует сделать следующие шаги:

1. Создать файлы create_news.html, edit_news.html, delete_news.html, create_article.html, edit_article.html и delete_article.html в папке templates.

2. В файле urls.py добавить маршруты для страниц:

python
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    ...
    path('create/', views.create_news, name='create_news'),
    path('<int:pk>/edit/', views.edit_news, name='edit_news'),
    path('<int:pk>/delete/', views.delete_news, name='delete_news'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/<int:pk>/edit/', views.edit_article, name='edit_article'),
    path('articles/<int:pk>/delete/', views.delete_article, name='delete_article'),
    ...
]


3. В views.py добавить функции обработки запросов для каждой страницы:

python
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Article
from .forms import NewsForm, ArticleForm

def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news:index')
    else:
        form = NewsForm()
    return render(request, 'news/create_news.html', {'form': form})

def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news:index')
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/edit_news.html', {'form': form})

def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        return redirect('news:index')
    return render(request, 'news/delete_news.html', {'news': news})

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news:index')
    else:
        form = ArticleForm()
    return render(request, 'news/create_article.html', {'form': form})

def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('news:index')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'news/edit_article.html', {'form': form})

def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('news:index')
    return render(request, 'news/delete_article.html', {'article': article})


4. Создать формы NewsForm и ArticleForm в файле forms.py:

python
from django import forms
from .models import News, Article

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


Теперь у вас будет возможность добавлять, редактировать и удалять новости и статьи, используя страницы /news/create/, /news/<int:pk>/edit/, /news/<int:pk>/delete/, /news/articles/create/, /news/articles/<int:pk>/edit/ и /news/articles/<int:pk>/delete/.