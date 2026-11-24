from django.contrib import admin

# Register your models here.
from quizapp.models import *
admin.site.register(User)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Result)
