from django.urls import path, include

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register('games', GameViewSet)
router.register('questions', QuestionViewSet)
router.register('guesses', GuessViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
