from django.http import JsonResponse
from django.shortcuts import render

from .models import Category, News


# Create your views here.
def get_news_detail(request, news_id):
    news_obj = News.objects.get(uuid=news_id)

    news = {
        'uuid': news_obj.uuid,
        'title': news_obj.title,
        'author': news_obj.author,
        'date_published': news_obj.date_published,
        'domain': news_obj.domain,
        'url': news_obj.url,
        'html_content': news_obj.html_content,
        'created_at': news_obj.created_at,
        'updated_at': news_obj.updated_at,
        'categories': [{'uuid': category.uuid, 'name': category.name} for category in news_obj.categories.all()],
    }
    return JsonResponse({
        'news': news,
        'message': 'Success'
    })


def get_news_view(request, news_id):
    news_obj = News.objects.get(uuid=news_id)

    return render(request, 'news/detail.html', {'news': news_obj})


def get_all_categories(request):
    view = request.GET.get('view', 'list')
    categories = Category.objects.all()

    if view == 'list':
        return JsonResponse({
            'categories': [{'name': category.name} for category in categories],
            'count': len(categories),
            'message': 'Success'
        })
    elif view == 'tree':
        categories_tree = [{'name': category.name, 'childs': [
            child.name for child in category.get_childs()]} for category in categories if category.parent is None]
        return JsonResponse({
            'categories': categories_tree,
            'count': len(categories),
            'message': 'Success'
        })


def get_news_by_category(request, category_name):
    category = Category.objects.get(name=category_name)
    print(category)
    list_news = category.news_set.all()

    total_count = len(list_news)

    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    sort_by = request.GET.get('sort_by', '-date_published')

    list_news = list_news.order_by(sort_by)
    list_news = list_news[(int(page) - 1) * int(page_size):int(page) * int(page_size)]

    return JsonResponse({
        'news': [
            {
                'uuid': news.uuid,
                'title': news.title,
                'author': news.author,
                'date_published': news.date_published,
            } for news in list_news
        ],
        'count': len(list_news),
        'page': page,
        'page_size': page_size,
        'total_count': total_count,
        'sort_by': sort_by,
        'message': 'Success'
    })
