"""Module that calculates important metrics for a call center planinng."""

from math import ceil, exp, factorial
from typing import overload


def calls_per_hour(calls: int, period: float) -> float:
    # TODO Add exemples
    """Calculate the number of calls per hour.

    Parameters
    ----------
    calls : float
        The number of calls.
    period : int
        The period of time in minutes.

    Returns
    -------
    float
        The calls per hour.
    """
    return calls * (60 / period)


@overload
def traffic_intensity(
    *, calls_per_hour: float, average_handling_time: float
) -> float: ...
@overload
def traffic_intensity(
    *, calls: int, period: float, average_handling_time: float
) -> float: ...
def traffic_intensity(**kwargs) -> float:
    # TODO Add exemples
    """
    Calculate traffic intensity (in Erlangs).

    Usage modes:
    ------------
    - traffic_intensity(calls_per_hour=..., average_handling_time=...)
    - traffic_intensity(calls=..., period=..., average_handling_time=...)

    Parameters
    ----------
    calls : int, optional
        Total number of calls in a period.
    period : float, optional
        Period of time in minutes.
    calls_per_hour : float, optional
        Number of calls per hour.
    average_handling_time : float
        Average handling time (in seconds).

    Returns
    -------
    float
        Traffic intensity in Erlangs.
    """
    aht: float = kwargs.pop('average_handling_time')
    try:
        cph: float = kwargs.pop('calls_per_hour')
    except KeyError:
        cph: float = calls_per_hour(**kwargs)

    return cph * (aht / 3600)


@overload
def erlang_c(*, traffic_intensity: float, agents: int) -> float: ...
@overload
def erlang_c(
    *, calls_per_hour: float, average_handling_time: float, agents: int
) -> float: ...
@overload
def erlang_c(
    *, calls: int, period: float, average_handling_time: float, agents: int
) -> float: ...
def erlang_c(**kwargs) -> float:
    # TODO Add exemples
    """
    Calculate the probability that a call will wait in queue (Erlang C formula).

    Usage modes:
    ------------
    - erlang_c(traffic_intensity=..., agents=...)
    - erlang_c(calls_per_hour=..., average_handling_time=..., agents=...)
    - erlang_c(calls=..., period=..., average_handling_time=..., agents=...)

    Parameters
    ----------
    traffic_intensity : float, optional
        Offered traffic (in Erlangs).
    calls_per_hour : float, optional
        Calls per hour.
    calls : int, optional
        Total number of calls in a time period.
    period : float, optional
        Time period in minutes.
    average_handling_time : float, optional
        Average handling time (in seconds).
    agents : int
        Number of available agents.

    Returns
    -------
    float
        Probability that a call will wait in queue (Erlang C).
    """
    agents: int = kwargs.pop('agents')
    try:
        ti: float = kwargs.pop('traffic_intensity')
    except KeyError:
        ti: float = traffic_intensity(**kwargs)

    num: float = ti**agents / factorial(agents)
    den: float = (1 - ti / agents) * sum(ti**i / factorial(i) for i in range(agents))
    return num / (den + num)


@overload
def service_level(
    *,
    erlang_c: float,
    traffic_intensity: float,
    average_handling_time: float,
    agents: int,
    target_time: float,
) -> float: ...
@overload
def service_level(
    *,
    erlang_c: float,
    calls_per_hour: float,
    average_handling_time: float,
    agents: int,
    target_time: float,
) -> float: ...
@overload
def service_level(
    *,
    erlang_c: float,
    calls: float,
    period: float,
    average_handling_time: float,
    agents: int,
    target_time: float,
) -> float: ...
@overload
def service_level(
    *,
    traffic_intensity: float,
    average_handling_time: float,
    agents: int,
    target_time: float,
) -> float: ...
@overload
def service_level(
    *,
    calls_per_hour: float,
    average_handling_time: float,
    agents: int,
    target_time: float,
) -> float: ...
@overload
def service_level(
    *,
    calls: int,
    period: float,
    average_handling_time: float,
    agents: int,
    target_time: float,
) -> float: ...
def service_level(**kwargs) -> float:
    # TODO Add usage modes
    # TODO Add exemples
    """
    Calculate the estimated service level.

    Parameters
    ----------
    erlang_c : float, optional
        Probability that a call waits in queue (Erlang C).
    traffic_intensity : float, optional
        Traffic intensity in Erlangs.
    calls_per_hour : float, optional
        Number of calls per hour.
    calls : int, optional
        Total number of calls in a time period.
    period : float, optional
        Time period in minutes.
    average_handling_time : float
        Average handling time in seconds.
    agents : int
        Number of available agents.
    target_time : float
        Target service level time in seconds.

    Returns
    -------
    float
        Estimated service level (probability that a call is answered within the target time).
    """
    aht: float = kwargs.pop('average_handling_time')
    agents: int = kwargs.pop('agents')
    tt: int = kwargs.pop('target_time')
    try:
        ti: float = kwargs.pop('traffic_intensity')
    except KeyError:
        ti: float = traffic_intensity(average_handling_time=aht, **kwargs)
    try:
        ec: float = kwargs.pop('erlang_c')
    except KeyError:
        ec: float = erlang_c(agents=agents, traffic_intensity=ti)

    return 1 - (ec * exp((ti - agents) * (tt / aht)))


def agents_required(
    traffic_intensity: float,
    average_handling_time: float,
    target_time: float,
    target_service_level: float,
) -> int:
    # TODO Create docstring
    ti: float = traffic_intensity
    aht: float = average_handling_time
    tt: float = target_time
    agents: int = ceil(ti)
    while (
        service_level(
            traffic_intensity=ti,
            average_handling_time=aht,
            agents=agents,
            target_time=tt,
        )
        < target_service_level
    ):
        agents += 1
    return agents


# TODO Create tests for this module and delete the main function
def main() -> None:
    """
    Maximum Occupancy – 85%
    Shrinkage – 30%

    https://www.callcentrehelper.com/erlang-c-formula-example-121281.htm
    """
    calls = 100  # Number of calls
    period = 30  # Period of time in minutes
    aht = 180  # Average Handling Time in seconds
    target_time = 20  # The target answer time for the service level
    target_service_level = 0.8  # The constracted service level

    cph = calls_per_hour(calls, period)
    print(f'Calls per hour: {cph}')

    ti = traffic_intensity(calls_per_hour=cph, average_handling_time=aht)
    print(f'Traffic intensity: {ti}')

    agents: int = agents_required(ti, aht, target_time, target_service_level)
    print(f'Agents: {agents}')

    ec = erlang_c(traffic_intensity=ti, agents=agents)
    print(f'Erlang-c: {ec:.3%}')

    sl = service_level(
        erlang_c=ec,
        agents=agents,
        traffic_intensity=ti,
        target_time=target_time,
        average_handling_time=aht,
    )
    print(f'Service Level: {sl:.3%}')


if __name__ == '__main__':
    main()
