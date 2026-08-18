from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Module, Lesson, Progress, Material, Achievement
from .forms import UserRegisterForm, UserLoginForm, MaterialForm

# ==========================================
# 🏠 ГЛАВНАЯ СТРАНИЦА И КАТАЛОГ ПРОГРАММ
# ==========================================
def catalog_view(request):
    """
    Выводит официальный каталог программ с фильтрацией по возрасту, 
    тематикам и форматам, а также осуществляет полностью регистронезависимый поиск.
    """
    query = request.GET.get('q', '').strip()
    selected_theme = request.GET.get('theme', '')
    selected_age = request.GET.get('age', '')
    # Считываем выбранный формат из GET-запроса формы
    selected_format = request.GET.get('format', '')

    courses = Course.objects.all()

    if query:
        courses = courses.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct()

    if selected_theme:
        courses = courses.filter(theme=selected_theme)
    if selected_age:
        courses = courses.filter(age_category=selected_age)
    
    # ИСПРАВЛЕНИЕ: Фильтруем строго по полю модели course_format
    if selected_format:
        courses = courses.filter(course_format=selected_format)

    context = {
        'courses': courses,
        'query': query,
        'selected_theme': selected_theme,
        'selected_age': selected_age,
        'selected_format': selected_format,
    }
    return render(request, 'catalog.html', context)

# ==========================================
# 📖 СТРАНИЦА КУРСА (СТРУКТУРА ПРОГРАММЫ)
# ==========================================
@login_required(login_url='login')
def course_detail_view(request, course_id):
    """
    Открывает детальную карточку выбранного курса со списком 
    всех привязанных к нему модулей и вложенных уроков.
    """
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})


# ==========================================
# 📝 СТРАНИЦА УРОКА, ТЕСТ И ЗАВЕРШЕНИЕ БЛОКА
# ==========================================
@login_required(login_url='login')
def lesson_view(request, lesson_id):
    """
    Динамически выводит видеоплеер VK, конспект (поле content),
    проверяет уникальный интерактивный тест из админки, а также
    обрабатывает кнопку закрытия всего образовательного модуля.
    """
    # Получаем текущий урок из базы данных
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    test_checked = False
    is_correct = False

    # 1. ОБРАБОТКА НАЖАТИЯ КНОПКИ ПРОВЕРКИ ТЕСТА
    if request.method == 'POST' and 'submit_test' in request.POST:
        test_checked = True
        user_answer = request.POST.get('user_answer')

        # Сравниваем выбор пользователя с буквой правильного ответа из базы данных
        if user_answer == lesson.correct_answer:
            is_correct = True

    # 2. ОБРАБОТКА НАЖАТИЯ КНОПКИ ЗАВЕРШЕНИЯ БЛОКА (МОДУЛЯ)
    if request.method == 'POST' and 'complete_module' in request.POST:
        # Помечаем ВСЕ уроки текущего модуля как пройденные для этого пользователя
        lessons_in_module = Lesson.objects.filter(module=lesson.module)
        for les in lessons_in_module:
            progress, created = Progress.objects.get_or_create(user=request.user, lesson=les)
            progress.is_completed = True
            progress.save()
            
        messages.success(request, f"Поздравляем! Модуль '{lesson.module.title}' успешно завершен и занесен в портфолио!")
        return redirect('profile')

    context = {
        'lesson': lesson,
        'test_checked': test_checked,
        'is_correct': is_correct,
    }
    return render(request, 'lesson_detail.html', context)


# ==========================================
# 💼 ЛИЧНЫЙ КАБИНЕТ И ЦИФРОВОЕ ПОРТФОЛИО
# ==========================================
@login_required(login_url='login')
def profile_view(request):
    """
    Личный кабинет: рассчитывает успеваемость по модулям, управляет UGC-публикациями, 
    содержит панель модератора и генерирует официальное резюме.
    """
    user = request.user
    is_admin = user.is_superuser
    is_moderator = user.groups.filter(name='Модераторы').exists() or user.is_staff
    is_user = not is_admin and not is_moderator

    # Редактирование личных данных пользователя
    if request.method == 'POST' and 'update_profile' in request.POST:
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, "Профиль успешно обновлен!")
        return redirect('profile')

    # Панель модерации: одобрение или отклонение статей участников
    if is_moderator or is_admin:
        if request.method == 'POST' and 'material_id' in request.POST:
            material_id = request.POST.get('material_id')
            action = request.POST.get('action')
            if material_id and action:
                material = get_object_or_404(Material, id=material_id)
                if action == 'approve':
                    material.status = 'approved'
                elif action == 'reject':
                    material.status = 'rejected'
                material.save()
                return redirect('profile')

    # Сортировка материалов для вывода
    if is_moderator or is_admin:
        materials_for_review = Material.objects.filter(status='pending').order_by('created_at')
        my_materials = Material.objects.filter(author=user).order_by('-created_at')
    else:
        materials_for_review = None
        my_materials = Material.objects.filter(author=user).order_by('-created_at')

    # Рассчет метрик успеваемости для фишки "Цифровое Портфолио"
    user_achievements = Achievement.objects.filter(user=user)
    completed_lessons_count = Progress.objects.filter(user=user, is_completed=True).count()
    approved_materials_count = Material.objects.filter(author=user, status='approved').count()
    achievements_count = user_achievements.count()

    # Сбор процентов прогресса по каждому учебному модулю
    modules_progress = []
    all_modules = Module.objects.all().prefetch_related('lessons')
    
    for module in all_modules:
        total_lessons = module.lessons.count()
        completed_lessons = Progress.objects.filter(user=user, lesson__module=module, is_completed=True).count()
        percent = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0
        modules_progress.append({
            'title': module.title,
            'course_title': module.course.title,
            'completed': completed_lessons,
            'total': total_lessons,
            'percent': percent
        })

    # Считываем флаг для автогенерации бланка резюме
    show_resume = request.GET.get('generate_resume', '') == 'true'

    context = {
        'my_materials': my_materials,
        'materials_for_review': materials_for_review,
        'achievements': user_achievements,
        'modules_progress': modules_progress,
        'is_admin': is_admin,
        'is_moderator': is_moderator,
        'is_user': is_user,
        
        # Передача данных портфолио в HTML
        'completed_lessons_count': completed_lessons_count,
        'approved_materials_count': approved_materials_count,
        'achievements_count': achievements_count,
        'show_resume': show_resume,
    }
    return render(request, 'profile.html', context)


# ==========================================
# ✍️ СОЗДАНИЕ МАТЕРИАЛА (БЛОГ УЧАСТНИКОВ / UGC)
# ==========================================
@login_required(login_url='login')
def create_material_view(request):
    """
    Позволяет школьникам делиться научными заметками или медиа-статьями, 
    отправляя их на предварительную верификацию модераторам.
    """
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.author = request.user
            material.status = 'pending'
            material.save()
            messages.success(request, "Материал успешно отправлен на модерацию Первых!")
            return redirect('profile')
    else:
        form = MaterialForm()
    return render(request, 'create_material.html', {'form': form})


# ==========================================
# 🔐 ВХОД, РЕГИСТРАЦИЯ И ВЫХОД ИЗ СИСТЕМЫ
# ==========================================
def register_view(request):
    """Регистрация новых участников платформы."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Добро пожаловать в Движение!")
            return redirect('catalog')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
# Убедитесь, что импорты вашей формы находятся вверху файла, например:
# from .forms import UserLoginForm

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # Безопасно достаем очищенные данные из полей формы
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Проверяем пользователя через стандартный механизм Django
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('/') # Перенаправляем на главную страницу каталога
            else:
                form.add_error(None, "Неверное имя пользователя или пароль")
    else:
        form = UserLoginForm()
        
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Безопасный выход из аккаунта экосистемы."""
    logout(request)
    return redirect('catalog')





