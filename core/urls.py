from django.urls import path

from .views import *

urlpatterns = [
    path('add_elevators', AddElevators.as_view(), name='add_elevators'),

    path('call_elevator', CallElevator.as_view(), name='call_elevator'),
    path('fetch_all_requests', FetchAllRequests.as_view(), name='fetch_all_requests'),
    path('fetch_next_destination', FetchNextDestination.as_view(), name='fetch_next_destination'),
    path('fetch_direction', FetchDirection.as_view(), name='fetch_direction'),
    path('mark_elevator_down', MarkElevatorDown.as_view(), name='mark_elevator_down'),
    path('open_or_close_door', OpenOrCloseDoor.as_view(), name='open_or_close_door')
]