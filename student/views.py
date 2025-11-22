from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from .models import Parent, Student
from school.models import Notification


def _ensure_staff_access(request):
    if not (request.user.is_admin or request.user.is_teacher):
        raise PermissionDenied("You do not have permission to access this page.")


def create_notification(user, message):
    if user.is_authenticated:
        Notification.objects.create(user=user, message=message)


@login_required
def add_student(request):
    _ensure_staff_access(request)
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')

        # Retrieve parent data from the form
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, "A student with this ID already exists.")
            return redirect("add_student")

        # save parent information
        parent = Parent.objects.create(
            father_name= father_name,
            father_occupation= father_occupation,
            father_mobile= father_mobile,
            father_email= father_email,
            mother_name= mother_name,
            mother_occupation= mother_occupation,
            mother_mobile= mother_mobile,
            mother_email= mother_email,
            present_address= present_address,
            permanent_address= permanent_address
        )

        # Save student information
        student = Student.objects.create(
            first_name= first_name,
            last_name= last_name,
            student_id= student_id,
            gender= gender,
            date_of_birth= date_of_birth,
            student_class= student_class,
            religion= religion,
            joining_date= joining_date,
            mobile_number = mobile_number,
            admission_number = admission_number,
            section = section,
            student_image = student_image,
            parent = parent
        )
        create_notification(request.user, f"Added student: {student.first_name} {student.last_name}")
        messages.success(request, "Student added Successfully")
        return redirect("student_list")

    return render(request, "students/add-student.html")


@login_required
def student_list(request):
    _ensure_staff_access(request)
    student_list = Student.objects.select_related('parent').all()
    context = {
        'student_list': student_list,
    }
    return render(request, "students/students.html", context)


@login_required
def edit_student(request,slug):
    _ensure_staff_access(request)
    student = get_object_or_404(Student, slug=slug)
    parent = student.parent if hasattr(student, 'parent') else None
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')  if request.FILES.get('student_image') else student.student_image

        if Student.objects.exclude(pk=student.pk).filter(student_id=student_id).exists():
            messages.error(request, "A student with this ID already exists.")
            return redirect("edit_student", slug=student.slug)

        # Retrieve parent data from the form
        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')
        parent.save()

        # update student information
        student.first_name= first_name
        student.last_name= last_name
        student.student_id= student_id
        student.gender= gender
        student.date_of_birth= date_of_birth
        student.student_class= student_class
        student.religion= religion
        student.joining_date= joining_date
        student.mobile_number = mobile_number
        student.admission_number = admission_number
        student.section = section
        student.student_image = student_image
        student.save()
        create_notification(request.user, f"Updated student: {student.first_name} {student.last_name}")
        messages.success(request, "Student updated successfully")
        
        return redirect("student_list")
    return render(request, "students/edit-student.html",{'student':student, 'parent':parent} )


@login_required
def view_student(request, slug):
    _ensure_staff_access(request)
    student = get_object_or_404(Student, slug=slug)
    context = {
        'student': student
    }
    return render(request, "students/student-details.html", context)


@login_required
def delete_student(request,slug):
    _ensure_staff_access(request)
    if request.method == "POST":
        student = get_object_or_404(Student, slug=slug)
        student_name = f"{student.first_name} {student.last_name}"
        student.delete()
        create_notification(request.user, f"Deleted student: {student_name}")
        messages.success(request, "Student deleted successfully")
        return redirect ('student_list')
    return HttpResponseForbidden()