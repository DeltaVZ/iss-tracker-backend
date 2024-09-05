from datetime import datetime, timedelta

import pytest

from challenge.database.models.models import IssPosition
from challenge.database.models.visibility import Visibility
from challenge.utils.operations.time_windows_utils import get_daylight_time_windows


@pytest.fixture
def timestamps(size: int = 11):
    timestamps = []
    now = datetime.fromtimestamp(1699577271)
    for i in range(size - 1, 0, -1):
        timestamps.append(now - timedelta(minutes=i))
    return timestamps


def test_get_complex_window(timestamps):
    expected_result = [(timestamps[2], timestamps[5]),
                       (timestamps[7], timestamps[9])]
    test_list = [IssPosition(visibility=Visibility.ECLIPSED, timestamp=timestamps[0]),
                 IssPosition(visibility=Visibility.ECLIPSED,
                             timestamp=timestamps[1]),
                 IssPosition(visibility=Visibility.DAYLIGHT,
                             timestamp=timestamps[2]),
                 IssPosition(visibility=Visibility.DAYLIGHT,
                             timestamp=timestamps[3]),
                 IssPosition(visibility=Visibility.DAYLIGHT,
                             timestamp=timestamps[4]),
                 IssPosition(visibility=Visibility.ECLIPSED,
                             timestamp=timestamps[5]),
                 IssPosition(visibility=Visibility.ECLIPSED,
                             timestamp=timestamps[6]),
                 IssPosition(visibility=Visibility.DAYLIGHT,
                             timestamp=timestamps[7]),
                 IssPosition(visibility=Visibility.DAYLIGHT,
                             timestamp=timestamps[8]),
                 IssPosition(visibility=Visibility.ECLIPSED, timestamp=timestamps[9])]
    time_windows = get_daylight_time_windows(test_list)
    assert time_windows == expected_result


def test_get_daylight_start_cases(timestamps):
    """
       Tests get_daylight_time_windows when the list of IssPosition start with daylight visibility
       :param timestamps: the timestamps fixture
       """
    expected_result = [(None, timestamps[3]), (timestamps[4], timestamps[7])]

    # 1: Test that a single start daylight is handled correctly
    test_list = [IssPosition(visibility=Visibility.DAYLIGHT, timestamp=timestamps[2]),
                 IssPosition(visibility=Visibility.ECLIPSED,
                             timestamp=timestamps[3]),
                 IssPosition(visibility=Visibility.DAYLIGHT,
                             timestamp=timestamps[4]),
                 IssPosition(visibility=Visibility.DAYLIGHT,
                             timestamp=timestamps[5]),
                 IssPosition(visibility=Visibility.DAYLIGHT,
                             timestamp=timestamps[6]),
                 IssPosition(visibility=Visibility.ECLIPSED,
                             timestamp=timestamps[7]),
                 IssPosition(visibility=Visibility.ECLIPSED, timestamp=timestamps[8])]
    time_windows = get_daylight_time_windows(test_list)
    assert time_windows == expected_result

    # 2: Test that multiple start daylights are handled correctly
    test_list.insert(0, IssPosition(
        visibility=Visibility.DAYLIGHT, timestamp=timestamps[0]))
    test_list.insert(1, IssPosition(
        visibility=Visibility.DAYLIGHT, timestamp=timestamps[1]))
    time_windows = get_daylight_time_windows(test_list)
    assert time_windows == expected_result


def test_get_daylight_end_cases(timestamps):
    """
    Tests get_daylight_time_windows when the list of IssPosition end with daylight visibility
    :param timestamps: the timestamps fixture
    """

    expected_result = [(timestamps[2], timestamps[5]), (timestamps[7], None)]

    # 1: Test that a single end daylight is handled correctly
    test_list = [IssPosition(visibility=Visibility.ECLIPSED, timestamp=timestamps[0]),
                 IssPosition(visibility=Visibility.ECLIPSED,
                             timestamp=timestamps[1]),
                 IssPosition(visibility=Visibility.DAYLIGHT,
                             timestamp=timestamps[2]),
                 IssPosition(visibility=Visibility.DAYLIGHT,
                             timestamp=timestamps[3]),
                 IssPosition(visibility=Visibility.DAYLIGHT,
                             timestamp=timestamps[4]),
                 IssPosition(visibility=Visibility.ECLIPSED,
                             timestamp=timestamps[5]),
                 IssPosition(visibility=Visibility.ECLIPSED,
                             timestamp=timestamps[6]),
                 IssPosition(visibility=Visibility.DAYLIGHT, timestamp=timestamps[7])]
    time_windows = get_daylight_time_windows(test_list)
    assert time_windows == expected_result

    # 2: Test that multiple end daylights are handled correctly
    test_list.append(IssPosition(
        visibility=Visibility.DAYLIGHT, timestamp=timestamps[7]))
    test_list.append(IssPosition(
        visibility=Visibility.DAYLIGHT, timestamp=timestamps[8]))
    time_windows = get_daylight_time_windows(test_list)
    assert time_windows == expected_result


def test_get_daylight_small_lists(timestamps):
    """
    Tests get_daylight_time_windows in the edge cases of empty or small List of IssPosition
    :param timestamps: the timestamps fixture
    """

    # 1: Empty list
    test_list = []
    time_windows = get_daylight_time_windows(test_list)
    assert time_windows == []

    # 2: Singleton List with only a position with visibility Eclipsed
    test_list = [IssPosition(
        visibility=Visibility.ECLIPSED, timestamp=timestamps[0])]
    time_windows = get_daylight_time_windows(test_list)
    assert time_windows == []

    # 3: List with multiple Eclipsed positions
    test_list.append(IssPosition(
        visibility=Visibility.ECLIPSED, timestamp=timestamps[0]))
    time_windows = get_daylight_time_windows(test_list)
    assert time_windows == []

    # 4: Singleton List with only a position with visibility Daylight
    test_list = [IssPosition(
        visibility=Visibility.DAYLIGHT, timestamp=timestamps[0])]
    time_windows = get_daylight_time_windows(test_list)
    assert time_windows == [(None, None)]

    # 5: List with multiple Daylight positions
    test_list.append(IssPosition(
        visibility=Visibility.DAYLIGHT, timestamp=timestamps[1]))
    test_list.append(IssPosition(
        visibility=Visibility.DAYLIGHT, timestamp=timestamps[2]))
    time_windows = get_daylight_time_windows(test_list)
    assert time_windows == [(None, None)]
