from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'image', 'created_at', 'updated_at']
        read_only_fields = ('owner',) # owner is set in the view
