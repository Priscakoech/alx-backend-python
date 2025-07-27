from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants in a conversation to view, edit, or delete messages.
    """

    def has_object_permission(self, request, view, obj):
        # If obj is a conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # If obj is a message with a related conversation
        if hasattr(obj, 'conversation') and hasattr(obj.conversation, 'participants'):
            return request.user in obj.conversation.participants.all()

        return False
