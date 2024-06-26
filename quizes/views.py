from django.shortcuts import render
from .models import Quizes 
from django.views.generic import ListView
from django.http import JsonResponse
from question.models import Question , Answer
from result.models import Result
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.

class QuizList(ListView):
    model = Quizes
    template_name = 'quizes/quizlist.html'

@login_required(login_url='login')
def quiz_detail(request , pk):
    quiz = Quizes.objects.get(pk=pk)
    return render(request , 'quizes/quiz_detail.html' , {'obj':quiz})


@login_required(login_url='login')
def quiz_data_view(request,pk):
    quiz = Quizes.objects.get(pk=pk)
    existing = Result.objects.filter(quiz = quiz,user=request.user).exists()

    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answer():
            answers.append(a.text)
        questions.append({str(q):answers})
    return JsonResponse({
        'data':questions ,
        'time': quiz.time,
        'existing':existing,
    })
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url='login')
def save_quiz_view(request , pk):
    # print(request.POST)
    if is_ajax(request=request):
        questions =[]
        data = request.POST
        data_ = dict(data.lists())
       
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            # print('key :',k)
            question = Question.objects.get(text = k)
            questions.append(question)
        # print(questions)
        user = request.user
        quiz = Quizes.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            if a_selected != '':
                question_answers = Answer.objects.filter(question = q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score +=1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append({str(q): {'correct_answer':correct_answer,'answered':a_selected}})
            else:
                results.append({str(q):'not answered'})
        score_ = score * multiplier
        Result.objects.create(quiz=quiz , user=user , score=score_)

        if score_ >= quiz.required_scored_to_pass:
            return JsonResponse({'passed':True , 'score':score_ , 'results':results})
        else:
            return JsonResponse({'passed':False , 'score':score_ , 'results':results})