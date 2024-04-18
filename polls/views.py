from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone
from django.http import HttpResponse
from django.template import loader
from .models import Post
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Choice, Question
from django.views.generic.list import ListView



"""
주소 : 판교 , 네이버, 백엔드 부서로 -> 택배를 보낸다.
주소 : 주소확인 -> 우체국 -> 다리 건너서
-> 네이버 본사 -> 백엔드로 배달이 된다.
"""

# Create your views here.


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :9
        ]
        # return Question.objects.filter(pk=1)


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_object(self): 
        # kwargs['urls.py 패턴값과 같음']
        q_id = self.kwargs['question_id']
        question = get_object_or_404(Question, pk=q_id)
        return question

    # def get_queryset(self):
    #     """
    #     Return the last five published questions (not including those set to be
    #     published in the future).
    #     """
    #     return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")
    
    
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


class Practice(generic.DetailView):
    model = Question
    template_name = "polls/practice.html"


class QuestionListView(ListView):
    model = Question
    template_name = 'polls/question_list.html'  # 사용할 템플릿 파일 지정
    context_object_name = 'question_list'  # 템플릿에서 사용할 변수 이름 지정

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]

    def get_object(self): 
        # kwargs['urls.py 패턴값과 같음']
        q_id = self.kwargs['question_id']
        question = get_object_or_404(Question, pk=q_id)
        return question


class PostDetailView(DetailView):
    model = Post
    template_name = 'polls/post_detail.html'  # 사용할 템플릿 파일 지정
    context_object_name = 'post'  # 템플릿에서 사용할 변수 이름 지정


class QuestionCreateView(CreateView):
    model = Question
    fields = ['question_text']
    template_name = 'polls/question_form.html'
    success_url = reverse_lazy('polls:index')  # 예시 URL, 실제 프로젝트에 맞게 수정 필요


class ChoiceCreateView(CreateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_form.html'

    def form_valid(self, form):
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('polls:detail', kwargs={'question_id': self.kwargs['pk']})
    

class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['question_text', 'pub_date']
    template_name = 'polls/update_question_form.html'  # 재사용하거나 적절한 템플릿 지정
    success_url = reverse_lazy('polls:index')  # 예시 URL, 실제 프로젝트에 맞게 수정 필요


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'polls/question_confirm_delete.html'
    success_url = reverse_lazy('polls:index')  # 삭제 후 리다이렉션될 URL, 실제 프로젝트에 맞게 수정 필요

# ==================================

from django.views.generic.base import TemplateView

from polls.models import Question


class HomePageView(TemplateView):
    template_name = "polls/practice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_articles"] = Question.objects.all()[:5]
        return context