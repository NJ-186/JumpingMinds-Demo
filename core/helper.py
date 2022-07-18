from django.core.cache import cache

from .constants import *
from .models import *
from .serializers import *


def validate_get_request(elevator_id):
    res = {}

    if not elevator_id:
        res = {
            "error_message": "elevator_id is a required field."
        }

        return res

    if not validate_elevator_object(elevator_id):
        res = {
            "error_message": "invalid elevator_id."
        }

    return res


def validate_elevator_object(elevator_id):
    try:
        elevator = Elevator.objects.get(id=elevator_id)
    except:
        elevator = None

    if elevator:
        return True
    
    return False


def get_all_elevators():
    return Elevator.objects.all()


def create_elevators_initially(elevator_count):
    objs = [Elevator() for i in range(elevator_count)]

    Elevator.objects.bulk_create(objs)

    return


def check_if_elevator_is_down(elevator_id):

    res = {}

    elevator = Elevator.objects.get(id=elevator_id)

    if elevator.is_down:
        res = {
            "error_message": "Elevator is under maintenance."
        }

    return res


def update_cache_for_elevator_request(elevator_id, requested_floor):

    is_initial_request = False

    # floors_pipeline -> the pending list of requests that elevator_id needs to serve.
    floors_pipeline = cache.get(elevator_id)

    if floors_pipeline:
        floors_pipeline.append(requested_floor)

    else:
        floors_pipeline = [requested_floor]
        is_initial_request = True

    cache.set(elevator_id, floors_pipeline)

    return is_initial_request


def update_db_for_elevator_request(elevator_id, requested_floor, is_initial_request):
    
    elevator = Elevator.objects.get(id=elevator_id)

    if is_initial_request:

        last_destination = cache.get(
            CACHE_LAST_DESTINATION_KEY % elevator_id
        )

        # Check for case when lifts stops at a certain floor for sometime and then request
        # comes in
        if last_destination:

            if last_destination > requested_floor:
                elevator.direction = DOWNWARD

            elif last_destination < requested_floor:
                elevator.direction = UPWARDS

            else:
                elevator.direction = IDLE

        else:
            elevator.direction = UPWARDS

        elevator.next_destination = requested_floor
        elevator.save()

    ElevatorRequests.objects.create(
        elevator=elevator,
        requested_floor=requested_floor
    )
    
    return


def get_all_requests_for_elevator(elevator_id):

    elevator = Elevator.objects.get(id=elevator_id)

    requests =  ElevatorRequests.objects.filter(
        elevator=elevator
    ).order_by('created_at')

    serializer = ElevatorRequestsSerializer(requests, many=True)

    return serializer.data


def get_elevator_next_destination(elevator_id):

    elevator = Elevator.objects.get(id=elevator_id)

    res = {
        "next_destination": elevator.next_destination
    }

    return res


def get_elevator_direction(elevator_id):

    elevator = Elevator.objects.get(id=elevator_id)

    res = {
        "direction": elevator.direction
    }

    return res


def mark_elevator_down(elevator_id):

    elevator = Elevator.objects.get(id=elevator_id)

    elevator.is_down = True
    elevator.save()

    return


def open_elevator(elevator_id):

    elevator = Elevator.objects.get(id=elevator_id)

    if elevator.direction == IDLE:
        res = {
            "error_message": "Could not perform operation since elevator is in idle state."
        }

        return res

    floors_pipeline = cache.get(elevator_id)

    # removing the floor arrived, from cache
    floors_pipeline = list(filter((elevator.next_destination).__ne__, floors_pipeline))

    # updating floors pipeline in cache
    cache.set(elevator_id, floors_pipeline)

    update_elevator_request_state(elevator)

    next_destination = get_next_destination(elevator, floors_pipeline)

    update_elevator_state_on_elevator_opening(elevator, next_destination)

    return


def update_elevator_request_state(elevator):

    ElevatorRequests.objects.filter(
        elevator=elevator,
        requested_floor=elevator.next_destination
    ).update(
        is_completed=True
    )

    return


def get_next_destination(elevator, floors_pipeline):

    if not floors_pipeline:
        return -1
    
    if elevator.direction == UPWARDS:

        next_upper_floor = get_next_upper_floor(elevator, floors_pipeline)

        # means the elevator has reached its topmost requested floor
        if next_upper_floor < elevator.next_destination: 

            next_lower_floor = get_next_lower_floor(elevator, floors_pipeline)

            next_floor = next_lower_floor

        next_floor = next_upper_floor

    else:

        next_lower_floor = get_next_lower_floor(elevator, floors_pipeline)

        # means the elevator has reached its lowermost requested destination
        if next_lower_floor > elevator.next_destination:

            next_upper_floor = get_next_upper_floor(elevator, floors_pipeline)

            next_floor = next_upper_floor

        next_floor = next_lower_floor
    
    return next_floor


def get_next_upper_floor(elevator, floors_pipeline):

    current_floor = elevator.next_destination

    return min(
        floors_pipeline,
        key=lambda x: abs(x-current_floor) if x > current_floor else FLOORS_COUNT
    )


def get_next_lower_floor(elevator, floors_pipeline):

    current_floor = elevator.next_destination

    return min(
        floors_pipeline,
        key=lambda x: abs(x-current_floor) if x < current_floor else FLOORS_COUNT
    )


def update_elevator_state_on_elevator_opening(elevator, next_destination):

    # updating last_destination in cache, will be required to update elevator direction once
    # elevator stops and then starts after sometime
    cache.set(
        CACHE_LAST_DESTINATION_KEY % elevator.id,
        elevator.next_destination
    )

    if next_destination == -1:
        next_direction = IDLE
        elevator.next_destination = None

    elif next_destination > elevator.next_destination:
        next_direction = UPWARDS # holds elevator direction once elevator closes door
        elevator.next_destination = next_destination

    else:
        next_direction = DOWNWARD # holds elevator direction once elevator closes door
        elevator.next_destination = next_destination

    elevator.direction = IDLE
    elevator.save()

    # updating next_direction in cache, will be required to update elevator direction once elevator 
    # closes door.
    cache.set(
        CACHE_NEXT_DIRECTION_KEY % elevator.id,
        next_direction
    )

    return


def close_elevator(elevator_id):
    elevator = Elevator.objects.get(id=elevator_id)

    if elevator.direction != IDLE:
        res = {
            "error_message": "Could not perform operation since elevator is moving."
        }

        return res
    
    update_elevator_state_on_elevator_closing(elevator)
    
    return


def update_elevator_state_on_elevator_closing(elevator):

    next_direction = cache.get(
        CACHE_NEXT_DIRECTION_KEY % elevator.id
    )

    elevator.direction = next_direction
    elevator.save()

    return
