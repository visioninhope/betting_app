
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from ..models import Group, Member
from ..serializer import GroupSerializer, MemberSerializer


class GroupViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.prefetch_related("members__user").all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
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
        new_member = Member.objects.create(group=group, user=user)

        # Serialize the newly created member to return its data, including userId data is used to flip the isMember state when joining a group
        new_member_data = MemberSerializer(new_member).data

        return Response(
            {"message": "Successfully joined the group",
            "member": new_member_data},
            status=status.HTTP_200_OK
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

