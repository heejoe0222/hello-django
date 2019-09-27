import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

kor_now = timezone.localtime()

# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = kor_now + datetime.timedelta(days=30) #timedelta: 두 날짜나 시간의 차이 기간 나타냄
        future_question = Question(pub_date=time)           #임의로 30일 미래인 Question객체 생성
        self.assertIs(future_question.was_published_recently(),False) #이 경우 False를 반환하길 원함


    def test_was_published_recently_with_old_question(self):
        time = kor_time-datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)


    def test_was_published_recently_with_recent_question(self):
        time = kor_time-datetime.timedelta(hours=23, minites=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),True)


    def create_question(question_text, days):
        time = kor_now + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase): #인덱스 뷰 테스트
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No polls are available.") #메세지 확인
        self.assertQuerysetEqual(response.context['latest_question_list'],[]) #latest_question_list 비어있는지 확인


    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],['<Question: Past question.>']
            )


    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])


    def test_furue_question_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])


    def test_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 1.>'], ['<Question: Past question 2.>']
            )


class QuestionDetailViewTests(TestCase): #디테일 뷰 테스트
    def test_future_question(self):
        future_question = create_question(question_text='Future question.',days=5)
        url = reverse('polls:detail',args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)


    def test_past_question(self):
        past_question = create_question(question_text='Past question.',days=-5)
        url = reverse('polls:details', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
