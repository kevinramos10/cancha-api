from django.urls import path
from gestion.views.sede_view import SedeView, SedesView
from gestion.views.cancha_view import CanchaView, CanchasView

urlpatterns = [
    path('sedes', SedesView.as_view()), path('sede/<uuid:id>', SedeView.as_view()),
    path('canchas', CanchasView.as_view()), path('cancha/<uuid:id>', CanchaView.as_view())
]
