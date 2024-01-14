from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):


    #custom permission to only allows owners of an object to edit it
    def has_object_permission(self, request, view, obj):
        #Read permissions are allowed to any request
        #so we will always allow 'GET', 'HEAD' or 'OPTIONS' request

        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user