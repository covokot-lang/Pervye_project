from django.db import models
from django.contrib.auth.models import User

# 1. ТАБЛИЦА КУРСОВ (Каталог)
class Course(models.Model):
    # Существующие поля
    title = models.CharField(max_length=200, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса")
    
    # Новые поля для фильтрации по ТЗ конкурса
    THEME_CHOICES = [
        ('media', 'Медиа и коммуникации'),
        ('leadership', 'Лидерство и команда'),
        ('science', 'Наука и технологии'),
        ('volunteering', 'Волонтерство и добрые дела'),
    ]
    AGE_CHOICES = [
        ('6-11', 'Младшие классы (6-11 лет)'),
        ('12-15', 'Средние классы (12-15 лет)'),
        ('16-18', 'Старшие классы и студенты (16-18 лет)'),
    ]
    FORMAT_CHOICES = [
        ('online', 'Онлайн-курс'),
        ('hybrid', 'Интенсив / Смешанный'),
    ]
    
    theme = models.CharField(max_length=30, choices=THEME_CHOICES, default='media', verbose_name="Тема курса")
    age_category = models.CharField(max_length=10, choices=AGE_CHOICES, default='12-15', verbose_name="Возраст участников")
    course_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='online', verbose_name="Формат обучения")

    def __str__(self):
        return self.title


# 2. ТАБЛИЦА МОДУЛЕЙ (Связана с курсом: в одном курсе много модулей)
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', verbose_name="Курс")
    title = models.CharField(max_length=200, verbose_name="Название модуля")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} -> {self.title}"

# 3. ТАБЛИЦА УРОКОВ (Связана с модулем. Здесь хранится комбинированный контент)
class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons', verbose_name="Модуль")
    title = models.CharField(max_length=200, verbose_name="Название урока")
    content = models.TextField(verbose_name="Текст урока (Лонгрид)")
    video_url = models.URLField(blank=True, verbose_name="Ссылка на видео (если есть)")

    def __str__(self):
        return self.title
        # Поля для уникального интерактивного теста к уроку
    test_question = models.TextField(verbose_name="Вопрос теста", blank=True, null=True)
    option_a = models.CharField(max_length=255, verbose_name="Вариант А", blank=True, null=True)
    option_b = models.CharField(max_length=255, verbose_name="Вариант Б", blank=True, null=True)
    option_c = models.CharField(max_length=255, verbose_name="Вариант В", blank=True, null=True)
    option_d = models.CharField(max_length=255, verbose_name="Вариант Г", blank=True, null=True)
    correct_answer = models.CharField(
        max_length=1, 
        choices=[('A', 'А'), ('B', 'Б'), ('C', 'В'), ('D', 'Г')], 
        verbose_name="Буква правильного ответа (A, B, C, D)", 
        blank=True, 
        null=True
    )


# 4. ТАБЛИЦА ПРОГРЕССА (Связывает пользователя и пройденный урок)
class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False, verbose_name="Пройден")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')

# 5. ТАБЛИЦА ДЛЯ МОДЕРАЦИИ (Материалы, которые участники отправляют на проверку)
class Material(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На модерации'),
        ('approved', 'Опубликовано'),
        ('rejected', 'Отклонено'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор публикации")
    title = models.CharField(max_length=200, verbose_name="Заголовок материала")
    text = models.TextField(verbose_name="Текст материала")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус проверки")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"
# Модель для хранения достижений (наград) участников
class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200, verbose_name="Название достижения")
    description = models.TextField(verbose_name="За что получено")
    icon_type = models.CharField(max_length=20, default="🌟", verbose_name="Иконка")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
