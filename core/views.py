from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Elevator, ElevatorRequests
from .serializers import ElevatorSerializer, ElevatorRequestsSerializer
from .constants import *
from .helper import *

# Create your views here.


class AddElevators(APIView):

    def _validate_request(self, elevator_count):
        res = {}

        if not elevator_count:
            res = {
                "error_message": "elevator_count is a required field."
            }

        return res

    def post(self, request):
        try:
            elevator_count = int(request.data.get('elevator_count'))

            request_validation_errors = self._validate_request(elevator_count)

            if request_validation_errors:
                return Response(
                    request_validation_errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            elevators = get_all_elevators()

            if elevators:
                res = {
                    "error_message": "It looks like you have already updated the elevator_count."
                }
                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )

            create_elevators_initially(elevator_count)

            res = {
                "success": True
            }

            return Response(res, status=status.HTTP_201_CREATED)

        except Exception as e:
            res = {
                "Exception" : str(e)
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CallElevator(APIView):

    def _validate_request(self, elevator_id, requested_floor):
        res = {}

        if not elevator_id:
            res = {
                "error_message": "elevator_id is a required field."
            }

        elif not validate_elevator_object(elevator_id):
            res = {
                "error_message": "invalid elevator_id."
            }

        elif not requested_floor:
            res = {
                "error_message": "requested_floor is a required field."
            }

        elif requested_floor not in range(0, FLOORS_COUNT):
            res = {
                "error_message": "invalid requested_floor."
            }

        return res

    def post(self, request):
        try:
            elevator_id = request.data.get('elevator_id')
            requested_floor = int(request.data.get('requested_floor'))

            request_validation_errors = self._validate_request(elevator_id, requested_floor)

            if request_validation_errors:
                return Response(
                    request_validation_errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            is_elevator_down = check_if_elevator_is_down(elevator_id)

            if is_elevator_down:
                return Response(
                    is_elevator_down,
                    status=status.HTTP_400_BAD_REQUEST
                )

            is_initial_request = update_cache_for_elevator_request(elevator_id, requested_floor)

            update_db_for_elevator_request(elevator_id, requested_floor, is_initial_request)

            res = {
                "success": True
            }

            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            res = {
                "Exception" : str(e)
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchAllRequests(APIView):

    def get(self, request):
        try:
            elevator_id = request.GET.get('elevator_id')

            request_validation_errors = validate_get_request(elevator_id)

            if request_validation_errors:
                return Response(
                    request_validation_errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            is_elevator_down = check_if_elevator_is_down(elevator_id)

            if is_elevator_down:
                return Response(
                    is_elevator_down,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res = get_all_requests_for_elevator(elevator_id)

            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            res = {
                "Exception" : str(e)
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchNextDestination(APIView):

    def get(self, request):
        try:
            elevator_id = request.GET.get('elevator_id')

            request_validation_errors = validate_get_request(elevator_id)

            if request_validation_errors:
                return Response(
                    request_validation_errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            is_elevator_down = check_if_elevator_is_down(elevator_id)

            if is_elevator_down:
                return Response(
                    is_elevator_down,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res = get_elevator_next_destination(elevator_id)

            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            res = {
                "Exception" : str(e)
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchDirection(APIView):

    def get(self, request):
        try:
            elevator_id = request.GET.get('elevator_id')

            request_validation_errors = validate_get_request(elevator_id)

            if request_validation_errors:
                return Response(
                    request_validation_errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            is_elevator_down = check_if_elevator_is_down(elevator_id)

            if is_elevator_down:
                return Response(
                    is_elevator_down,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res = get_elevator_direction(elevator_id)

            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            res = {
                "Exception" : str(e)
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class MarkElevatorDown(APIView):

    def get(self, request):
        try:
            elevator_id = request.GET.get('elevator_id')

            request_validation_errors = validate_get_request(elevator_id)

            if request_validation_errors:
                return Response(
                    request_validation_errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            is_elevator_down = check_if_elevator_is_down(elevator_id)

            if is_elevator_down:
                res = {
                    "error_message": "Elevator is already under maintenance"
                }
                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )

            mark_elevator_down(elevator_id)

            res = {
                "success": True
            }

            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            res = {
                "Exception" : str(e)
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OpenOrCloseDoor(APIView):

    def _validate_request(self, elevator_id, door_state):
        res = {}

        if not elevator_id:
            res = {
                "error_message": "elevator_id is a required field."
            }

        elif not validate_elevator_object(elevator_id):
            res = {
                "error_message": "invalid elevator_id."
            }

        elif door_state not in [OPEN, CLOSE]:
            res = {
                "error_message": "invalid door_state."
            }

        return res

    def post(self, request):
        try:
            elevator_id = request.data.get('elevator_id')
            door_state = request.data.get('door_state')

            request_validation_errors = self._validate_request(elevator_id, door_state)

            if request_validation_errors:
                return Response(
                    request_validation_errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            is_elevator_down = check_if_elevator_is_down(elevator_id)

            if is_elevator_down:
                res = {
                    "error_message": "Elevator is already under maintenance"
                }
                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )

            if door_state == OPEN:
                res = open_elevator(elevator_id)

            else:
                res = close_elevator(elevator_id)

            if res:
                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res = {
                "success": True
            }

            return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            res = {
                "Exception" : str(e)
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
