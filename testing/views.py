from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils import timezone
from .models import Question, Answer, UserExamSession, UserAnswer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# Testni boshlash
@method_decorator(login_required, name='dispatch')
class StartExamView(View):
     def get(self, request):
          session, created = UserExamSession.objects.get_or_create(
               user=request.user,
               is_finished=False,
          )
          return redirect('exam:question', question_index=1)



# Savolni ko‘rsatish va tanlash
@method_decorator(login_required, name='dispatch')
class QuestionView(View):
     def get(self, request, question_index):
          questions = Question.objects.all().order_by('id')
          question_index = int(question_index)
          
          if question_index >= questions.count():
               return redirect('exam:finish')
          
          question = questions[question_index]
          answers = question.answers.all()
          session = UserExamSession.objects.get(user=request.user, is_finished=False)
          try:
               selected = UserAnswer.objects.get(session=session, question=question).selected_answer_id
          except UserAnswer.DoesNotExist:
               selected = None
          
          context = {
               'question': question,
               'answers': answers,
               'index': question_index,
               'total': questions.count(),
               'selected': selected,
               
               'start_time': session.start_time.isoformat(),
               'duration_minutes': 20,
          }
          return render(request, 'testing.html', context)



     def post(self, request, question_index):
          questions = Question.objects.all().order_by('id')
          question = questions[int(question_index)]
          answer_id = request.POST.get('answer')

          if answer_id:
               answer = get_object_or_404(Answer, id=answer_id, question=question)
               session = UserExamSession.objects.get(user=request.user, is_finished=False)
               user_answer, created = UserAnswer.objects.update_or_create(
                    session=session,
                    question=question,
                    defaults={'selected_answer': answer}
               )

          if 'next' in request.POST:
               return redirect('exam:question', question_index=int(question_index)+1)
          elif 'prev' in request.POST:
               return redirect('exam:question', question_index=int(question_index)-1)
          elif 'finish' in request.POST:
               return redirect('exam:finish')
          return redirect('exam:question', question_index=question_index)



class FinishExamView(View):
     def get(self, request):
          session = UserExamSession.objects.filter(user=request.user, is_finished=False).first()
          if session:
               session.is_finished = True
               session.end_time = timezone.now()
               session.save()

          user_answers = UserAnswer.objects.filter(session=session)
          total = user_answers.count()
          correct = sum(1 for ua in user_answers if ua.selected_answer and ua.selected_answer.is_correct)
          incorrect = total - correct
          percentage = round((correct / total) * 100, 2) if total > 0 else 0
          score = correct * 5  # har to‘g‘ri javob 5 ball

          context = {
               'correct_count': correct,
               'incorrect_count': incorrect,
               'total': total,
               'percentage': percentage,
               'score': score,
               'user_answers': user_answers,
          }
          return render(request, 'finish.html', context)


class ReviewExamView(View):
     def get(self, request):
          session = UserExamSession.objects.filter(user=request.user, is_finished=True).last()
          user_answers = UserAnswer.objects.filter(session=session).select_related('question', 'selected_answer')
          context = {
               'user_answers': user_answers,
          }
          return render(request, 'review.html', context)

