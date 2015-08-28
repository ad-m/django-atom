class UserKwargFilterSetMixin(object):

    def get_filterset_kwargs(self, *args, **kwargs):
        kwargs = super(UserKwargFilterSetMixin, self).get_filterset_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs
