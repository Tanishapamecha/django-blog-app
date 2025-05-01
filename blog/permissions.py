# blog/permissions.py

from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post/comment to edit or delete it.
    All other users can only view (read) posts/comments.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are granted to any request, so we'll allow GET, HEAD, and OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are granted only to the author of the post/comment.
        return obj.author == request.user
