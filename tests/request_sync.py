import time


class RequestSyncMiddleware:
    sync_url_mutexes = {}

    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

    def __call__(self, request):
        # We check if there are any mutexes defined. if so, let's wait until they are cleared
        # the view (and later middleware) are called.

        def process_mutex(pth, mutex_key, mutex_passes):
            if mutex_key in pth:
                if mutex_passes == 0:
                    return True
                RequestSyncMiddleware.sync_url_mutexes[mutex_key] -= 1

        pth = request.path
        while any(
            map(
                lambda mutex_item: process_mutex(pth, mutex_item[0], mutex_item[1]),
                RequestSyncMiddleware.sync_url_mutexes.items(),
            )
        ):
            # print('waiting for mutex to be removed...')
            time.sleep(0.1)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    @staticmethod
    def add_sync_url_mutex(partial_path, passes_to_let_through: int = 0):
        RequestSyncMiddleware.sync_url_mutexes[partial_path] = passes_to_let_through

        class WithClass:
            def __enter__(self):
                pass

            def __exit__(self, exc_type, exc_val, exc_tb):
                RequestSyncMiddleware.clear_sync_url_mutex(partial_path)

        return WithClass()

    @staticmethod
    def clear_sync_url_mutex(partial_path):
        RequestSyncMiddleware.sync_url_mutexes.pop(partial_path, None)
