# Hello Django
Django tutorial 시도해보기 :sunglasses:

> Django 2.2.5버전으로 작성
> (참고: [django 튜토리얼 문서](https://docs.djangoproject.com/ko/2.2/intro/tutorial01/))


## part1

* 개발서버 동작

 로컬(127.0.0.1:8000)에서 접속 가능하다
```
python manage.py runserver
```

* 앱 생성

 appname라는 이름의 디렉토리 생성됨
```
python manage.py startapp appname
```

* mysite/urls.py

 include('앱이름.urls') 통해 다른 URLconf 참조 -> 프로젝트와 앱 url 연결
```
urlpatterns = [
    path('polls/', include('polls.urls')),  #url 포함 시 include() 사용
    path('admin/', admin.site.urls),        #예외
]
```

---
## part2

* 데이터베이스 셋업

 mysite/settings.py에서 sqlite3로 설정
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
  > mysql경우 [mysqlclient](https://pypi.org/project/mysqlclient/) 같은 DB API driver를 필요로 하고 'django.db.backends.mysql'로 바꿔줘야 함  
  > user, password, host 등의 추가 설정 필요

* 타임존 설정

 mysite/settings.py에서 아래와 같이 설정
```
TIME_ZONE = 'Asia/Seoul'
```

 한국시간 필요한 경우:
```
from django.utils import timezone
now = timezone.localtime()
```
타임존을 설정하더라도 시간이 안 맞을 수 있는데 localtime() 통해 정확한 한국시간 얻을 수 있다  

* 모델 생성

 장고의 내장 ORM으로 SQL을 작성하지 않아도 코드로 데이터베이스에 접근 (조회/추가/수정/삭제)

  > Model: 파이썬의 class 형태로 DB의 테이블과 매핑됨  
  > Model instance: DB 테이블의 1 row

 모델 생성 예시:
```
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
```
  -> Field 클래스 통해 DB의 속성에 해당되는 컬럼 생성  
  -> ForeignKey를 사용하여 Question에 Choice를 관계시킨다

* 현재 프로젝트에 앱 추가

 mysite/settings.py의 INSTALLED_APPS 설정에 PollsConfig 클래스 추가해준다

* 모델 실제 생성 또는 변경
```
$python manage.py makemigrations  # 변경사항에 대한 마이그레이션 생성
$python manage.py migrate         # 변경사항을 DB에 적용 <- 아직 적용되지 않은 마이그레이션 실행
```

* 모델의 객체 생성 및 조회, 삭제

 Question 모델에 대한 예제:

  ```
  Question.objects.all() #모든 객체 조회

  q = Question(question_text="What's new?", pub_date=timezone.now()) #객체 생성 및 저장
  q.save()

  Question.objects.get(id=2) #id 통한 조회
  Question.objects.filter(question_text__startswith='What') #필터함수 통한 조회 (double-underscore 통해 where 구 기능)

  q.delete() #객체 삭제
  ```
---
## part3

* 뷰 추가 및 연결
  * ```앱이름/view.py``` 에서 뷰(함수 형태) 추가하고 ```앱이름/urls.py```에서 추가한 뷰 연결

  ex> polls/urls.py
```
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),  #view의 index 함수
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),  #view의 detail 함수
]
```

* 템플릿 시스템: 코드로부터 디자인 분리
```
앱이름/template/앱이름
```
 폴더 생성한 후 html 파일 이곳에 넣기

 ex> ```polls/templates/polls/index.html```

  * render(request 객체, template 이름, context 사전형 객체) 를 리턴하면 HttpResponse 사용하지 않아도 됨  
  * django templates 주석 표시 방법=> {# #}  
  * html에서 파이썬 문법 활용 => {% %}로 감싸주기  
  * 하드코딩 url 제거: polls.urls의 path()에서 이름을 정의했기 때문에 가능한 것!         

   ```<a href="/polls/{{ question.id }}/">``` =>  ```<a href="{% url 'detail' question.id %}">```

* get_object_or_404()

 try-except raise Http404 로 예외 발생시키지 않아도 되는 단축 기능

* URL 이름공간 정하기

 앱이 여러 개일 때 앱 내의 url 구분하기 위한 것

 polls/urls.py에 이름 공간 추가: ``` app_name = 'polls' ```

   ```<a href="{% url 'detail' question.id %}">``` => ```<a href="{% url 'polls:detail' question.id %}">```
---
## part4

* form으로 제출된 데이터 처리

 해당하는 POST 자료가 없으면 KeyError 발생시킴 -> try-except 처리 해줘야
```
  try:
      selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist): ## choice 없으면 request.post['choice']가 keyerror 발생시킴
      return render(request, 'polls/detail.html', {'question':question, 'error_message': "You didn't select a choice!",})
```

* F() 객체
 1. python이 아닌 DB에서 해당 연산 처리
 2. 쿼리 수 줄일 수 있음
 3. 경쟁 조건(race condition) 피할 수 있음

   ```selected_choice.votes += 1``` => ```selected_choice.votes = F('votes') + 1```

  python 코드(메모리 상) 값으로 처리하는 것이 아니라 데이터베이스에서 해당 작업을 처리하도록!

* 제너릭 뷰 사용: 코드를 재사용하자!

 클래스로 작성되어 있는 뷰 객체를 말함

 1. URLconf 수정
```
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),             # as_view(): 클래스로 진입하기 위한 진입메소드
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),  # question_id를 pk로 수정
    ... ]
```

 2. View 수정

   함수형 뷰에서 클래스 형 뷰로 변경

 * Generic Display View
   * ListView: object의 목록 표시할 때<br>
   * DetailView: 특정 object 하나에 대한 세부 정보 페이지 표시할 때

    ```
    class IndexView(generic.ListView):
        template_name = 'polls/index.html'
        context_object_name = 'latest_question_list'

    class DetailView(generic.DetailView):
        model = Question
        template_name = 'polls/detail.html'
    ```
