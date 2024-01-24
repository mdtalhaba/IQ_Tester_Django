from django.contrib import admin
from .models import Category, Question, Quiz, Choice, UserResponse

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['quiz','quistion','option', 'is_correct']

    def quistion(self, obj) :
        return obj.question.text
    
    def quiz(self, obj) :
        return obj.question.quiz.title
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz','text']

    def quiz(self, obj) :
        return obj.quiz.title

admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(UserResponse)
