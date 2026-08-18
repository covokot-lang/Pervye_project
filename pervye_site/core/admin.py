from django.contrib import admin
from .models import Course, Module, Lesson, Progress, Material

# Регистрируем модели, чтобы админ мог ими управлять
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Progress)
admin.site.register(Material)
