import json

from django.http import HttpResponse
from django.shortcuts import render

from .models import Field, Target, Word, WordField, WordTarget


# Create your views here.
def get_all_words(request):
    words = Word.objects.all()

    target = request.GET.get('target', '')
    if target:
        target_obj = Target.objects.filter(name=target).first()
        if target_obj:
            words = words.filter(wordtarget__target=target_obj)
    field = request.GET.get('field', '')
    if field:
        field_obj = Field.objects.filter(name=field).first()
        if field_obj:
            words = words.filter(wordfield__field=field_obj)

    level = request.GET.get('level', '')
    if level:
        if level == 'easy':
            words = words.filter(wordfield__idf__lt=3.0, wordfield__field=field_obj)
        elif level == 'medium':
            words = words.filter(wordfield__idf__gte=3.0, wordfield__idf__lt=7.0, wordfield__field=field_obj)
        elif level == 'hard':
            words = words.filter(wordfield__idf__gte=7.0, wordfield__field=field_obj)

    sort_by = request.GET.get('sort_by', 'id')
    if sort_by:
        if sort_by == 'id':
            words = words.order_by('id')
        elif sort_by == 'text':
            words = words.order_by('word')
        elif sort_by == 'idf':
            words = words.order_by('wordfield__idf')

    limit = request.GET.get('limit', '1000')
    if limit:
        words = words[:int(limit)]

    if field:
        words = [{'text': word.word, 'weight': WordField.objects.get(word=word, field=field_obj).idf} for word in words]
    else:
        words = [{'text': word.word} for word in words]
    return HttpResponse(json.dumps(words), content_type='application/json')
