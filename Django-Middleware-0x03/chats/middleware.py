# chats/middleware.py
import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from django.http import JsonResponse, HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(filename='requests.log', level=logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_msg = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_msg)
        return self.get_response(request)
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if request.path.startswith('/chats/') and (current_hour < 18 or current_hour >= 21):
            return HttpResponseForbidden("Access to chat is restricted between 9 PM and 6 PM.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        now = time.time()

        if request.method == 'POST' and request.path.startswith('/chats/'):
            if ip not in self.requests:
                self.requests[ip] = []
            self.requests[ip] = [t for t in self.requests[ip] if now - t < 60]  # last 60 sec
            if len(self.requests[ip]) >= 5:
                return JsonResponse({'error': 'Rate limit exceeded. Max 5 messages/min.'}, status=429)
            self.requests[ip].append(now)

        return self.get_response(request)
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/chats/') and request.user.is_authenticated:
            role = getattr(request.user, 'role', 'guest')
            if role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Permission denied: You must be admin or moderator.")
        return self.get_response(request)