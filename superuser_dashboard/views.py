from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ValidationError
from user_dashboard.models import  User, Registration, Feedback
from .models import Category, Event
from .forms import EventForm, CategoryForm
from .utils import generate_suggestions_function

"""
This module contains views for managing events, categories, and user registrations in the event management system.
It handles CRUD operations for events and categories, displays user registrations, and provides description suggestions for events.
"""

def generate_suggestions(request):
    """
    Generate description suggestions for an event based on its title.

    Args:
        request: HttpRequest object containing the event title in GET parameters.

    Returns:
        JsonResponse object with a list of description suggestions or an error message.
    """
    try:
        if request.method == 'GET' and 'title' in request.GET:
            event_title = request.GET.get('title')
            suggestions = generate_suggestions_function(event_title)
            return JsonResponse(suggestions, safe=False)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {e}'}, status=500)

def superuser_required(view_func):
    """
    Decorator to require superuser status for a view.

    Args:
        view_func: The view function to decorate.

    Returns:
        The decorated view function.
    """
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser, login_url='login')(view_func))
    return decorated_view_func

@superuser_required
def superuser_dashboard(request):
    """
    Display the superuser dashboard with upcoming events, recent registrations, and recent feedback.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object with rendered superuser dashboard template.
    """
    try:
        upcoming_events = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')[:2]
        recent_registrations = Registration.objects.select_related('user', 'event').order_by('-registration_datetime')[:2]
        recent_feedback = Feedback.objects.select_related('user', 'event').order_by('-feedback_datetime')[:2]

        feedbacks = Feedback.objects.all()
        sentiment_data = {}
        for event in Event.objects.all():
            feedbacks_for_event = feedbacks.filter(event=event)
            if feedbacks_for_event.exists():
                positive_feedbacks = feedbacks_for_event.filter(sentiment='positive').count()
                total_feedbacks = feedbacks_for_event.count()
                sentiment_data[event.title] = int((positive_feedbacks / total_feedbacks) * 100)

        context = {
            'upcoming_events': upcoming_events,
            'recent_registrations': recent_registrations,
            'recent_feedback': recent_feedback,
            'sentiment_data': sentiment_data,
        }
        return render(request, 'superuser_dashboard.html', context)
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return render(request, 'superuser_dashboard.html')

@superuser_required
def add_event(request):
    """
    Handle adding a new event.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object with rendered add event template.
    """
    try:
        form = EventForm() 
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.organizer = request.user
                event.save()
                messages.success(request, 'Event added successfully!')
                return redirect('manage_events')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                form = EventForm()  # Re-initialize form to display errors in the template

        categories = Category.objects.all()
        events = Event.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'events': events,
        }
        return render(request, 'manage_events.html', context)
    except ValidationError as e:
        messages.error(request, f"Validation error: {e}")
        return render(request, 'manage_events.html', {'form': form})
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return render(request, 'manage_events.html', {'form': form})

@superuser_required
def edit_event(request, event_id):
    """
    Handle editing an existing event.

    Args:
        request: HttpRequest object.
        event_id: ID of the event to be edited.

    Returns:
        HttpResponse object with rendered edit event template.
    """
    try:
        event = get_object_or_404(Event, id=event_id)
        if request.method == "POST":
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request, 'Event updated successfully!')
                return redirect('manage_events')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            form = EventForm(instance=event)
        return render(request, 'edit_event.html', {'form': form})
    except ValidationError as e:
        messages.error(request, f"Validation error: {e}")
        return render(request, 'edit_event.html', {'form': form})
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return render(request, 'edit_event.html', {'form': form})

@superuser_required
def delete_event(request, event_id):
    """
    Handle deleting an existing event.

    Args:
        request: HttpRequest object.
        event_id: ID of the event to be deleted.

    Returns:
        HttpResponse object redirecting to manage events page.
    """
    try:
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('manage_events')
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return redirect('manage_events')

@superuser_required
def manage_events(request):
    """
    Display all events and categories for management.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object with rendered manage events template.
    """
    try:
        events = Event.objects.all()
        categories = Category.objects.all()
        context = {
            'events': events,
            'categories': categories,
        }
        return render(request, 'manage_events.html', context)
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return render(request, 'manage_events.html')

@superuser_required
def add_category(request):
    """
    Handle adding a new category.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object with rendered add category template.
    """
    try:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Category added successfully!')
                return redirect('manage_categories')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            form = CategoryForm()

        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
        }
        return render(request, 'manage_categories.html', context)
    except ValidationError as e:
        messages.error(request, f"Validation error: {e}")
        return render(request, 'manage_categories.html', {'form': form})
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return render(request, 'manage_categories.html', {'form': form})

@superuser_required
def edit_category(request, category_id):
    """
    Handle editing an existing category.

    Args:
        request: HttpRequest object.
        category_id: ID of the category to be edited.

    Returns:
        HttpResponse object with rendered edit category template.
    """
    try:
        category = get_object_or_404(Category, id=category_id)
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, 'Category updated successfully!')
                return redirect('manage_categories')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            form = CategoryForm(instance=category)

        context = {
            'form': form,
            'category': category,
        }
        return render(request, 'edit_category.html', context)
    except ValidationError as e:
        messages.error(request, f"Validation error: {e}")
        return render(request, 'edit_category.html', {'form': form})
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return render(request, 'edit_category.html', {'form': form})

@superuser_required
def delete_category(request, category_id):
    """
    Handle deleting an existing category.

    Args:
        request: HttpRequest object.
        category_id: ID of the category to be deleted.

    Returns:
        HttpResponse object redirecting to manage categories page.
    """
    try:
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('manage_categories')
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return redirect('manage_categories')

@superuser_required
def manage_categories(request):
    """
    Display all categories for management.
    Args:
    request: HttpRequest object.

    Returns:
        HttpResponse object with rendered manage categories template.
    """
    try:
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'manage_categories.html', context)
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return render(request, 'manage_categories.html')

@superuser_required
def view_registrations(request):
    """
    Display all user registrations with optional filters for event, user, and date.
    Args:
    request: HttpRequest object.

    Returns:
        HttpResponse object with rendered view registrations template.
    """
    try:
        events = Event.objects.all()
        users = User.objects.all()
        registrations = Registration.objects.all()

        event_filter = request.GET.get('event')
        user_filter = request.GET.get('user')
        date_filter = request.GET.get('date')

        if event_filter:
            registrations = registrations.filter(event_id=event_filter)
        if user_filter:
            registrations = registrations.filter(user_id=user_filter)
        if date_filter:
            registrations = registrations.filter(registration_datetime__date=date_filter)

        context = {
            'events': events,
            'users': users,
            'registrations': registrations,
        }
        return render(request, 'view_registrations.html', context)
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return render(request, 'view_registrations.html')
