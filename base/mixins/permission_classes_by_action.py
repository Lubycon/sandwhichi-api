# -*- coding: UTF-8 -*-

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