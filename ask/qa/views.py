# Create your views here.
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from .models import Question
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

def paginate(request, qs):
	try:
		limit = int(request.GET.get('limit', 10))
	except ValueError:
		limit = 10
	if limit > 100:
		limit = 10

	try:
		page = int(request.GET.get('page', 1))
	except ValueError:
		raise Http404

	paginator = Paginator(qs, limit)

	try:
		page = paginator.page(page)
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	return page, paginator


def test(request, *args, **kwargs):
	return HttpResponse('OK')

def question_list(request):
	#qs = Question.objects.all()
	#qs = qs.order_by('-added_at')
	qs = Question.objects.new()
	page, paginator = paginate(request, qs)
	paginator.baseurl = reverse('index') + '?page='

	return render(request, 'index.html', {
		'questions': page.object_list,
		'page': page,
		'paginator': paginator,
	})

def popular(request):
	#qs = Question.objects.all()
	#qs = qs.order_by('-rating')
	qs = Question.objects.popular()
	page, paginator = paginate(request, qs)
	paginator.baseurl = reverse('popular') + '?page='

	return render(request, 'popular.html', {
		'questions': page.object_list,
		'page': page,
		'paginator': paginator,
	})	

def question_detail(request, pk):
	question = get_object_or_404(Question, id=pk)
	answers = question.answer_set.all()

	return render(request, 'question.html', {
		'question': question,
		'answers': answers,
	})
