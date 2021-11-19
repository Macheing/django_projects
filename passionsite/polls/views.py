from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

# Create your views here.

# index view class
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the five published question."""
        return Question.objects.order_by('-pub_date')[:5]

    """
    old index view design
    def index(request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        #output = ', '.join([q.question_text for q in latest_question_list])
        template = loader.get_template('polls/index.html')
        context = {'latest_question_list': latest_question_list,}
        return HttpResponse(template.render(context,request))
        #  we could use render() to accomplish the same task.
        # return render(request, 'polls/index.html', context)
    """

# owner view for grading purpose only
def owner(request):
    return HttpResponse("Hello, world. 6afb69ea is the polls index.")


# detail view class
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    """
    # old detail view design.
    def detail(request, question_id):
        # we can use get_object_or_404() too without having try & except.
        # question = get_object_or_404(Question, pk=question_id)
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise Http404('Question does not exist')

        #return HttpResponse("You're looking at question %s." % question_id)
        return render(request, 'polls/detail.html', {'question': question})
    """
# results view class
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    """
    # old results view design
    def results(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/results.html', {'question': question})

    #response = "You're looking at the results of the question %s."
    #return HttpResponse(response % question_id)

    """

# vote view function
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))




