from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Ticket, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import LoginForm, SignUpForm, SellTicketForm, edit_profile


def index(request):
	return render(request, 'ticket_app/index.html')

def event_list(request):
	events = Event.objects.all()
	return render(request, 'ticket_app/event_list.html', {'events': events})

def ticket_list(request):
	tickets = Ticket.objects.all()
	return render(request, 'ticket_app/ticket_list.html', {'tickets', tickets})


def home(request):
    sort_by = request.GET.get('sort', 'event')  # Default sorting by event

    club_filter = request.GET.get('club', None)

    tickets = Ticket.objects.all()

    if club_filter:
        tickets = tickets.filter(event=club_filter)

    if sort_by:
        tickets = tickets.order_by(sort_by)
    
    context = {
        'tickets': tickets
    }
    
    return render(request, 'ticket_app/home.html', context)
        
	

def terms_conditions(request):
	return render(request, 'ticket_app/terms_conditions.html')

def SignUp(request):
    form = SignUpForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user = UserProfile.objects.get(username=form.cleaned_data.get('username'))
            user.save()
            return redirect("login")
        else:
            print(form.errors)
            return render(request, 'ticket_app/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'ticket_app/signup.html', {'form': form})


def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                print("User logged in successfully")
                login(request, user)
                return redirect("home")
            else:
                return render(request, 'ticket_app/login.html', {'error': 'Incorrect username or password.'})
    else:
        form = LoginForm()
    return render(request, 'ticket_app/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('index') 


@login_required
def sell_ticket(request):
    if request.method == 'POST':
        form = SellTicketForm(request.POST)
        if form.is_valid():
            # Process the form data
            event1 = form.cleaned_data.get('event')
            date1 = form.cleaned_data.get('date')
            time1 = form.cleaned_data.get('time')
            price1 = form.cleaned_data.get('price')
            user1 = request.user
            
            Ticket.objects.create(event=event1, date=date1, time=time1, price=price1, seller=user1)
            
            # For now, let's just redirect to a success page or the same page
            return redirect('sell_ticket_success')  # Create this URL/view for a success page
    else:
        form = SellTicketForm()
    
    return render(request, 'ticket_app/sell_ticket.html', {'form': form})


def sell_ticket_success(request):
    return HttpResponse('Your ticket has been listed successfully!')

@login_required
def buy_ticket(request, ticket_id):
    
	ticket = get_object_or_404(Ticket, id=ticket_id)

	return render(request, 'ticket_app/buy_ticket.html', {'ticket': ticket})

def profile(request):
    user = request.user

    if request.method == 'POST':
        form = edit_profile(request.POST)  # Ensure the form is instantiated with the current user
        if form.is_valid():
            form.save()  # Save the form, which updates the user1 instance
            return redirect('profile')  # Redirect to the same page or another page to show the updated profile
        else:
            print(form.errors)
    else:
        form = edit_profile()


    bought_tickets = Ticket.objects.filter(buyer=user)

    bought_tickets = bought_tickets.filter(sold= True)
    
    sold_tickets = Ticket.objects.filter(seller=user)
    print(sold_tickets)
    
    context = {
        'bought_tickets': bought_tickets,
        'sold_tickets': sold_tickets,
        'form': form,
    }
    
    return render(request, 'ticket_app/profile.html', context)

