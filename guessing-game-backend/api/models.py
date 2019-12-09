import random

from django.db import models
from lib.models import BaseModel


class Game(BaseModel):
    def random_number():
        return random.randint(1, 50)

    # 1 <= number <= 100
    # PositiveSmallIntegerField can store 0 - 32767
    number = models.PositiveSmallIntegerField(default=random_number)
    question_limit = models.PositiveSmallIntegerField(default=5)

class Question(BaseModel):
    # number can be null if for questions like "is even"
    number = models.PositiveSmallIntegerField(blank=True, null=True)
    type = models.CharField(max_length=10)
    is_correct = models.BooleanField()
    # stores the primary key of a Game
    # related_name property allows the reverse lookup of
    # all Question objects from a Game instance
    game = models.ForeignKey(
        'Game',
        related_name='questions',
        on_delete=models.CASCADE,
    )

class Guess(BaseModel):
    number = models.PositiveSmallIntegerField()
    game = models.OneToOneField('Game', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "guesses"
