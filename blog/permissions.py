from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to allow only authors to edit/delete their own posts or comments.
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET, HEAD, OPTIONS) for anyone
        if request.method in SAFE_METHODS:
            return True

        # Allow update/delete only to the author
        return obj.author == request.user

# GET     /api/comments/           -> list all comments
# POST    /api/comments/           -> create a comment
# GET     /api/comments/<id>/      -> retrieve a specific comment
# PUT     /api/comments/<id>/      -> update a comment
# DELETE  /api/comments/<id>/      -> delete a comment
