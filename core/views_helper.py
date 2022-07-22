from .impl import ElevatorHelper
from .constants import *

class ValidationChecks:

    def __init__(self):
        self.validation_error = ""

    def get_validation_error(self):
        return self.validation_error

    def set_validation_error(self, validation_error):
        self.validation_error = validation_error

    def validate_add_elevator_request(self, elevator_count):

        if not elevator_count:
            error = "elevator_count is a required field."

            self.set_validation_error(error)

        return self.get_validation_error()

    def validate_call_elevator_request(self, elevator_id, requested_floor):

        error = ValidationChecks.validate_elevator_id(elevator_id)

        if not error:
            error = ValidationChecks.validate_requested_floor(requested_floor)

        self.set_validation_error(error)

        return self.get_validation_error()

    def validate_open_or_close_door_request(self, elevator_id, door_state):

        error = ValidationChecks.validate_elevator_id(elevator_id)

        if not error:
            error = ValidationChecks.validate_door_state(door_state)

        self.set_validation_error(error)

        return self.get_validation_error()

    @staticmethod
    def validate_elevator_id(elevator_id):
        error = ""

        if not elevator_id:
            error = "elevator_id is a required field."

        elif not ValidationChecks.validate_elevator_object(elevator_id):
            error = "invalid elevator_id."

        return error

    @staticmethod
    def validate_elevator_object(elevator_id):

        try:
            elevator = ElevatorHelper.get_elevator_object(elevator_id)
        except:
            elevator = None

        if elevator:
            return True

        return False

    @staticmethod
    def validate_requested_floor(requested_floor):
        error = ""

        if not requested_floor:
            error = "requested_floor is a required field."

        elif int(requested_floor) not in range(0, FLOORS_COUNT):
            error = "invalid requested_floor."

        return error

    @staticmethod
    def validate_door_state(door_state):
        error = ""

        if door_state not in [OPEN, CLOSE]:
            error = "invalid door_state."

        return error


class ResponseHelper:

    @staticmethod
    def get_success_response(data=None):

        res = {
            'success': True
        }

        if data:
            res['data'] = data

        return res

    @staticmethod
    def get_error_response(error):

        return {
            'success': False,
            'error_message': error
        }
