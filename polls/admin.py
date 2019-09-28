from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3 #한번에 추가 가능한 슬롯 개수


class QuestionAdmin(admin.ModelAdmin): #fieldsets, inlines, list_display, list_filter는 정해진 변수명
    fieldsets = [ #수십 개의 필드가 있는 폼의 경우 fieldset으로 분할하는 것이 좋음
        #(fieldset의 제목, {fields: [관련 필드 리스트]})
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text','pub_date','was_published_recently')
    list_filter = ['pub_date'] #filter 사이드 바 추가 -> 필터링중인 필드 유형(DateTimeField)에 따라 필터 유형 정해짐
    search_fields = ['question_text'] #변경 목록 맨 위에 검색 창이 추가 -> [] 내 필드 검색

# Register your models here.
admin.site.register(Question, QuestionAdmin)
