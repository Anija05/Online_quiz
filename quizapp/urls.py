from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register_page'),
    path('teacher_page/', views.teacher_page, name='teacher_page'),
    path('student_page/', views.student_page, name='student_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('takequiz_page/<int:quizid>/', views.takequiz_page, name='takequiz_page'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('teacher/<int:userid>/', views.Teacher.as_view(), name='teacher'),
    path('student/<int:userid>/quizzes/', views.Student.as_view(), name='student'),
    path('role/', views.RoleView.as_view(), name='role'),
    path('quiz/', views.QuizAPI.as_view(), name='quiz'),
    path('quizdetail/<int:userid>/', views.Quizdetailview.as_view(), name='quizdetail'),
    path('teacher/<int:userid>/quiz/<int:quizid>/questions/',views.QuestionView.as_view(),name='questions'),
    path('teacher/<int:userid>/quiz/<int:quizid>/questions/<int:questionid>/',views.Questiondetailview.as_view(),name='question_detail'),
    path('student/<int:userid>/quiz/<int:quizid>/', views.TakeQuiz.as_view(), name='takequiz'),
    path('student/<int:userid>/quiz/<int:quizid>/submit/',views.SubmitQuizView.as_view(),name='submit_quiz'),
    path('student/<int:userid>/results/',views.ResultView.as_view(),name='result'),
    path('teacher/<int:userid>/quiz/<int:quizid>/results/',views.TeacherResults.as_view(),name='teacher_results'),
]