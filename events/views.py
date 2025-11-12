from django.contrib import messages
from django.utils.timezone import now
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from events.forms import EventModelForm, CategoryModelForm
from events.models import Event, Category, RSVP
from django.utils import timezone


def admin_dashboard(request):
    today = now().date()
    # Base queryset
    base_query = Event.objects.select_related('category').prefetch_related('participants')
    # All events with participants preloaded
    events = base_query.all()
    # All participants (users)
    participants = User.objects.all().prefetch_related('rsvped_events')
    # All categories with event counts
    categories = Category.objects.prefetch_related('events').all()
    # Stats counts
    counts = {
        'total_participants': User.objects.count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(date__gte=timezone.now()).count(),
        'total_categories': Category.objects.count(),
    }
    type = request.GET.get('type', 'all').lower()
    if type == 'today':
        events = base_query.filter(date__date=today)
    elif type == 'upcoming':
        events = base_query.filter(date__date__gt=today)
    elif type == 'past':
        events = base_query.filter(date__date__lt=today)
    else:
        events = base_query.all()

    context = {
        'events': events,
        'participants': participants,
        'categories': categories,
        'counts': counts,
        'type': type,
    }
    return render(request, 'admin_dashboard.html', context)





def organizer_dashboard(request):
    today = now().date()
    # Base queryset
    base_query = Event.objects.select_related('category').prefetch_related('participants')

    # Statistics
    counts = {
        'total_events': base_query.count(),
        'total_participants': User.objects.count(),   # All users count
        'today_events': base_query.filter(date__date=today).count(),
        'upcoming_events': base_query.filter(date__date__gt=today).count(),
        'past_events': base_query.filter(date__date__lt=today).count(),
    }

    # Filter by query param
    type = request.GET.get('type', 'all').lower()
    if type == 'today':
        events = base_query.filter(date__date=today)
    elif type == 'upcoming':
        events = base_query.filter(date__date__gt=today)
    elif type == 'past':
        events = base_query.filter(date__date__lt=today)
    else:
        events = base_query.all()
    context = {
        'events': events,
        'counts': counts,
        'type': type,
    }
    return render(request, 'organizer_dashboard.html', context)


def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    # Check if user already RSVP'd
    if RSVP.objects.filter(user=user, event=event).exists():
        messages.warning(request, "You have already RSVP'd to this event.")
    else:
        RSVP.objects.create(user=user, event=event)
        messages.success(request, f"You have successfully RSVP'd to {event.name}.")

    if user.is_superuser:
        return redirect('admin-dashboard')
    elif user.is_staff:
        return redirect('organizer-dashboard')
    else:
        return redirect('participant-dashboard')



def rsvp_list(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    rsvps = RSVP.objects.filter(event=event).select_related("user")
    return render(request, "rsvp_list.html", {
        "event": event,
        "rsvps": rsvps
    })

def remove_rsvp(request, event_id, user_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        RSVP.objects.filter(event=event, user_id=user_id).delete()
    return redirect("rsvp-list", event_id=event.id)

def view_event(request, id):
    event = get_object_or_404(Event.objects.select_related('category'), id=id)
    context = {'event': event}
    return render(request, 'view_event.html', context)





def create_event(request):
    # Only Organizer or Admin can access
    if not (request.user.is_superuser or request.user.groups.filter(name='Organizer').exists()):
        messages.error(request, "You do not have permission to create events.")
        return redirect('sign-in')  # or another safe page

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, request.FILES)
        category_form = CategoryModelForm(request.POST)

        if event_form.is_valid() and category_form.is_valid():
            # Save category
            category_obj = category_form.save()

            # Save event
            event_obj = event_form.save(commit=False)
            event_obj.category = category_obj
            event_obj.save()

            messages.success(request, "Event created successfully.")

            # Role-based redirect after creation
            if request.user.is_superuser:
                return redirect('admin-dashboard')
            else:
                return redirect('organizer-dashboard')

    else:
        event_form = EventModelForm()
        category_form = CategoryModelForm()

    context = {
        'event_form': event_form,
        'category_form': category_form,
    }
    return render(request, 'create_event.html', context)

def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name)
            return redirect("admin-dashboard")
    return render(request, "add_category.html")



def edit_event(request, id):
    event_instance = get_object_or_404(Event, id=id)

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, request.FILES, instance=event_instance)
        category_form = CategoryModelForm(request.POST, instance=event_instance.category)

        if event_form.is_valid() and category_form.is_valid():
            category_form.save()
            event_form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('organizer-dashboard')
    else:
        event_form = EventModelForm(instance=event_instance)
        category_form = CategoryModelForm(instance=event_instance.category)

    context = {
        'event_form': event_form,
        'category_form': category_form,
    }
    return render(request, 'create_event.html', context)


def delete_event(request, id):
    event_instance = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event_instance.delete()
        messages.success(request, 'Event deleted successfully.')

    return redirect('admin-dashboard')




def participant_dashboard(request):
    user = request.user  
    now = timezone.now()

    # Stats
    total_rsvps = RSVP.objects.filter(user=user).count()
    upcoming_events = Event.objects.filter(date__gt=now).count()
    past_events = Event.objects.filter(date__lt=now).count()
    todays_events = Event.objects.filter(date__date=now.date()).count()

    # Event lists
    todays_event_list = Event.objects.filter(date__date=now.date())
    upcoming_event_list = Event.objects.filter(date__gt=now).order_by("date")
    past_event_list = Event.objects.filter(date__lt=now).order_by("-date")

    # RSVP dictionary
    user_rsvps = RSVP.objects.filter(user=user)
    rsvp_status = {rsvp.event.id: rsvp.status for rsvp in user_rsvps}

    context = {
        "total_rsvps": total_rsvps,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "todays_events": todays_events,
        "todays_event_list": todays_event_list,
        "upcoming_event_list": upcoming_event_list,
        "past_event_list": past_event_list,
        "rsvp_status": rsvp_status,
    }
    return render(request, "participant_dashboard.html", context)



def cancel_rsvp(request, event_id):
    user = request.user

    if request.method == "POST":
        rsvp = get_object_or_404(RSVP, event_id=event_id, user=request.user)
        rsvp.delete()  # remove the RSVP
    if user.is_superuser:
        return redirect('admin-dashboard')
    elif user.is_staff:
        return redirect('organizer-dashboard')
    else:
        return redirect('participant-dashboard')
