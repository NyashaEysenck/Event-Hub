import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f'Exception occurred: {exception}', exc_info=True)
        # You can customize the response here
        return JsonResponse({'error': 'An error occurred, please try again later.'}, status=500)
