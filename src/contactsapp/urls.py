from django.urls import path
from . import views


app_name = 'contactsapp'

urlpatterns = [
    path('add_contact/', views.add_contact, name='add_contact'),
    path('update_contact/<int:contact_id>', views.update_contact, name='update_contact'),
    path('delete_contact/<int:contact_id>', views.delete_contact, name='delete_contact'),
    path('search_contact/', views.search_contact, name='search_contact'),
    path('upcoming_birthdays/', views.upcoming_birthdays, name='upcoming_birthdays'),
    path('detail_contact/<int:contact_id>', views.detail_contact, name="detail_contact"),
    path('send_email_contact/<int:contact_id>/',  views.send_email_contact, name='send_email_contact')

]