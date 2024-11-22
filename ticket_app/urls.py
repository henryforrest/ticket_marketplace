from django.urls import path, include
from . import views 

urlpatterns = [
	path("", views.index, name="index"),
    path("home/", views.home, name="home"),
	path('events/', views.event_list, name='event_list'), 
	path("tickets/", views.ticket_list, name='ticket_list'),
    path("signup/", views.SignUp, name="signup"), 
	path("login/", views.Login, name="login"), 
    path("terms_conditions/", views.terms_conditions, name="terms_conditions"),
    path("sell_ticket/", views.sell_ticket, name="sell_ticket"),
    path("sell_ticket_success/", views.sell_ticket_success, name="sell_ticket_success"),
    path('logout/', views.logout_view, name='logout'),
    path('buy_ticket/<int:ticket_id>', views.buy_ticket, name="buy_ticket"),
    path('profile/', views.profile, name='profile'),
]
