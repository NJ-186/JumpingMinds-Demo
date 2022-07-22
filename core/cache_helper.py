from django.core.cache import cache

from .constants import *

class CacheHelper:

    @staticmethod
    def get_value_for_key_from_cache(key):

        value = cache.get(key)

        return value

    @staticmethod
    def set_value_for_key_in_cache(key, value):

        cache.set(key, value)

        return

    @staticmethod
    def update_cache_with_elevator_request(elevator_id, requested_floor):

        is_initial_request = False

        floors_pipeline = CacheHelper.get_value_for_key_from_cache(elevator_id)

        if floors_pipeline:
            floors_pipeline.append(requested_floor)

        else:
            floors_pipeline = [requested_floor]
            is_initial_request = True

        CacheHelper.set_value_for_key_in_cache(elevator_id, floors_pipeline)

        return is_initial_request

    @staticmethod
    def get_last_destination_from_cache(elevator_id):

        return CacheHelper.get_value_for_key_from_cache(
            CACHE_LAST_DESTINATION_KEY % elevator_id
        )

    @staticmethod
    def get_floors_pipeline_from_cache(elevator_id):

        return CacheHelper.get_value_for_key_from_cache(elevator_id)

    @staticmethod
    def get_next_direction_from_cache(elevator_id):

        return CacheHelper.get_value_for_key_from_cache(
            CACHE_NEXT_DIRECTION_KEY % elevator_id
        )
