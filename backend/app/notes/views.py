from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from .models import Note
from .serializers import NoteSerializer
from shared.permissions import IsAuthenticatedForWrite

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    #permission_classes = [IsAuthenticatedForWrite]
