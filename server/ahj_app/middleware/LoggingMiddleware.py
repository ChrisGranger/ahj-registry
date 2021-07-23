from request_logging.middleware import LoggingMiddleware


class SkipRequestLoggingMiddleware(LoggingMiddleware):
    """
    Inherits from django-request-logging's LoggingMiddleware:
    https://github.com/Rhumbix/django-request-logging/blob/master/request_logging/middleware.py#L73
    """

    def __call__(self, request):
        """
        Overridden to skip calling ``self.process_request(request, response)``.
        Requests are not logged anymore; only responses to requests are logged.
        """
        self.cached_request_body = request.body
        response = self.get_response(request)
        if not hasattr(request, 'auth'):
            """
            LOGGING in settings.py wants a request.auth but this is only set
            by Django Rest Framework views. This sets the request.auth attribute
            for standard Django views, such as Admin Dashboard to prevent log errors.
            """
            setattr(request, 'auth', None)
        self.process_response(request, response)
        return response
