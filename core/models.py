from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import DEFAULT_ELEVATOR_DIRECTION

# Create your models here.

class Elevator(models.Model):

    DIRECTION_CHOICES = (
        ('upwards','upwards'),
        ('downwards','downwards'),
        ('idle','idle'),
    )

    direction = models.CharField(
        max_length=10,
        default=DEFAULT_ELEVATOR_DIRECTION,
        choices=DIRECTION_CHOICES,
        help_text=_(
            'Direction in which the elevator is moving.'
        )
    )
    next_destination = models.IntegerField(
        null=True,
        blank=True,
        help_text=_(
            'Next Floor Destination.'
        )
    )
    is_down = models.BooleanField(
        default=False,
        help_text=_(
            'Tells if the elevator is working or under maintenance.'
        )
    )

    class Meta:
        verbose_name = 'Elevator'
        verbose_name_plural = 'Elevators'
        db_table = 'elevator'

    def __str__(self):
        return "elevator_" + str(self.id)


class ElevatorRequests(models.Model):

    elevator = models.ForeignKey(
        Elevator,
        on_delete=models.PROTECT
    )
    requested_floor = models.IntegerField(
        help_text=_(
            'Requested Floor Number.'
        )
    )
    is_completed = models.BooleanField(
        default=False,
        help_text=_(
            'Tells if the request has been completed or not.'
        )
    )
    created_at =  models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'elevator request'
        verbose_name_plural = 'elevator requests'
        db_table = 'elevator_request'
