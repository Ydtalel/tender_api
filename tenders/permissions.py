from rest_framework.permissions import BasePermission
from .models import OrganizationResponsible


class IsOrganizationResponsible(BasePermission):
    """Проверяет, что пользователь является ответственным за организацию"""

    def has_permission(self, request, view):
        organization_id = request.data.get('organization')
        creator_id = request.data.get('creator')
        if not organization_id or not creator_id:
            return False
        return OrganizationResponsible.objects.filter(
            user_id=creator_id, organization_id=organization_id
        ).exists()


class IsTenderCreatorOrResponsible(BasePermission):
    """
    Проверяет, что пользователь является автором или ответственным за
    организацию
    """

    def has_object_permission(self, request, view, obj):
        creator_id = request.data.get('creator')
        is_creator = obj.creator_id == creator_id
        is_responsible = OrganizationResponsible.objects.filter(
            user_id=creator_id, organization=obj.organization
        ).exists()

        return is_creator or is_responsible
