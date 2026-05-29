from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Student


@receiver(m2m_changed, sender=Student.courses.through)
def notify_instructor_on_enrollment(sender, instance, action, pk_set, **kwargs):
    """
    Student.courses.add(course) chaqirilganda bu signal ishlaydi.
    Instruktorga yangi o'quvchi haqida email jo'natiladi.
    """
    if action != 'post_add':  # Faqat qo'shishdan keyin
        return

    if not pk_set:  
        return

    from courses.models import Course
    for course_id in pk_set:
        try:
            course = Course.objects.select_related('instructor').get(pk=course_id)
            instructor = course.instructor
            student = instance.user

            send_mail(
                subject=f"🎓 Yangi o'quvchi: {course.title}",
                message=(
                    f"Assalomu alaykum, {instructor.username}!\n\n"
                    f"'{course.title}' kursingizga yangi o'quvchi qo'shildi:\n"
                    f"O'quvchi: {student.username} ({student.email})\n\n"
                    f"Platformani tekshiring! 🌟"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instructor.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Signal xatosi: {e}")