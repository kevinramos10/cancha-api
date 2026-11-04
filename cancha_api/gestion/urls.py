from django.urls import path
from gestion.views.sede_view import SedeView, SedesView

urlpatterns = [
    path('sedes', SedesView.as_view()), path('sede/<uuid:id>', SedeView.as_view())
]
