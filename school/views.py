from datetime import timedelta
from django.contrib import messages
from django.db.models import Avg
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from home_auth.models import CustomUser
from student.models import Student
from .models import (
    Notification,
    TeacherProfile,
    ClassSchedule,
    Homework,
)
from .forms import TeacherProfileForm, ClassScheduleForm, HomeworkForm


def index(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect("dashboard")
        return redirect("teacher_dashboard")
    return render(request, "authentication/login.html")


def _require_teacher(user):
    return user.is_authenticated and (user.is_teacher or user.is_admin)


def _ensure_teacher_profiles():
    teacher_users = CustomUser.objects.filter(is_teacher=True)
    for teacher in teacher_users:
        TeacherProfile.objects.get_or_create(user=teacher)


@login_required
def dashboard(request):
    if not request.user.is_admin:
        if request.user.is_teacher:
            return redirect("teacher_dashboard")
        messages.error(request, "You do not have access to the admin dashboard.")
        return redirect("login")

    _ensure_teacher_profiles()
    today = timezone.localdate()
    student_count = Student.objects.count()
    teacher_count = CustomUser.objects.filter(is_teacher=True).count()
    total_classes = ClassSchedule.objects.count()
    coverage = (
        ClassSchedule.objects.filter(status="completed").aggregate(avg=Avg("syllabus_coverage"))["avg"]
        or 0
    )
    upcoming_classes = ClassSchedule.objects.filter(date__gte=today).order_by("date", "start_time")[:5]
    homework_queue = Homework.objects.order_by("-assigned_on")[:5]
    teacher_profiles = TeacherProfile.objects.select_related("user").order_by("-updated_at")[:5]
    recent_students = Student.objects.order_by("-joining_date")[:5]
    context = {
        "student_count": student_count,
        "teacher_count": teacher_count,
        "total_classes": total_classes,
        "coverage": round(coverage, 1),
        "upcoming_classes": upcoming_classes,
        "homework_queue": homework_queue,
        "teacher_profiles": teacher_profiles,
        "recent_students": recent_students,
    }
    return render(request, "Home/index.html", context)


@login_required
def teacher_dashboard(request):
    if not _require_teacher(request.user):
        messages.error(request, "Only teachers can access the teacher workspace.")
        return redirect("login")

    _ensure_teacher_profiles()
    profile, _ = TeacherProfile.objects.get_or_create(user=request.user)
    today = timezone.localdate()
    weekly_range = today - timedelta(days=7)

    teacher_classes = ClassSchedule.objects.filter(teacher=request.user)
    upcoming_classes = teacher_classes.filter(date__gte=today).order_by("date", "start_time")[:5]
    recent_history = teacher_classes.filter(date__gte=weekly_range).order_by("-date", "-start_time")[:5]
    completed_count = teacher_classes.filter(status="completed").count()
    total_classes = teacher_classes.count()
    coverage = teacher_classes.aggregate(avg=Avg("syllabus_coverage"))["avg"] or 0
    total_students = Student.objects.count()

    homework_list = Homework.objects.filter(teacher=request.user).order_by("due_date")[:5]
    other_teachers = (
        TeacherProfile.objects.select_related("user")
        .exclude(user=request.user)
        .order_by("user__first_name")[:6]
    )
    students = Student.objects.select_related("parent").all()[:6]

    context = {
        "profile": profile,
        "upcoming_classes": upcoming_classes,
        "recent_history": recent_history,
        "total_classes": total_classes,
        "completed_count": completed_count,
        "coverage": round(coverage, 1),
        "total_students": total_students,
        "homework_list": homework_list,
        "other_teachers": other_teachers,
        "students": students,
    }
    return render(request, "teachers/teacher-dashboard.html", context)


@login_required
def manage_teacher_profile(request):
    if not _require_teacher(request.user):
        return HttpResponseForbidden()

    profile, _ = TeacherProfile.objects.get_or_create(user=request.user)
    form = TeacherProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("teacher_profile")
    return render(request, "teachers/manage-profile.html", {"form": form})


@login_required
def manage_schedules(request):
    if not _require_teacher(request.user):
        return HttpResponseForbidden()

    form = ClassScheduleForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        schedule = form.save(commit=False)
        schedule.teacher = request.user
        schedule.save()
        messages.success(request, "Class schedule saved.")
        return redirect("teacher_schedules")

    schedules = ClassSchedule.objects.filter(teacher=request.user)
    return render(
        request,
        "teachers/manage-schedules.html",
        {"form": form, "schedules": schedules},
    )


@login_required
def manage_homework(request):
    if not _require_teacher(request.user):
        return HttpResponseForbidden()

    form = HomeworkForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        homework = form.save(commit=False)
        homework.teacher = request.user
        homework.save()
        messages.success(request, "Homework record saved.")
        return redirect("teacher_homework")

    homework_items = Homework.objects.filter(teacher=request.user)
    return render(
        request,
        "teachers/manage-homework.html",
        {"form": form, "homework_items": homework_items},
    )


@login_required
def mark_notification_as_read(request):
    if request.method == "POST":
        notification = Notification.objects.filter(user=request.user, is_read=False)
        notification.update(is_read=True)
        return JsonResponse({"status": "success"})
    return HttpResponseForbidden()


@login_required
def clear_all_notification(request):
    if request.method == "POST":
        notification = Notification.objects.filter(user=request.user)
        notification.delete()
        return JsonResponse({"status": "success"})
    return HttpResponseForbidden()