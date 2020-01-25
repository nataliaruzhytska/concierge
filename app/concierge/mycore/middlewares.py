from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now as django_now


class SimpleMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.start_render_time = django_now()
        print(f"we start rendering at {request.start_render_time}")

    def process_response(self, request, response):
        finish_time = django_now()
        request.start_render_time = django_now()
        print(f"we stop rendering at {finish_time}")
        result = finish_time - request.start_render_time
        print(result.seconds)
        return response
