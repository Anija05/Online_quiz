from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        # role = request.data.get("role")

        # print(name, email, password, role)

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create(
            name=name,
            email=email,
            password=password,
            role="Student"
        )
        return Response(
            {
                "message": "Registration successful",
                "userid": user.id,
                "name": user.name,
                "email": user.email,
                "role": "Student"
            },
            status=status.HTTP_201_CREATED
        )
        
@method_decorator(csrf_exempt, name='dispatch')
class Login(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.password != password:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {
                "message": "Login successful",
                "userid": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            },
            status=status.HTTP_200_OK
        )
class RoleView(APIView):
    def get(self, request, userid):
        try:
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.role == "Teacher":
            return Response({
                "role": "teacher",
                "page": "teacher",
                "message": "Welcome Teacher",
                "options": [
                    "Create Quiz",
                    "View Quizzes",
                    "Edit Quiz",
                    "Delete Quiz"
                ]
            })
        elif user.role == "Student":
            return Response({
                "role": "student",
                "page": "student",
                "message": "Welcome Student",
                "options": [
                    "View Quizzes",
                    "Take Quiz",
                    "View Results"
                ]
            })
        return Response(
            {"error": "Invalid role"},
            status=status.HTTP_400_BAD_REQUEST
        )

class Teacher(APIView):
    def get(self, request, userid):
        try:
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.role != "Teacher":
            return Response(
                {"error": "Only Teacher can access quizzes"},
                status=status.HTTP_403_FORBIDDEN
            )
        quiz = Quiz.objects.filter(teacher=user)
        serializer = QuizSerializer(quiz, many=True)
        return Response(serializer.data)
    def post(self, request, userid):
        try:
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.role != "Teacher":
            return Response(
                {"error": "Only Teacher can create quizzes"},
                status=status.HTTP_403_FORBIDDEN
            )
        data = request.data.copy()
        data["teacher"] = user.id
        serializer = QuizSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class Student(APIView):
    def get(self,request,userid):
        try:
            user=User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {'error':'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.role!='Student':
            return Response(
                {'error':'Students can only take quiz'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        quiz=Quiz.objects.all()
        serializer=QuizSerializer(quiz,many=True)
        return Response(serializer.data)

class TakeQuiz(APIView):
    def get(self,request,userid,quizid):
        try:
            user=User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {'error':'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.role!='Student':
            return Response(
                {'error':'Students can only take the quiz'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if Result.objects.filter(student=user).exists():
            return Response(
                {'error':'You cannot able to attend another quiz'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            quiz=Quiz.objects.get(id=quizid)
        except Quiz.DoesNotExist:
            return Response(
                {'error':'Quiz not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        question=Question.objects.filter(quiz=quiz)
        serializer=QuestionSerializer(question,many=True)
        return Response(
            {'quiz':QuizSerializer(quiz).data,
            'question':serializer.data}
        )

class QuizAPI(APIView):
    def get(self,request):
        quizes=Quiz.objects.all()
        serializer=QuizSerializer(quizes,many=True)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class Quizdetailview(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self,request):
        serializer=QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
    def put(self,request,userid):
        try:
            quiz=Quiz.objects.get(id=userid)
        except Quiz.DoesNotExist:
            return Response(
                {'error':'Quiz not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer=QuizSerializer(quiz,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,userid):
        try:
            quiz=Quiz.objects.get(id=userid)
        except Quiz.DoesNotExist:
            return Response(
                {'error':'Quiz not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        quiz.delete()
        return Response(
            {"message": "Quiz deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
@method_decorator(csrf_exempt, name='dispatch')
class QuestionView(APIView):
    def get(self, request, userid, quizid):
        try:
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.role != "Teacher":
            return Response(
                {"error": "Only Teacher can access questions"},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            quiz = Quiz.objects.get(
                id=quizid,
                teacher=user
            )
        except Quiz.DoesNotExist:
            return Response(
                {"error": "Quiz not found or does not belong to this teacher"},
                status=status.HTTP_404_NOT_FOUND
            )
        questions = Question.objects.filter(quiz=quiz)
        serializer = QuestionSerializer(
            questions,
            many=True
        )
        return Response(serializer.data)
    def post(self, request, userid, quizid):
        try:
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.role != "Teacher":
            return Response(
                {"error": "User is not a Teacher"},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            quiz = Quiz.objects.get(id=quizid)
        except Quiz.DoesNotExist:
            return Response(
                {"error": "Quiz not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if quiz.teacher.id != user.id:
            return Response(
                {"error": "This quiz does not belong to this teacher"},
                status=status.HTTP_403_FORBIDDEN
            )
        data = request.data.copy()
        data["quiz"] = quiz.id
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@method_decorator(csrf_exempt, name='dispatch')
class Questiondetailview(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request, userid, quizid, questionid):
        try:
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.role != "Teacher":
            return Response(
                {"error": "Only teachers can access this"},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            question = Question.objects.get(
                id=questionid,
                quiz_id=quizid
            )
        except Question.DoesNotExist:
            return Response(
                {"error": "Question not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, userid, quizid, questionid):

        try:
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.role != "Teacher":
            return Response(
                {"error": "Only teachers can update questions"},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            question = Question.objects.get(
                id=questionid,
                quiz_id=quizid
            )
        except Question.DoesNotExist:
            return Response(
                {"error": "Question not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = QuestionSerializer(
            question,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def delete(self, request, userid, quizid, questionid):
        try:
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if user.role != "Teacher":
            return Response(
                {"error": "Only Teacher can delete questions"},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            quiz = Quiz.objects.get(id=quizid)
        except Quiz.DoesNotExist:
            return Response(
                {"error": "Quiz not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if quiz.teacher.id != user.id:
            return Response(
                {"error": "This quiz does not belong to this teacher"},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            question = Question.objects.get(id=questionid)
        except Question.DoesNotExist:
            return Response(
                {"error": "Question not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if question.quiz.id != quiz.id:
            return Response(
                {"error": "This question does not belong to this quiz"},
                status=status.HTTP_403_FORBIDDEN
            )
        question.delete()
        return Response(
            {"message": "Question deleted successfully"},
            status=status.HTTP_200_OK
        )
class ResultView(APIView):
    def get(self, request, userid):
        try:
            student = User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {"error": "Student not found"},
                status=404
            )
        results = Result.objects.filter(student=student)
        data = []
        for result in results:
            data.append({
                "id": result.id,
                "quiz_title": result.quiz.title,
                "score": result.score,
                "total_questions": result.total_questions
            })
        return Response(data)

@method_decorator(csrf_exempt, name='dispatch')
class SubmitQuizView(APIView):
    def post(self, request, userid, quizid):
        try:
            student = User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if student.role != "Student":
            return Response(
                {"error": "Only students can submit quizzes"},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            quiz = Quiz.objects.get(id=quizid)
        except Quiz.DoesNotExist:
            return Response(
                {"error": "Quiz not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        existing_result = Result.objects.filter(student=student,quiz=quiz).first()
        if existing_result:
            return Response(
                {
                    "error": "You have already submitted."
                },status=400
            )
        questions = Question.objects.filter(quiz=quiz)
        score = 0
        answers = request.data.get("answers", {})
        for question in questions:
            student_answer = answers.get(str(question.id))
            if student_answer == question.correct_answer:
                score += 1
        total_questions = questions.count()
        result = Result.objects.create(
            student=student,
            quiz=quiz,
            score=score,
            total_questions=total_questions
        )
        return Response({
            "message": "Quiz submitted successfully",
            "score": score,
            "total_questions": total_questions,
            "result_id": result.id
        })
class TeacherResults(APIView):

    def get(self, request, userid, quizid):

        try:
            admin = User.objects.get(id=userid)
        except User.DoesNotExist:
            return Response(
                {"error": "Admin not found"},
                status=404
            )

        if admin.role != "Teacher":
            return Response(
                {"error": "Only Admin can view results"},
                status=403
            )

        try:
            quiz = Quiz.objects.get(id=quizid)
        except Quiz.DoesNotExist:
            return Response(
                {"error": "Quiz not found"},
                status=404
            )

        results = Result.objects.filter(
            quiz=quiz
        ).select_related("student")

        data = []

        for result in results:
            data.append({
                "student_name": result.student.name,
                "student_email": result.student.email,
                "score": result.score,
                "total_questions": result.total_questions
            })

        return Response(data)
def index(request):
    return render(request,'index.html')
def register(request):
    return render(request,'register.html')
def login_page(request):
    return render(request, 'login.html')
def student_page(request):
    return render(request, 'student.html')
def teacher_page(request):
    return render(request, 'teacher.html')
def takequiz_page(request, quizid):
    return render(request, 'takequiz.html', {
        'quizid': quizid
    })
