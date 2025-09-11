from django.contrib import admin
from django.utils.html import format_html
from .models import Question, Answer, UserExamSession, UserAnswer



# Javoblarni savol ostida kiritish uchun Inline
class AnswerInline(admin.TabularInline):
     model = Answer
     extra = 2  # Kamida 2 ta javob bo‘lishi ko‘rinadi
     min_num = 1
     max_num = 4
     fields = ('text', 'is_correct')
     show_change_link = True

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
     list_display = ('id', 'text_snippet', 'created_at')
     search_fields = ('text',)
     list_filter = ('created_at',)
     inlines = [AnswerInline]

     def text_snippet(self, obj):
          return obj.text[:50]
     text_snippet.short_description = 'Savol matni'



@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
     list_display = ('id', 'question_text', 'text', 'is_correct')
     list_filter = ('is_correct',)
     search_fields = ('text', 'question__text')

     def question_text(self, obj):
          return obj.question.text[:40]
     question_text.short_description = 'Savol'



@admin.register(UserExamSession)
class UserExamSessionAdmin(admin.ModelAdmin):
     list_display = (
          'id', 'user', 'start_time', 'end_time', 'is_finished',
          'duration', 'correct_answers', 'total_answers', 'percentage',
          'score', 'status'
     )
     list_filter = ('is_finished',)
     search_fields = ('user__username',)



# @admin.register(UserAnswer)
# class UserAnswerAdmin(admin.ModelAdmin):
#      list_display = ('id', 'session', 'user', 'question_snippet', 'selected_answer_text')
#      list_display_links = ('id', 'session', 'user')
#      search_fields = ('session__user__username', 'question__text', 'selected_answer__text')
#      list_filter = ('session__is_finished', 'selected_answer__is_correct')
#      # list_editable = ()

#      def user(self, obj):
#           return obj.session.user

#      def question_snippet(self, obj):
#           return obj.question.text[:50]
#      question_snippet.short_description = 'Savol'

#      def selected_answer_text(self, obj):
#           return obj.selected_answer.text
#      selected_answer_text.short_description = 'Tanlangan javob'

#      def is_correct(self, obj):
#           return obj.selected_answer and obj.selected_answer.is_correct
#      is_correct.boolean = True



@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
     list_display = ('id', 'session', 'user_display', 'question', 'highlighted_answer')


     def user_display(self, obj):
          return obj.session.user
     user_display.short_description = "User"

     def highlighted_answer(self, obj):
          selected = obj.selected_answer
          is_correct = selected.is_correct
          color = "#a3f7bf" if is_correct else "#fcd5ce"
          return format_html('<div style="background-color:{}; padding:5px;">{}</div>', color, selected.text)
     highlighted_answer.short_description = "Tanlangan javob"

     def get_queryset(self, request):
          # Tanlangan javobni birinchi ko‘rsatish uchun: order by tanlangan javob ID
          return super().get_queryset(request).order_by('-selected_answer__is_correct')
