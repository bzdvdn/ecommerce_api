from .auth import Auth
from .pagination import resolve_paginated


class CustomAuthMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        info.context.user = self.authorize_user(info)
        return next(root, info, **kwargs)

    @staticmethod
    def authorize_user(info):
        auth = Auth(info.context)
        return auth.authenticate()


class CustomPaginationMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        try:
            is_paginated = info.return_type.name.endswith('Paginated')
        except Exception:
            is_paginated = False

        if is_paginated:
            page = kwargs.pop("page", 1)
            page_size = kwargs.pop("page_size", 1)
            return resolve_paginated(
                next(root, info, **kwargs).value, info, page, page_size
            )

        return next(root, info, **kwargs)
