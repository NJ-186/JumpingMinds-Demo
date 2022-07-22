from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .views_helper import ValidationChecks, ResponseHelper
from .constants import *
from .impl import ElevatorImpl

# Create your views here.


class AddElevators(APIView):

    def post(self, request):
        try:
            elevator_count = request.data.get('elevator_count')

            validation_check = ValidationChecks()
            request_validation_errors = validation_check.validate_add_elevator_request(elevator_count)

            if request_validation_errors:
                res = ResponseHelper.get_error_response(request_validation_errors)

                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res_object = ElevatorImpl.add_elevators(elevator_count=int(elevator_count))

            if res_object.get('error_message'):
                return Response(
                    res_object,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res_object = ResponseHelper.get_success_response()

            return Response(
                res_object,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            res = ResponseHelper.get_error_response(str(e))

            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CallElevator(APIView):

    def post(self, request):
        try:
            elevator_id = request.data.get('elevator_id')
            requested_floor = request.data.get('requested_floor')

            validation_check = ValidationChecks()
            request_validation_errors = validation_check.validate_call_elevator_request(elevator_id, requested_floor)

            if request_validation_errors:
                res = ResponseHelper.get_error_response(request_validation_errors)

                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res_manager = ElevatorImpl(elevator_id=int(elevator_id), requested_floor=int(requested_floor))
            res_object = res_manager.call_elevator()

            if res_object.get('error_message'):
                return Response(
                    res_object,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res_object = ResponseHelper.get_success_response()

            return Response(res_object, status=status.HTTP_200_OK)

        except Exception as e:
            res = ResponseHelper.get_error_response(str(e))

            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchAllRequests(APIView):

    def get(self, request):
        try:
            elevator_id = request.GET.get('elevator_id')

            request_validation_errors = ValidationChecks.validate_elevator_id(elevator_id)

            if request_validation_errors:
                res = ResponseHelper.get_error_response(request_validation_errors)

                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res_manager = ElevatorImpl(elevator_id=elevator_id)
            res_object = res_manager.get_all_requests_for_elevator()

            if res_object.get('error_message'):
                return Response(
                    res_object,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res_object = ResponseHelper.get_success_response(res_object)

            return Response(res_object, status=status.HTTP_200_OK)

        except Exception as e:
            res = ResponseHelper.get_error_response(str(e))

            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchNextDestination(APIView):

    def get(self, request):
        try:
            elevator_id = request.GET.get('elevator_id')

            request_validation_errors = ValidationChecks.validate_elevator_id(elevator_id)

            if request_validation_errors:
                res = ResponseHelper.get_error_response(request_validation_errors)

                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            res_manager = ElevatorImpl(elevator_id=elevator_id)
            res_object = res_manager.get_elevator_next_destination()

            if res_object.get('error_message'):
                return Response(
                    res_object,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            res_object = ResponseHelper.get_success_response(res_object)

            return Response(res_object, status=status.HTTP_200_OK)

        except Exception as e:
            res = ResponseHelper.get_error_response(str(e))

            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchDirection(APIView):

    def get(self, request):
        try:
            elevator_id = request.GET.get('elevator_id')

            request_validation_errors = ValidationChecks.validate_elevator_id(elevator_id)

            if request_validation_errors:
                res = ResponseHelper.get_error_response(request_validation_errors)

                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res_manager = ElevatorImpl(elevator_id=elevator_id)
            res_object = res_manager.get_elevator_direction()

            if res_object.get('error_message'):
                return Response(
                    res_object,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            res_object = ResponseHelper.get_success_response(res_object)

            return Response(res_object, status=status.HTTP_200_OK)

        except Exception as e:
            res = ResponseHelper.get_error_response(str(e))

            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarkElevatorDown(APIView):

    def get(self, request):
        try:
            elevator_id = request.GET.get('elevator_id')

            request_validation_errors = ValidationChecks.validate_elevator_id(elevator_id)

            if request_validation_errors:
                res = ResponseHelper.get_error_response(request_validation_errors)

                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res_manager = ElevatorImpl(elevator_id=elevator_id)
            res_object = res_manager.mark_elevator_down()

            if res_object.get('error_message'):
                return Response(
                    res_object,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res_object = ResponseHelper.get_success_response(res_object)

            return Response(res_object, status=status.HTTP_200_OK)

        except Exception as e:
            res = ResponseHelper.get_error_response(str(e))

            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OpenOrCloseDoor(APIView):

    def post(self, request):
        try:
            elevator_id = request.data.get('elevator_id')
            door_state = request.data.get('door_state')

            validation_check = ValidationChecks()
            request_validation_errors = validation_check.validate_open_or_close_door_request(
                elevator_id,
                door_state
            )

            if request_validation_errors:
                res = ResponseHelper.get_error_response(request_validation_errors)

                return Response(
                    res,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res_manager = ElevatorImpl(elevator_id=elevator_id, door_state=door_state)
            res_object = res_manager.open_or_close_door()

            if res_object.get('error_message'):
                return Response(
                    res_object,
                    status=status.HTTP_400_BAD_REQUEST
                )

            res_object = ResponseHelper.get_success_response(res_object)

            return Response(res_object, status=status.HTTP_200_OK)

        except Exception as e:
            res = ResponseHelper.get_error_response(str(e))

            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
