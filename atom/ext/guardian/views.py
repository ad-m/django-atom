from braces.mixins import LoginRequiredMixin  # django.contrib.auth.mixins lack of redirect_unauthenticated_users
from guardian.mixins import PermissionRequiredMixin


class RaisePermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """Mixin to verify object permission with preserve correct status code in view
    """
    raise_exception = True
    redirect_unauthenticated_users = True


class AttrPermissionRequiredMixin(RaisePermissionRequiredMixin):
    """Mixin to verify object permission in SingleObjectView
    Attributes:
        permission_attribute (str): A path to traverse from object to permission object
    """
    permission_attribute = None

    @staticmethod
    def _resolve_path(obj, path=None):
        """Resolve django-like path eg. object2__object3 for object
        Args:
            obj: The object the view is displaying.
            path (str, optional): Description
        Returns:
            A oject at end of resolved path
        """
        if path:
            for attr_name in path.split('__'):
                obj = getattr(obj, attr_name)
        return obj

    def get_permission_object(self):
        obj = super(AttrPermissionRequiredMixin, self).get_object()
        return self._resolve_path(obj, self.permission_attribute)

    def get_object(self):
        if not hasattr(self, 'object'):
            self.object = super(AttrPermissionRequiredMixin, self).get_object()
        return self.object
