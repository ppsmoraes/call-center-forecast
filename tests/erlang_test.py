from datetime import datetime

from erlang import CallCenterPredictions


def test_traffic_intensity() -> None:
    # Test with known values
    pred: CallCenterPredictions = CallCenterPredictions(
        start_time=datetime(2021, 4, 1, 8),
        end_time=datetime(2021, 4, 1, 8, 30),
        calls=100,
        average_handling_time=180,
        target_service_level=0.8,
        target_answer_time=20,
    )

    result: float = pred.traffic_intensity()
    expected: float = 10.0

    assert expected == result

    pred_2: CallCenterPredictions = CallCenterPredictions(
        start_time=datetime(2020, 7, 6, 13),
        end_time=datetime(2020, 7, 6, 14),
        calls=230,
        average_handling_time=180,
        target_service_level=0.8,
        target_answer_time=20,
    )

    result_2: float = pred_2.traffic_intensity()
    expected_2: float = 11.5

    assert expected_2 == result_2
