from datetime import datetime

from challenge.database.models.models import IssPosition
from challenge.database.models.visibility import Visibility


def get_daylight_time_windows(iss_positions: list[IssPosition]) -> list[tuple]:
    """
    Provides a List of Daylight time windows given a list of IssPosition. The time window is defined as following:
    the first timestamp is the datetime of a Daylight IssPosition when the previous one is Eclipsed, the second
    timestamp is the datetime of the first Eclipsed IssPosition after the time window's first timestamp
    :param iss_positions: the List of IssPosition
    :return: a List of Tuples representing daylight time windows
    """
    start_window = None
    daylight_time_windows = []
    for i in range(0, len(iss_positions)):
        current_position = iss_positions[i]
        if i == 0:
            _append_if_not_none(daylight_time_windows, _get_first_daylight_time_window(current_position, iss_positions))
        elif i == len(iss_positions) - 1:
            _append_if_not_none(daylight_time_windows,
                                _get_last_daylight_time_window(current_position, iss_positions, start_window))
        elif current_position.visibility == Visibility.DAYLIGHT:
            if iss_positions[i - 1].visibility == Visibility.ECLIPSED:
                start_window = current_position.timestamp
            if iss_positions[i + 1].visibility == Visibility.ECLIPSED:
                daylight_time_windows.append((start_window, iss_positions[i + 1].timestamp))
                start_window = None
    return daylight_time_windows


def _append_if_not_none(daylight_time_windows: list[tuple], time_window: tuple):
    if time_window:
        daylight_time_windows.append(time_window)


def _get_first_daylight_time_window(current_position: IssPosition, iss_positions: list[IssPosition]) -> tuple:
    if current_position.visibility == Visibility.DAYLIGHT:
        if len(iss_positions) - 1 == 0:
            return None, None
        elif iss_positions[1].visibility == Visibility.ECLIPSED:
            return None, iss_positions[1].timestamp


def _get_last_daylight_time_window(current_position: IssPosition, iss_positions: list[IssPosition],
                                   start_window: datetime) -> tuple:
    i = len(iss_positions) - 1
    if current_position.visibility == Visibility.DAYLIGHT:
        if not start_window and iss_positions[i - 1].visibility == Visibility.ECLIPSED:
            start_window = current_position.timestamp
        return start_window, None

## Alternative time windows
# def get_daylight_time_windows_alternative(iss_positions: list[IssPosition]) -> list[tuple]:
#     """
#     Provides a List of Daylight time windows given a list of IssPosition. The time window is defined as following:
#     the first timestamp is the datetime of an Eclipsed IssPosition when the next one has Daylight visibility, the second
#     timestamp is the datetime of the last Daylight IssPosition before the next Eclipsed IssPosition
#     :param iss_positions: the List of IssPosition
#     :return: a List of Tuples representing daylight time windows
#     """
#     start_window = None
#     daylight_time_windows = []
#     for i in range(0, len(iss_positions)):
#         current_position = iss_positions[i]
#         if i == 0:
#             if current_position.visibility == Visibility.DAYLIGHT:
#                 if i == len(iss_positions) - 1:
#                     daylight_time_windows.append((None, None))
#                 elif iss_positions[i + 1].visibility == Visibility.ECLIPSED:
#                     daylight_time_windows.append((start_window, current_position.timestamp))
#         elif i == len(iss_positions) - 1:
#             if current_position.visibility == Visibility.DAYLIGHT:
#                 if not start_window and iss_positions[i - 1].visibility == Visibility.ECLIPSED:
#                     start_window = iss_positions[i - 1].timestamp
#                 daylight_time_windows.append((start_window, None))
#         elif current_position.visibility == Visibility.DAYLIGHT:
#             if iss_positions[i - 1].visibility == Visibility.ECLIPSED:
#                 start_window = iss_positions[i - 1].timestamp
#             if iss_positions[i + 1].visibility == Visibility.ECLIPSED:
#                 daylight_time_windows.append((start_window, current_position.timestamp))
#                 start_window = None
#     return daylight_time_windows
