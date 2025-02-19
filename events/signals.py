from events.models import *
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(m2m_changed, sender=Event.rsvp.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_email = [] #all assigned email for a task
        for emp in instance.rsvp.all():
            assigned_email.append(emp.email)
        send_mail(
            "New Event Assignment",
            f""" We are pleased to inform you that you have been assigned to the following event:
            Event Name: {instance.name}
            Date & Time: {instance.date} {instance.time}
            Location: {instance.location}
            """,
            "anisulalam2003@gmail.com",
            assigned_email,
        )

pass