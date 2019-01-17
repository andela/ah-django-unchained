from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to allow only owners of an object to edit it
    """
    message = "You are not allowed to edit or delete this object"

    def has_object_permission(self, request, view, obj):
        # read permissions are allowed to any request
        # so we will allow GET, HEAD or OPTIONS requests
        if request.method in SAFE_METHODS:
            return True

        # write permission is only allowed to the owner of the object
        return obj.author == request.user


class IsNotAuthorOrReadOnly(BasePermission):
    """
    Custom permission to ensure that an author cannot rate their own article
    """
    message = "You are not allowed to rate your own article"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Rating permission is allowed to all other users except the owner
        # The article owner will only be allowed GET
        return obj.author != request.user


class IsMyProfileOrReadOnly(BasePermission):
    """
    Custom permission to allow only owners of an object to edit it
    """
    message = "You are not allowed to edit or delete this object"

    def has_object_permission(self, request, view, obj):
        # read permissions are allowed to any request
        # so we will allow GET, HEAD or OPTIONS requests
        if request.method in SAFE_METHODS:
            return True

        # write permission is only allowed to the owner of the object
        print(obj)
        return obj.user.username == request.user.username
