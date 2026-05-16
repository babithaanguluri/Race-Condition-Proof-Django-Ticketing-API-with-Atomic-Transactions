import sys
import time
from django.db import transaction, models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Event, Booking

def log_confirmation(event_id):
    print(f"CONFIRMATION: Booking successful for event {event_id}", flush=True)

@csrf_exempt
def book_vulnerable(request, event_id):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)
    
    event = get_object_or_404(Event, id=event_id)
    
    if event.booked_seats < event.total_seats:
        time.sleep(0.01)
        event.booked_seats += 1
        event.save()
        
        Booking.objects.create(event=event, user_name="vulnerable_user")
        return JsonResponse({"status": "success"}, status=201)
    
    return JsonResponse({"status": "error", "message": "No seats available"}, status=400)

@csrf_exempt
def book_pessimistic(request, event_id):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    try:
        with transaction.atomic():
            event = Event.objects.select_for_update().get(id=event_id)
            
            if event.booked_seats < event.total_seats:
                event.booked_seats += 1
                event.save()
                
                Booking.objects.create(event=event, user_name="pessimistic_user")
                
                transaction.on_commit(lambda: log_confirmation(event_id))
                
                return JsonResponse({"status": "success"}, status=201)
            
            return JsonResponse({"status": "error", "message": "No seats available"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

