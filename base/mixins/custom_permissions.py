# -*- coding: UTF-8 -*-
from rest_framework import permissions
from project.models import ProjectMember

class PermissionClassesByAction():
    # Viewset에서 각 메소드 별로 퍼미션을 다르게 설정
    """
    ex.
    {'create': [IsAdminUser]
    'default': [IsAuthenticated]}
    """
    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes_by_action['default']]


class IsProjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, project):
        owner = ProjectMember.objects.filter(project=project, role='owner').first()
        owner_user = owner.user
        return owner_user == request.user


class IsProjectAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, project):
        user = request.user
        project_admins = ProjectMember.objects.filter(project=project, role='admin', user=user, )
        return project_admins.exists()


class IsProjectMember(permissions.BasePermission):
    def has_object_permission(self, request, view, project):
        user = request.user
        project_members = ProjectMember.objects.filter(project=project, user=user, )
        return project_members.exists()