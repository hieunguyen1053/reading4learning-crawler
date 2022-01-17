import json
from math import ceil

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from .models import Field, Target, Word, WordField, WordTarget


def get_all_targets(request):
    objects = Target.objects.all()
    resp = {
        'targets': [{'text': item.name} for item in objects],
        'total': len(objects)
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")

def get_all_fields(request):
    objects = Field.objects.all()
    objects = objects.exclude(name='General')
    resp = {
        'fields': [{'text': item.name} for item in objects],
        'total': len(objects)
    }
    return HttpResponse(json.dumps(resp), content_type="application/json")

def get_all_words(request):
    words = Word.objects.all()
    words = words.filter(~Q(word__startswith='-'))
    words = words.filter(~Q(word__startswith="'"))
    words = words.filter(~Q(word__startswith='.'))

    list_words = request.GET.get('list_words', None)
    if list_words:
        list_words = list_words.split(',')
        list_words = [item.strip() for item in list_words]
        words = words.filter(word__in=list_words)

    target = request.GET.get('target', None)
    if target:
        target_obj = Target.objects.filter(name=target).first()
        if target_obj:
            wordidfs = WordTarget.objects.filter(target=target_obj)
            words = words.filter(wordtarget__in=wordidfs)

    field = request.GET.get('field', 'General')
    field_obj = Field.objects.filter(name=field).first()
    if field_obj:
        wordidfs = WordField.objects.filter(field=field_obj)
        words = words.filter(wordfield__in=wordidfs)
        wordidfs = wordidfs.filter(word__in=words)

    level = request.GET.get('level', None)
    if level:
        if level == 'easy':
            wordidfs = wordidfs.filter(idf__lt=3.0)
        elif level == 'medium':
            wordidfs = wordidfs.filter(idf__gte=3.0, idf__lt=7.0)
        elif level == 'hard':
            wordidfs = wordidfs.filter(idf__gte=7.0)

    sort_by = request.GET.get('sort_by', None)
    if sort_by:
        if sort_by == 'text':
            wordidfs = wordidfs.order_by('word__word')
        elif sort_by == 'idf':
            wordidfs = wordidfs.order_by('idf')

    total = len(wordidfs)

    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 100))

    num_pages = ceil(total / page_size)
    start = (page - 1) * page_size
    end = start + page_size
    wordidfs = wordidfs[start:end]

    words = {
        'vocabulary': [{'text': item.word.word, 'idf': item.idf } for item in wordidfs],
        'total': total,
        'page': page,
        'num_pages': num_pages,
        'page_size': page_size
    }
    return HttpResponse(json.dumps(words), content_type='application/json')
