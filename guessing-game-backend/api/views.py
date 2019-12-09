from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=True, url_path='guess')
    def get_guess(self, request, pk):
        game = self.get_object()
        data = None

        if hasattr(game, 'guess'):
            serializer = GuessSerializer(game.guess)
            data = serializer.data

        return Response(data)

    @action(detail=True, url_path='questions')
    def get_questions(self, request, pk):
        questions = self.get_object().questions
        serializer = QuestionSerializer(questions, many=True)

        return Response(serializer.data)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        number = request.data['number']
        type = request.data['type']

        game = Game.objects.get(pk=request.data['game'])

        # cannot exceed question limit per game (5 questions by default, defined in models.py)
        if game.questions.count() >= game.question_limit:
            content = { 'message': 'Question limit reached' }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # all question types except for "is even" must have a associated number
        if type != 'even' and number == None:
            content = { 'message': 'A number is required' }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        # find answer to question
        is_correct = None
        if type == '>':
            is_correct = game.number > number
        elif type == '>=':
            is_correct = game.number >= number
        elif type == '==':
            is_correct = game.number == number
        elif type == '<=':
            is_correct = game.number <= number
        elif type == '<':
            is_correct = game.number < number
        elif type == 'even':
            is_correct = game.number % 2 == 0
        else:
            content = { 'message': 'Invalid question type. Only ">", ">=", "==", "<=", "<", "even" supported.' }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        request.data['is_correct'] = is_correct
        return super(QuestionViewSet, self).create(request, args, kwargs)


class GuessViewSet(viewsets.ModelViewSet):
    queryset = Guess.objects.all()
    serializer_class = GuessSerializer

    def create(self, request, *args, **kwargs):
        game = Game.objects.get(pk=request.data['game'])

        if hasattr(game, 'guess'):
            content = { 'message': 'Only 1 guess is allowed per game' }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        return super(GuessViewSet, self).create(request, args, kwargs)
