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


# def test_erlang_c_traffic_less_than_servers():
#     assert erlang_c(2, 5) == 0.0

# def test_erlang_c_waiting_probability():
#     assert math.isclose(erlang_c_waiting_probability(10, 10), 0.4286, rel_tol=1e-3)

# def test_erlang_c_average_wait_time():
#     # Test with known values
#     assert math.isclose(erlang_c_average_wait_time(10, 10, 1), 0.4286, rel_tol=1e-3)

# def test_erlang_c_invalid_input():
#     with pytest.raises(ValueError):
#         erlang_c(-1, 5)
#     with pytest.raises(ValueError):
#         erlang_c(5, -1)
