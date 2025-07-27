from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import StandardResultsSetPagination

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsParticipantOfConversation]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter


    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(conversation__participants=self.request.user)