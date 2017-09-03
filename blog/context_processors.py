from django.utils import timezone

def blog(request):
    return {
        "Seoul" : timezone.now()
    }