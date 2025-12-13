from rest_framework.routers import Route

from src.apps.common.routers import CustomRouter


class CustomSellersRouter(CustomRouter):
    routes = CustomRouter.routes + [
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'get_by_id',
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'},
        ),
    ]
