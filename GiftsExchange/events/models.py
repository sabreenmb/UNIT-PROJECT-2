from django.db import models
from accounts.models import User
# Create your models here.

class Event(models.Model):

    event_organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    event_title = models.CharField(max_length=1024)
    event_date = models.DateField()
    event_description = models.CharField(max_length=2048)
    event_min_budget = models.IntegerField(default=10)
    event_max_budget = models.IntegerField()
    is_draw = models.BooleanField(default=False)

    def __str__(self):
        return self.event_title


# class Participant(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Each user is a participant
#     wishlist = models.JSONField(default=dict)  # Store wishlist as a JSON field

#     def __str__(self):
#         return self.user.username


# class DrawResult(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='draw_results')
#     result_data = models.JSONField(default=dict)  # Store draw results as a JSON field

#     def __str__(self):
#         return f"Draw Results for {self.event.event_title}"


