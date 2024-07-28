from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from textblob import TextBlob
from .models import Event, Registration, Category, Feedback
from .forms import FeedbackForm
from django.core.mail import send_mail
from django.conf import settings
import asyncio
import requests

@login_required
def user_dashboard(request):
    """
    Display the user dashboard with events the user has registered for and upcoming events.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object with rendered user dashboard template.
    """
    try:
        user = request.user
        if user.is_superuser:
            return redirect('super_home')
        
        my_events = Event.objects.filter(registration__user=user)[:2]
        upcoming_events = Event.objects.exclude(registration__user=user).order_by('start_date')[:2]
        
        context = {
            'my_events': my_events,
            'upcoming_events': upcoming_events,
        }
        return render(request, 'user_dashboard.html', context)
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return render(request, 'user_dashboard.html')

@login_required
def browse_events(request):
    """
    Display all events with optional filtering by date, category, and type.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object with rendered browse events template.
    """
    try:
        events = Event.objects.all()
        categories = Category.objects.all()

        if 'date' in request.GET:
            date = request.GET['date']
            if date:
                events = events.filter(start_date=date)
        
        if 'category' in request.GET:
            category_name = request.GET['category']
            category = get_object_or_404(Category, name=category_name)
            if category:
                events = events.filter(category=category)
        
        if 'type' in request.GET:
            event_type = request.GET['type']
            if event_type:
                events = events.filter(type=event_type)
        
        context = {
            'events': events,
            'categories': categories,
        }
        
        return render(request, 'browse_events.html', context)
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return render(request, 'browse_events.html')

@login_required
def event_details(request, event_id):
    """
    Display details of a specific event.

    Args:
        request: HttpRequest object.
        event_id: ID of the event to display details for.

    Returns:
        HttpResponse object with rendered event details template.
    """
    try:
        event = get_object_or_404(Event, id=event_id)
        context = {
            'event': event
        }
        return render(request, 'event_details.html', context)
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return redirect('home')

@login_required
def my_registrations(request):
    """
    Display registrations of the current user, categorized into attended and current events.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object with rendered my registrations template.
    """
    try:
        user = request.user
        registrations = Registration.objects.filter(user=user)
        
        attended_events = []
        current_events = []
        now = timezone.now()
        
        for registration in registrations:
            event = registration.event
            if event.end_date < now:
                attended_events.append(registration)
            else:
                current_events.append(registration)
        
        context = {
            'attended_events': attended_events,
            'current_events': current_events,
        }
        return render(request, 'my_registrations.html', context)
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return render(request, 'my_registrations.html')

@login_required
def cancel_registration(request, registration_id):
    """
    Cancel a user's registration for an event.

    Args:
        request: HttpRequest object.
        registration_id: ID of the registration to cancel.

    Returns:
        HttpResponse object redirecting to my registrations page.
    """
    try:
        registration = get_object_or_404(Registration, id=registration_id)
        if request.method == 'POST':
            registration.delete()
            messages.success(request, 'Registration successfully canceled.')
        return redirect('my_registrations')
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return redirect('my_registrations')

@login_required
def provide_feedback(request, event_id):
    """
    Provide feedback for a specific event.

    Args:
        request: HttpRequest object.
        event_id: ID of the event to provide feedback for.

    Returns:
        HttpResponse object with rendered feedback form template.
    """
    try:
        event = get_object_or_404(Event, id=event_id)
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.user = request.user
                feedback.event = event
                
                # Get sentiment analysis
                response = requests.post(
                    url=f"{settings.SENTIMENT_ANALYSIS_URL}/analyze/",
                    json={'sentence': feedback.comments}
                )

                if response.status_code == 200:
                    sentiment = response.json().get('sentiment', 'neutral')
                    feedback.sentiment = sentiment
                else:
                    feedback.sentiment = 'neutral'
                
                feedback.save()
                messages.success(request, 'Feedback submitted successfully!')
                return redirect('home')
        else:
            form = FeedbackForm()
        context = {
            'event': event,
            'form': form,
        }
        return render(request, 'feedback.html', context)
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return redirect('home')

@login_required
def register_event(request, event_id):
    """
    Register the current user for a specific event.

    Args:
        request: HttpRequest object.
        event_id: ID of the event to register for.

    Returns:
        HttpResponse object redirecting to my registrations page.
    """
    try:
        event = get_object_or_404(Event, id=event_id)
        if request:
            registration = Registration.objects.create(user=request.user, event=event)
            asyncio.run(send_registration_email(request.user.email, event.title))
            messages.success(request, 'Event registration successful!')
            return redirect('my_registrations')
        
        context = {'event': event}
        return render(request, 'event_details.html', context)
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return redirect('home')

# Asynchronous function to send registration email
async def send_registration_email(user_email, event_title):
    """
    Asynchronous function to send registration confirmation email.

    Args:
        user_email: Email address of the user to send the email to.
        event_title: Title of the event the user registered for.
    """
    try:
        subject = 'Event Registration Confirmation'
        message = f'Hello,\n\nYou have successfully registered for the event: {event_title}.\n\nThank you!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]
        
        await asyncio.sleep(1)  # Simulate some asynchronous task
        
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f'Failed to send registration email: {e}')
