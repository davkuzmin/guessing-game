from rest_framework import serializers

from .models import *


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        exclude = ['number'] # don't reveal the mystery number

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class GuessSerializer(serializers.ModelSerializer):
    is_correct = serializers.SerializerMethodField(read_only=True)

    def get_is_correct(self, guess):
        return guess.game.number == guess.number

    class Meta:
        model = Guess
        fields = ['game', 'number', 'is_correct']
