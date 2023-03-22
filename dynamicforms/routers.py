from typing import Optional, Set

from rest_framework.routers import DefaultRouter, Route

from dynamicforms.viewsets import SingleRecordViewSet


class DFRouter(DefaultRouter):
    single_record_registrations: Set[int] = set()

    def register_single_record(self, prefix: str, viewset: SingleRecordViewSet, basename: Optional[str] = None):
        """
        Register a single-record viewset with the router.
        """
        self.single_record_registrations.add(id(viewset))
        self.register(prefix, viewset, basename)

    def get_routes(self, viewset):
        if id(viewset) in self.single_record_registrations:
            # these routes are copied from SimpleRouter, but modified so that they don't ask for a parameter
            return [
                Route(
                    url=r"^{prefix}{trailing_slash}$",
                    mapping={
                        "post": "create",
                        "get": "retrieve",
                        "put": "update",
                        "patch": "partial_update",
                        "delete": "destroy",
                    },
                    name="{basename}-detail",
                    detail=True,
                    initkwargs={"suffix": "Instance"},
                ),
            ]
        return super().get_routes(viewset)
