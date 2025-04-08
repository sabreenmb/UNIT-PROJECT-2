import random
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
    
    def draw_participants(self):
        # Step 1: Remove placeholders
        PlaceholderParticipant.objects.filter(event=self).delete()

        # Step 2: Get valid participants
        valid_participants = list(self.participants.all())

        # Step 3: Check if enough participants to draw
        if len(valid_participants) < 3:
            raise ValueError("Not enough valid participants to draw!")

        # Step 4: Shuffle participants
        random.shuffle(valid_participants)

        # Step 5: Create a mapping of drawn names, ensuring no self-selection
        for participant in valid_participants:
            # Filter out the current participant from the potential draw names
            potential_draws = [p for p in valid_participants if p.user != participant.user]

            if not potential_draws:
                raise ValueError("Cannot draw names; insufficient unique participants.")

            # Randomly select a name from potential draws
            drawn_participant = random.choice(potential_draws)

            # Assign selected drawn name to the participant
            participant.drawn_name = drawn_participant.user
            participant.save()  # Save the participant instance
            self.is_draw=True
            self.save()



class PlaceholderParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='placeholder_participants')
    name = models.CharField(max_length=200)  # Placeholder for participant's name
    email = models.EmailField(unique=True)  # Placeholder for participant's email

    def __str__(self):
        return f"{self.name} ({self.email})"
    
class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')  # Each event can have multiple participants
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participants',default=None)  # A user can participate in multiple events
    wishlist = models.JSONField(default=list)  # Store wishlist as a list instead of a dictionary
    drawn_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drawn_names', null=True, blank=True)  # Nullable field to store the drawn name
    def __str__(self):
        return f"{self.user.username} in {self.event.event_title} {self.wishlist}"
    

# class DrawResult(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='draw_results')
#     result_data = models.JSONField(default=dict)  # Store draw results as a JSON field

#     def __str__(self):
#         return f"Draw Results for {self.event.event_title}"


