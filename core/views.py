from django.shortcuts import render
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from events.models import Event

User = get_user_model()

def home(request):
    today = now().date()
    base_query = Event.objects.select_related('category').prefetch_related('participants')

    counts = {
        'total_events': base_query.count(),
        'total_participants': User.objects.count(),
        'today_events': base_query.filter(date__date=today).count(),
        'upcoming_events': base_query.filter(date__date__gt=today).count(),
        'past_events': base_query.filter(date__date__lt=today).count(),
    }

    type_param = request.GET.get('type', 'all').lower()
    if type_param == 'today':
        events = base_query.filter(date__date=today)
    elif type_param == 'upcoming':
        events = base_query.filter(date__date__gt=today)
    elif type_param == 'past':
        events = base_query.filter(date__date__lt=today)
    else:
        events = base_query.all()

    context = {
        'events': events,
        'counts': counts,
        'type': type_param,
    }

    return render(request, 'home.html', context)
