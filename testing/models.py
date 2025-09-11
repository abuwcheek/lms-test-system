from django.db import models
from django.contrib.auth.models import User




class Question(models.Model):
     text = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.text[:50]



class Answer(models.Model):
     question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
     text = models.CharField(max_length=255)
     is_correct = models.BooleanField(default=False)

     def __str__(self):
          return f"{self.question.text[:30]} - {self.text}"



class UserExamSession(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     start_time = models.DateTimeField(auto_now_add=True)
     end_time = models.DateTimeField(null=True, blank=True)
     is_finished = models.BooleanField(default=False)

     def duration(self):
          if self.end_time:
               delta = self.end_time - self.start_time
               return str(delta).split('.')[0]
          return "⏳"

     def correct_answers(self):
          return self.answers.filter(selected_answer__is_correct=True).count()

     def total_answers(self):
          return self.answers.count()

     def percentage(self):
          total = self.total_answers()
          correct = self.correct_answers()
          return round((correct / total) * 100, 2) if total > 0 else 0

     def score(self):
          return f"{self.percentage()} / 100"

     def status(self):
          return "😊 O‘tdi" if self.percentage() >= 60 else "😞 O‘tmadi"

     def __str__(self):
          return f"{self.user.username} - Session"




class UserAnswer(models.Model):
     session = models.ForeignKey(UserExamSession, on_delete=models.CASCADE, related_name='answers')
     question = models.ForeignKey(Question, on_delete=models.CASCADE)
     selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

     class Meta:
          unique_together = ('session', 'question')  # Har bir savolga bitta javob

     def __str__(self):
          return f"{self.session.user.username} - Q{self.question.id} - A{self.selected_answer.id} - {self.question.text[:30]}"
