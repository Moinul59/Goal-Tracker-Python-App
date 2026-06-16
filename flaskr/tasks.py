from celery_app import celery
from flask import current_app

from flaskr.db import query_all
from flaskr.notifications.emailer import send_email


@celery.task
def send_deadline_reminders():
    """
    Send email reminders for goals whose deadlines
    are within the next 6 hours.
    """

    upcoming_goals = query_all(
        """
        SELECT
            g.id,
            g.title,
            g.due_date,
            u.email
        FROM goals g
        JOIN users u
            ON u.id = g.user_id
        WHERE
            g.is_completed = FALSE
            AND g.due_date IS NOT NULL
            AND g.due_date <= NOW() + INTERVAL '6 hours'
            AND g.due_date >= NOW()
        """
    )

    if not upcoming_goals:
        current_app.logger.info(
            "No goals due within the next 6 hours."
        )
        return "No reminders sent"

    reminders_sent = 0

    for goal in upcoming_goals:

        reminder_msg = (
            f"Goal Reminder:\n"
            f"Goal: {goal['title']}\n"
            f"Deadline: {goal['due_date']}\n"
            f"Please complete your goal soon!"
        )

        try:
            send_email(
                to_email=goal["email"],
                subject="Goal Deadline Reminder",
                body=reminder_msg
            )

            current_app.logger.info(
                f"Email reminder sent → {goal['email']}"
            )

            reminders_sent += 1

        except Exception as e:
            current_app.logger.error(
                f"Email failed for {goal['email']}: {e}"
            )

    current_app.logger.info(
        f"Deadline reminder task completed. "
        f"Reminders sent: {reminders_sent}"
    )

    return f"Reminders sent: {reminders_sent}"


@celery.task
def send_test_email_task():
    send_email(
        "onlyforclashofclan2017@gmail.com",
        "Test Email",
        "This is a Celery email test!"
    )

    return "Test email sent"