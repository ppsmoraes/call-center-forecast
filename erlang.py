"""Module that calculates important metrics for a call center planinng."""

from math import exp, factorial
from typing import overload


def calls_per_hour(calls: int, period: float) -> float:
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
    *, calls: int, period: float, average_handling_time: float
) -> float: ...
@overload
def traffic_intensity(
    *, calls_per_hour: float, average_handling_time: float
) -> float: ...
def traffic_intensity(**kwargs) -> float:
    """
    Calculate traffic intensity (in Erlangs).

    Usage modes:
    ------------
    - traffic_intensity(calls=..., period=..., average_handling_time=...)
    - traffic_intensity(calls_per_hour=..., average_handling_time=...)

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
        calls: int = kwargs.pop('calls')
        period: float = kwargs.pop('period')
        cph: float = calls_per_hour(calls, period)

    return cph * (aht / 3600)


@overload
def erlang_c(
    *, calls: int, period: float, average_handling_time: float, agents: int
) -> float: ...
@overload
def erlang_c(
    *, calls_per_hour: float, average_handling_time: float, agents: int
) -> float: ...
@overload
def erlang_c(*, traffic_intensity: float, agents: int) -> float: ...
def erlang_c(**kwargs) -> float:
    """
    Calculate the probability that a call will wait in queue (Erlang C formula).

    Usage modes:
    ------------
    - erlang_c(calls=..., period=..., average_handling_time=..., agents=...)
    - erlang_c(calls_per_hour=..., average_handling_time=..., agents=...)
    - erlang_c(traffic_intensity=..., agents=...)

    Parameters
    ----------
    calls : int, optional
        Total number of calls in a time period.
    period : float, optional
        Time period in minutes.
    calls_per_hour : float, optional
        Calls per hour.
    average_handling_time : float, optional
        Average handling time (in seconds).
    traffic_intensity : float, optional
        Offered traffic (in Erlangs).
    agents : int
        Number of available agents.

    Returns
    -------
    float
        Probability that a call will wait in queue (Erlang C).

    Raises
    ------
    ValueError
        If required parameters are missing or inconsistent.
    """
    agents: int = kwargs.pop('agents')

    try:
        ti: float = kwargs.pop('traffic_intensity')
    except KeyError:
        aht: float = kwargs.pop('average_handling_time')

        try:
            cph: float = kwargs.pop('calls_per_hour')
        except KeyError:
            calls: int = kwargs.pop('calls')
            period: float = kwargs.pop('period')
            cph: float = calls_per_hour(calls, period)

        ti: float = traffic_intensity(calls_per_hour=cph, average_handling_time=aht)

    num: float = ti**agents / factorial(agents)
    den: float = (1 - ti / agents) * sum(ti**i / factorial(i) for i in range(agents))
    return num / (den + num)


# TODO Remove all if/else, use try/except instead. Use only one definition.
@overload
def service_level(
    *,
    erlang_c: float,
    traffic_intensity: float,
    agents: int,
    target_time: float,
    average_handling_time: float,
) -> float: ...
@overload
def service_level(
    *,
    calls: int,
    period: float,
    agents: int,
    target_time: float,
    average_handling_time: float,
) -> float: ...
@overload
def service_level(
    *,
    calls_per_hour: float,
    agents: int,
    target_time: float,
    average_handling_time: float,
) -> float: ...
@overload
def service_level(
    *,
    traffic_intensity: float,
    agents: int,
    target_time: float,
    average_handling_time: float,
) -> float: ...
def service_level(**kwargs) -> float:
    """
    Calculate the estimated service level.

    This function supports multiple input forms. If `ec` (Erlang C) is not provided,
    it will be calculated automatically using available parameters with the `erlang_c` function.
    Likewise, if `traffic` is not provided, it will be computed via `traffic_intensity`.

    Parameters
    ----------
    ec : float, optional
        Probability that a call waits in queue (Erlang C).
    resources / agents : int
        Number of available agents.
    traffic / traffic_intensity : float, optional
        Traffic intensity in Erlangs.
    calls : int, optional
        Total number of calls in a time period.
    period : float, optional
        Time period in minutes.
    calls_per_hour : float, optional
        Number of calls per hour.
    aht : float
        Average handling time in seconds.
    target_time : float
        Target service level time in seconds.

    Returns
    -------
    float
        Estimated service level (probability that a call is answered within the target time).

    Raises
    ------
    ValueError
        If required parameters are missing or inconsistent.
    """

    agents = kwargs['agents']
    aht = kwargs['average_handling_time']
    target_time = kwargs['target_time']

    required = ['aht', 'target_time']
    missing = [p for p in required if p not in kwargs]
    if missing:
        raise ValueError(f"Missing required parameter(s): {', '.join(missing)}")

    ec = kwargs.get('erlang_c')
    if ec is None:
        ec = erlang_c(**kwargs)
        kwargs['ec'] = ec

    traffic = kwargs.get('traffic') or kwargs.get('traffic_intensity')
    if traffic is None:
        traffic = traffic_intensity(**kwargs)
        kwargs['traffic'] = traffic

    agents = kwargs.get('agents') or kwargs.get('resources')
    if agents is None:
        raise ValueError("Missing required parameter: 'agents' or 'resources'")

    return 1 - (ec * exp((traffic - agents) * (target_time / aht)))
def service_level(
    ec: float, resources: int, traffic: float, target_time: float, aht: float
) -> float:
    """Calculate the estimated service level.

    Parameters
    ----------
    ec : float
        Probability of a call going to the queue. AKA erlang-c.
    resources : int
        The number of agents that can answer those calls.
    traffic : float
        The traffic intensity.
    target_time : float
        The target time for the service level in seconds
    aht : float
        Average handling time in seconds.

    Returns
    -------
    float
        The service level.
    """
    return 1 - (ec * exp((traffic - resources) * (target_time / aht)))


# TODO Build this function
def estimate_agent_required(): ...


# TODO Create tests for this module and delete the main function
def main() -> None:
    """
    Required Service Level – 80%
    Maximum Occupancy – 85%
    Shrinkage – 30%

    https://www.callcentrehelper.com/erlang-c-formula-example-121281.htm
    """
    calls = 100  # Number of calls
    period = 30  # Period of time in minutes
    aht = 180  # Average Handling Time in seconds
    target_time = 20  # The target answer time for the service level
    agents = 11  # The number of agents that can answer those calls

    cph = calls_per_hour(calls, period)
    print(f'Calls per hour: {cph}')

    traffic = traffic_intensity(cph, aht)
    print(f'Traffic intensity: {traffic}')

    ec = erlang_c(traffic, agents)
    print(f'Erlang-c: {ec:.3%}')

    sl = service_level(ec, agents, traffic, target_time, aht)
    print(f'Service Level: {sl:.3%}')


if __name__ == '__main__':
    main()
