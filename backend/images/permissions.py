from rest_framework.permissions import BasePermission

class IsBasic(BasePermission):
    message = 'You must be authenticated to view this resource'
    
    def has_permission(self, request, view):
        return request.user.userprofile.tier.name == 'Basic'

class IsPremium(BasePermission):
    message = 'You must be Premium User to view this resource'
    
    def has_permission(self, request, view):
        return request.user.userprofile.tier.name == 'Premium'

class IsEnterprise(BasePermission):
    message = 'You must be Enterprise User to view this resource'
    
    def has_permission(self, request, view):
        return request.user.userprofile.tier.name == 'Enterprise'
    
class IsCustom(BasePermission):
    message = 'You must be authenticate to view this resource'
    
    def has_permission(self, request, view):
        return request.user.userprofile.tier.name not in ['Basic', 'Premium', 'Enterprise']
    

class CanFetchExpiringLink(BasePermission):
    message = 'You cannot create expiring Links'

    def has_permission(self, request, view):
        return request.user.userprofile.tier.expiring_urls == True