from datetime import datetime, timedelta

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from quiz.models import Question
from quiz.test_helpers import create_questions


class AutoPublishTest(TestCase):

    def test_publishes_scheduled_question_from_the_past(self):
        past = timezone.now() - timedelta(hours=1)
        [q] = create_questions(1, state="SCH", publish_time=past)
        call_command("auto_publish", "--skip-tweet")
        self.assertEqual("PUB", Question.objects.get(pk=q.pk).state)

    def test_does_not_publish_unscheduled_question_from_the_past(self):
        past = timezone.now() - timedelta(hours=1)
        [q] = create_questions(1, state="ACC", publish_time=past)
        call_command("auto_publish", "--skip-tweet")
        self.assertEqual("ACC", Question.objects.get(pk=q.pk).state)

    def test_does_not_publish_scheduled_question_from_the_future(self):
        future = timezone.now() + timedelta(hours=1)
        [q] = create_questions(1, state="SCH", publish_time=future)
        call_command("auto_publish", "--skip-tweet")
        self.assertEqual("SCH", Question.objects.get(pk=q.pk).state)
