from django import forms
from .models import TeacherProfile, ClassSchedule, Homework


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = [
            "title",
            "department",
            "subject_specialty",
            "experience_years",
            "phone",
            "bio",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }


class ClassScheduleForm(forms.ModelForm):
    class Meta:
        model = ClassSchedule
        fields = [
            "date",
            "start_time",
            "end_time",
            "class_name",
            "topic",
            "total_students",
            "present_students",
            "syllabus_coverage",
            "status",
            "notes",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = [
            "title",
            "subject",
            "class_name",
            "description",
            "due_date",
            "status",
            "completed_count",
            "pending_count",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

