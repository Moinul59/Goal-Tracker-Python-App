from datetime import datetime, timedelta
from celery_app import celery
from flask import current_app

from flaskr.models import Goal, User
from flaskr.notifications.emailer import send_email
from flaskr.notifications.sms_sender import send_sms


@celery.task
def send_deadline_reminders():
    """
    Send email + SMS reminders for goals whose deadlines are
    within the next 6 hours.
    """
    now = datetime.now()
    threshold = now + timedelta(hours=6)

    # Query all goals due soon and not completed
    upcoming_goals = Goal.query.filter(
        Goal.is_completed.is_(False),
        Goal.due_date.isnot(None),
        Goal.due_date <= threshold,
        Goal.due_date >= now
    ).all()

    if not upcoming_goals:
        current_app.logger.info("No goals due within the next 6 hours.")
        return "No reminders sent"

    reminders_sent = 0

    for goal in upcoming_goals:
        user = User.query.get(goal.user_id)

        if not user:
            current_app.logger.warning(
                f"Goal {goal.id} has no associated user."
            )
            continue

        # Email/SMS message content
        reminder_msg = (
            f"Goal Reminder:\n"
            f"Goal: {goal.title}\n"
            f"Deadline: {goal.due_date}\n"
            f"Please complete your goal soon!"
        )

        # --- EMAIL ---
        if getattr(user, "email", None):
            try:
                send_email(
                    to_email=user.email,
                    subject="Goal Deadline Reminder",
                    body=reminder_msg
                )
                current_app.logger.info(
                    f"Email reminder sent → {user.email}"
                )
            except Exception as e:
                current_app.logger.error(
                    f"Email failed for {user.email}: {e}"
                )

        # --- SMS ---
        if hasattr(user, "phone") and user.phone:
            try:
                send_sms(
                    to_number=user.phone,
                    message=f"Reminder: Your goal '{goal.title}' is due soon!"
                )
                current_app.logger.info(
                    f"SMS reminder sent → {user.phone}"
                )
            except Exception as e:
                current_app.logger.error(
                    f"SMS failed for {user.phone}: {e}"
                )

        reminders_sent += 1

    current_app.logger.info(
        f"Deadline reminder task completed. Reminders sent: {reminders_sent}"
    )
    return f"Reminders sent: {reminders_sent}"

@celery.task
def send_test_email_task():
    from flaskr.notifications.emailer import send_email
    send_email("onlyforclashofclan2017@gmail.com", "Test Email", "This is a Celery email test!")
    return "Test email sent"


@celery.task
def send_test_sms_task():
    from flaskr.notifications.sms_sender import send_sms
    send_sms("+918777314531", "This is a Celery SMS test!")
    return "Test SMS sent"

