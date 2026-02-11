import datetime
from celery import shared_task, group
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject="Book Loaned Successfully",
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans(self):

    loans_extended_due_date = Loan.objects.filter(
        due_date__lte=datetime.date.today()
    ).only("id")

    lazy_group = group(
        [send_loan_notification.s(loan.id) for loan in loans_extended_due_date]
    )

    promise = lazy_group()

    promise.get()

    for loan in Loan.objects.filter(due_date__lte=datetime.date.today()):
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject="Book Loaned Successfully",
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
