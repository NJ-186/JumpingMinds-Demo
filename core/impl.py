from .constants import *
from .models import *
from .serializers import *
from .views_helper import ResponseHelper
from .cache_helper import CacheHelper


class ElevatorImpl:
    
    def __init__(self, elevator_id, requested_floor=None, door_state=None) -> None:
        self.elevator_id = elevator_id
        self.requested_floor = requested_floor
        self.door_state = door_state

    def get_elevator_id(self):
        return self.elevator_id

    def get_requested_floor(self):
        return self.requested_floor

    def get_door_state(self):
        return self.door_state

    @staticmethod
    def add_elevators(elevator_count: int) -> dict:
        """
        - Method to add number of elevators initially and
        create their respective instances.
        - This can only be called once.
        """
        elevators = ElevatorHelper.get_all_elevators()

        if elevators:
            error = "It looks like you have already updated the elevator_count."
            res_object = ResponseHelper.get_error_response(error)

            return res_object

        ElevatorImpl.create_elevators_initially(elevator_count)

        return {}

    @staticmethod
    def create_elevators_initially(elevator_count) -> None:
        objs = [Elevator() for i in range(elevator_count)]

        Elevator.objects.bulk_create(objs)

        return

    def call_elevator(self) -> dict:
        """
        - Method to call requested elevator_id for the requested_floor
        """
        is_elevator_down = ElevatorHelper.check_if_elevator_is_down(
            self.get_elevator_id()
        )

        if is_elevator_down:
            res_object = ResponseHelper.get_error_response(is_elevator_down)

            return res_object

        is_initial_request = CacheHelper.update_cache_with_elevator_request(
            self.get_elevator_id(),
            self.get_requested_floor()
        )

        self.update_db_for_elevator_request(is_initial_request)

        return {}

    def update_db_for_elevator_request(self, is_initial_request):
        
        elevator = Elevator.objects.get(id=self.get_elevator_id())

        if is_initial_request:

            last_destination = CacheHelper.get_last_destination_from_cache(self.get_elevator_id())

            # Check for case when lifts stops at a certain floor for sometime and then request
            # comes in
            ElevatorHelper.update_elevator_schema_in_db_for_call_elevator_request(
                elevator,
                last_destination,
                self.get_requested_floor()
            )

        ElevatorImpl.create_elevator_request_object(
            elevator,
            self.get_requested_floor()
        )

        return

    @staticmethod
    def create_elevator_request_object(elevator_obj, requested_floor) -> None:
        ElevatorRequests.objects.create(
            elevator=elevator_obj,
            requested_floor=requested_floor
        )

        return

    def get_all_requests_for_elevator(self):
        """
        - Method to get all requests for elevator_id
        """
        is_elevator_down = ElevatorHelper.check_if_elevator_is_down(
            self.get_elevator_id()
        )

        if is_elevator_down:
            res_object = ResponseHelper.get_error_response(is_elevator_down)

            return res_object

        requests = ElevatorHelper.get_elevator_requests_for_elevator_id(self.get_elevator_id())

        serializer = ElevatorRequestsSerializer(requests, many=True)

        return {
            'elevator_requests': serializer.data
        }

    def get_elevator_next_destination(self):
        """
        
        """
        is_elevator_down = ElevatorHelper.check_if_elevator_is_down(
            self.get_elevator_id()
        )

        if is_elevator_down:
            res_object = ResponseHelper.get_error_response(is_elevator_down)

            return res_object

        elevator = ElevatorHelper.get_elevator_object(self.get_elevator_id())

        res = {
            "next_destination": elevator.next_destination
        }

        return res

    def get_elevator_direction(self):
        """
        
        """
        is_elevator_down = ElevatorHelper.check_if_elevator_is_down(
            self.get_elevator_id()
        )

        if is_elevator_down:
            res_object = ResponseHelper.get_error_response(is_elevator_down)

            return res_object

        elevator = ElevatorHelper.get_elevator_object(self.get_elevator_id())

        res = {
            "direction": elevator.direction
        }

        return res

    def mark_elevator_down(self):
        """
        
        """
        is_elevator_down = ElevatorHelper.check_if_elevator_is_down(
            self.get_elevator_id()
        )

        if is_elevator_down:
            res_object = ResponseHelper.get_error_response(is_elevator_down)

            return res_object

        elevator = ElevatorHelper.get_elevator_object(self.get_elevator_id())

        ElevatorHelper.update_elevator_is_down_in_db(elevator)

        return {}

    def open_or_close_door(self):
        """
        
        """
        is_elevator_down = ElevatorHelper.check_if_elevator_is_down(
            self.get_elevator_id()
        )

        if is_elevator_down:
            res_object = ResponseHelper.get_error_response(is_elevator_down)

            return res_object

        if self.get_door_state() == OPEN:
            res = self.open_elevator()

        else:
            res = self.close_elevator()

        return res

    def open_elevator(self):

        elevator = ElevatorHelper.get_elevator_object(self.get_elevator_id())

        is_elevator_idle, error_message = ElevatorHelper.check_if_elevator_is_idle(elevator)

        if is_elevator_idle:
            res_object = ResponseHelper.get_error_response(error_message)

            return res_object

        floors_pipeline = CacheHelper.get_floors_pipeline_from_cache(self.get_elevator_id())

        # removing the floor arrived, from cache
        floors_pipeline = list(filter((elevator.next_destination).__ne__, floors_pipeline))

        # updating floors pipeline in cache
        CacheHelper.set_value_for_key_in_cache(
            self.get_elevator_id(),
            floors_pipeline
        )

        ElevatorHelper.update_elevator_request_state(elevator)

        next_destination = ElevatorHelper.get_next_destination(elevator, floors_pipeline)

        ElevatorHelper.update_elevator_state_on_elevator_opening(elevator, next_destination)

        return {}

    def close_elevator(self):
        elevator = ElevatorHelper.get_elevator_object(self.get_elevator_id())

        is_elevator_idle, error_message = ElevatorHelper.check_if_elevator_is_idle(elevator)

        if not is_elevator_idle:
            res_object = ResponseHelper.get_error_response(error_message)

            return res_object
        
        ElevatorHelper.update_elevator_state_on_elevator_closing(elevator)

        return {}


class ElevatorHelper:

    @staticmethod
    def get_all_elevators():
        return Elevator.objects.all()

    @staticmethod
    def check_if_elevator_is_down(elevator_id):

        is_down = ""

        elevator = Elevator.objects.get(id=elevator_id)

        if elevator.is_down:
            is_down = "Elevator is under maintenance."

        return is_down

    @staticmethod
    def update_elevator_schema_in_db_for_call_elevator_request(elevator_obj, last_destination, requested_floor):

        if last_destination:
            if last_destination > requested_floor:
                elevator_obj.direction = DOWNWARD

            elif last_destination < requested_floor:
                elevator_obj.direction = UPWARDS

            else:
                elevator_obj.direction = IDLE

        else:
            elevator_obj.direction = UPWARDS

        elevator_obj.next_destination = requested_floor
        elevator_obj.save()

    @staticmethod
    def get_elevator_requests_for_elevator_id(elevator_id):

        elevator = ElevatorHelper.get_elevator_object(elevator_id)

        requests =  ElevatorRequests.objects.filter(
            elevator=elevator
        ).order_by('created_at')

        return requests

    @staticmethod
    def get_elevator_object(elevator_id):

        return Elevator.objects.get(id=elevator_id)

    @staticmethod
    def update_elevator_is_down_in_db(elevator):

        elevator.is_down = True
        elevator.save()

        return

    @staticmethod
    def check_if_elevator_is_idle(elevator):

        if elevator.direction == IDLE:

            is_elevator_idle = True
            error_message = "Could not perform operation since gates are already open."

        else:
            is_elevator_idle = False
            error_message = "Could not perform operation since elevator is already closed."


        return is_elevator_idle, error_message

    @staticmethod
    def update_elevator_request_state(elevator):

        ElevatorRequests.objects.filter(
            elevator=elevator,
            requested_floor=elevator.next_destination
        ).update(
            is_completed=True
        )

        return
    
    @staticmethod
    def get_next_destination(elevator, floors_pipeline):

        if not floors_pipeline:
            return -1
        
        if elevator.direction == UPWARDS:

            next_upper_floor = ElevatorHelper.get_next_upper_floor(elevator, floors_pipeline)

            # means the elevator has reached its topmost requested floor
            if next_upper_floor < ElevatorHelper.get_current_floor_of_elevator(elevator): 

                next_lower_floor = ElevatorHelper.get_next_lower_floor(elevator, floors_pipeline)

                next_floor = next_lower_floor

            next_floor = next_upper_floor

        else:

            next_lower_floor = ElevatorHelper.get_next_lower_floor(elevator, floors_pipeline)

            # means the elevator has reached its lowermost requested destination
            if next_lower_floor > ElevatorHelper.get_current_floor_of_elevator(elevator):

                next_upper_floor = ElevatorHelper.get_next_upper_floor(elevator, floors_pipeline)

                next_floor = next_upper_floor

            next_floor = next_lower_floor
        
        return next_floor

    @staticmethod
    def get_next_upper_floor(elevator, floors_pipeline):

        current_floor = ElevatorHelper.get_current_floor_of_elevator(elevator)

        return min(
            floors_pipeline,
            key=lambda x: abs(x-current_floor) if x > current_floor else FLOORS_COUNT
        )

    @staticmethod
    def get_next_lower_floor(elevator, floors_pipeline):

        current_floor = ElevatorHelper.get_current_floor_of_elevator(elevator)

        return min(
            floors_pipeline,
            key=lambda x: abs(x-current_floor) if x < current_floor else FLOORS_COUNT
        )

    @staticmethod
    def get_current_floor_of_elevator(elevator):

        return elevator.next_destination

    @staticmethod
    def update_elevator_state_on_elevator_opening(elevator, next_destination):

        # updating last_destination in cache, will be required to update elevator direction once
        # elevator stops and then starts after sometime
        CacheHelper.set_value_for_key_in_cache(
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
        CacheHelper.set_value_for_key_in_cache(
            CACHE_NEXT_DIRECTION_KEY % elevator.id,
            next_direction
        )

        return

    @staticmethod
    def update_elevator_state_on_elevator_closing(elevator):

        next_direction =  CacheHelper.get_next_direction_from_cache(elevator.id)

        elevator.direction = next_direction
        elevator.save()

        return
