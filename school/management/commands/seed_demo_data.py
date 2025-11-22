import random
import string
from datetime import date, time, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from home_auth.models import CustomUser
from school.models import ClassSchedule, Homework, TeacherProfile
from student.models import Parent, Student


class Command(BaseCommand):
    help = "Populate the database with demo teachers, students, schedules and homework."

    def add_arguments(self, parser):
        parser.add_argument(
            "--teachers",
            type=int,
            default=15,
            help="Number of teacher accounts to seed (default: 15)",
        )
        parser.add_argument(
            "--students",
            type=int,
            default=100,
            help="Number of students to seed (default: 100)",
        )

    def handle(self, *args, **options):
        target_teachers = options["teachers"]
        target_students = options["students"]

        with transaction.atomic():
            teachers = self._seed_teachers(target_teachers)
            self._seed_students(target_students)
            self._seed_schedules_and_homework(teachers)

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))

    # -------------------------------
    # Teacher helpers
    # -------------------------------
    def _seed_teachers(self, target):
        existing = list(CustomUser.objects.filter(is_teacher=True, is_admin=False))
        if len(existing) >= target:
            self.stdout.write(f"Already have {len(existing)} teachers. Skipping creation.")
            for teacher in existing:
                TeacherProfile.objects.get_or_create(user=teacher)
            return existing

        templates = [
            ("Aisha", "Shrestha", "Science", "Physics"),
            ("Bikash", "Adhikari", "Mathematics", "Calculus"),
            ("Pratima", "Koirala", "Languages", "English"),
            ("Suresh", "Maharjan", "Humanities", "History"),
            ("Nisha", "Gurung", "Computer Science", "Programming"),
            ("Kamal", "Thapa", "Science", "Biology"),
            ("Ritika", "Rai", "Mathematics", "Algebra"),
            ("Ganesh", "Bhattarai", "Languages", "Nepali"),
            ("Sunita", "Bista", "Humanities", "Civics"),
            ("Pawan", "Basnet", "Computer Science", "Robotics"),
        ]

        password = "demoPass123"
        created_teachers = []
        for idx in range(target - len(existing)):
            first, last, department, subject = templates[idx % len(templates)]
            serial = len(existing) + idx + 1
            email = f"{slugify(first)}.{slugify(last)}{serial}@sms-nepal.edu"
            user, created = CustomUser.objects.get_or_create(
                username=email,
                defaults=dict(
                    email=email,
                    first_name=first,
                    last_name=last,
                    is_teacher=True,
                    is_admin=False,
                ),
            )
            if created:
                user.set_password(password)
                user.save()

            profile, _ = TeacherProfile.objects.get_or_create(user=user)
            profile.title = "Subject Teacher"
            profile.department = department
            profile.subject_specialty = subject
            profile.experience_years = random.randint(3, 15)
            profile.phone = self._random_nepali_phone()
            profile.bio = (
                f"{first} {last} has been inspiring students across Nepal through "
                f"engaging {subject.lower()} lessons."
            )
            profile.save()
            created_teachers.append(user)

        self.stdout.write(f"Created {len(created_teachers)} teacher accounts.")
        return list(CustomUser.objects.filter(is_teacher=True, is_admin=False))

    # -------------------------------
    # Student helpers
    # -------------------------------
    def _seed_students(self, target):
        current = Student.objects.count()
        if current >= target:
            self.stdout.write(f"Already have {current} students. Skipping student creation.")
            return

        male_names = [
            "Aarav",
            "Sushan",
            "Bibek",
            "Prabesh",
            "Rohan",
            "Bijay",
            "Kiran",
            "Pratik",
            "Sudip",
            "Roshan",
        ]
        female_names = [
            "Aditi",
            "Sanjana",
            "Nitika",
            "Smriti",
            "Anu",
            "Bhawana",
            "Isha",
            "Kabita",
            "Reema",
            "Diya",
        ]
        surnames = [
            "Shrestha",
            "Gurung",
            "Khadka",
            "Magar",
            "Rai",
            "Thapa",
            "Poudel",
            "Bhattarai",
            "KC",
            "Basnet",
        ]

        father_names = [
            "Hari Bahadur",
            "Madan Prasad",
            "Dinesh Kumar",
            "Ramchandra",
            "Laxman",
            "Parmanand",
            "Kishor",
            "Mahesh",
            "Ramesh",
            "Krishna",
        ]
        mother_names = [
            "Laxmi",
            "Goma",
            "Radha",
            "Saraswati",
            "Mina",
            "Sita",
            "Kamala",
            "Parbati",
            "Sarita",
            "Gita",
        ]
        districts = [
            "Kathmandu",
            "Lalitpur",
            "Bhaktapur",
            "Pokhara",
            "Chitwan",
            "Biratnagar",
            "Dharan",
            "Butwal",
            "Hetauda",
            "Janakpur",
        ]

        genders = ["Male", "Female"]
        religions = ["Hindu", "Buddhist", "Christian", "Muslim"]
        classes = [f"Grade {i}" for i in range(1, 13)]
        sections = list(string.ascii_uppercase[:5])  # A-E

        needed = target - current
        for idx in range(needed):
            gender = random.choice(genders)
            if gender == "Male":
                first_name = random.choice(male_names)
            else:
                first_name = random.choice(female_names)
            last_name = random.choice(surnames)

            father = random.choice(father_names) + f" {random.choice(surnames)}"
            mother = random.choice(mother_names) + f" {random.choice(surnames)}"
            district = random.choice(districts)

            dob = date(
                random.randint(2008, 2016),
                random.randint(1, 12),
                random.randint(1, 28),
            )
            joining_date = timezone.now().date() - timedelta(days=random.randint(30, 900))
            student_class = random.choice(classes)
            section = random.choice(sections)

            parent = Parent.objects.create(
                father_name=father,
                father_occupation=random.choice(
                    ["Engineer", "Farmer", "Teacher", "Entrepreneur", "Civil Servant"]
                ),
                father_mobile=self._random_nepali_phone(),
                father_email=self._random_email(father),
                mother_name=mother,
                mother_occupation=random.choice(
                    ["Homemaker", "Nurse", "Lecturer", "Entrepreneur", "Banker"]
                ),
                mother_mobile=self._random_nepali_phone(),
                mother_email=self._random_email(mother),
                present_address=f"{district} - {random.randint(1, 30)}",
                permanent_address=f"{district}, Nepal",
            )

            current_count = Student.objects.count() + 1
            student_id = f"STD{timezone.now().year}{current_count:04d}"

            Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                gender=gender,
                date_of_birth=dob,
                student_class=student_class,
                religion=random.choice(religions),
                joining_date=joining_date,
                mobile_number=self._random_nepali_phone(),
                admission_number=f"ADM{timezone.now().year}{current_count:04d}",
                section=section,
                parent=parent,
            )

        self.stdout.write(f"Created {needed} student records.")

    # -------------------------------
    # Schedule & Homework helpers
    # -------------------------------
    def _seed_schedules_and_homework(self, teachers):
        subjects = [
            "Mathematics",
            "English",
            "Physics",
            "Chemistry",
            "Biology",
            "History",
            "Geography",
            "Computer Science",
        ]
        today = timezone.localdate()

        for teacher in teachers:
            # Ensure profile exists
            profile, _ = TeacherProfile.objects.get_or_create(user=teacher)
            profile.department = profile.department or random.choice(
                ["Science", "Mathematics", "Languages", "Humanities", "ICT"]
            )
            profile.subject_specialty = profile.subject_specialty or random.choice(subjects)
            profile.phone = profile.phone or self._random_nepali_phone()
            profile.save()

            existing_schedules = ClassSchedule.objects.filter(teacher=teacher).count()
            to_create = max(0, 3 - existing_schedules)
            for i in range(to_create):
                ClassSchedule.objects.create(
                    teacher=teacher,
                    date=today + timedelta(days=random.randint(1, 14)),
                    start_time=time(hour=8 + i, minute=0),
                    end_time=time(hour=9 + i, minute=0),
                    class_name=f"Grade {random.randint(5, 12)}",
                    topic=f"{profile.subject_specialty or random.choice(subjects)} - Lesson {i+1}",
                    total_students=random.randint(30, 45),
                    present_students=random.randint(25, 40),
                    syllabus_coverage=random.randint(40, 95),
                    status=random.choice(["scheduled", "completed"]),
                    notes="Automatically generated through seed_demo_data.",
                )

            existing_homework = Homework.objects.filter(teacher=teacher).count()
            to_create_hw = max(0, 2 - existing_homework)
            for i in range(to_create_hw):
                Homework.objects.create(
                    teacher=teacher,
                    title=f"{profile.subject_specialty or random.choice(subjects)} Assignment {i+1}",
                    subject=profile.subject_specialty or random.choice(subjects),
                    class_name=f"Grade {random.randint(5, 12)}",
                    description="Review classroom notes and prepare for next assessment.",
                    due_date=today + timedelta(days=random.randint(3, 10)),
                    status=random.choice(["assigned", "in_review", "completed"]),
                    completed_count=random.randint(10, 30),
                    pending_count=random.randint(5, 15),
                )

    # -------------------------------
    # Utilities
    # -------------------------------
    def _random_nepali_phone(self):
        prefix = random.choice(["981", "984", "985", "986", "974"])
        return prefix + "".join(random.choices(string.digits, k=7))

    def _random_email(self, full_name):
        user = slugify(full_name.replace(" ", "."))
        return f"{user}@example.com"

