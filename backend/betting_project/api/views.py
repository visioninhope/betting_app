from tokenize import group
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Group, Event, Member
from .serializer import (
    GroupSerializer,
    EventSerializer,
    FullGroupSerializer,
    MemberSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class GroupViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.prefetch_related("members__user").all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a group along with its members and events.
        """
        instance = self.get_object()
        serializer = FullGroupSerializer(
            instance, many=False, context={"request": request}
        )
        return Response(serializer.data)

    # /api/groups/{group_id}/join/ - auto generated by DRF Viewst class

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def join(self, request, pk=None):
        """
        Allow a user to join a group.
        """
        user = (
            request.user
        )  # The request.user attribute is populated by Django's authentication middleware, and it typically contains an instance of the authenticated user.
        group = get_object_or_404(Group, pk=pk)  # Get the group or return 404

        # Check if the user is already a member
        if group.members.filter(user=user).exists():
            return Response(
                {"message": "Already a member"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Create a new member
        Member.objects.create(group=group, user=user)
        return Response(
            {"message": "Successfully joined the group"}, status=status.HTTP_200_OK
        )

    # /api/groups/{group_id}/leave/ - auto generated by DRF Viewst class
    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def leave(self, request, pk=None):
        """
        Allow a user to leave a group.
        """
        user = request.user  # Get the authenticated user
        group = get_object_or_404(Group, pk=pk)  # Get the group (pk comes from URL)

        # Check if the user is a member
        try:
            member = group.members.get(user=user)
            member.delete()
            return Response(
                {"message": "Successfully left the group"}, status=status.HTTP_200_OK
            )
        except Member.DoesNotExist:
            return Response(
                {"message": "You are not a member of this group"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class EventViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer


class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows members to be viewed or edited.
    """

    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
