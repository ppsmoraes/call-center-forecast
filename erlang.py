from math import exp, factorial


def calls_per_hour(calls: int, period: int) -> float:
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


def traffic_intensity(cph: float, aht: float) -> float:
    """Calculate the traffic intensity.

    Parameters
    ----------
    cph : float
        Calls per hour.
    aht : float
        Average handling time in seconds.

    Returns
    -------
    float
        The traffic intensity
    """
    return cph * (aht / 3600)


def erlang_c(traffic: float, resources: int) -> float:
    """Calculates the probability of a call going to the queue.

    Parameters
    ----------
    traffic : float
        The traffic intensity.
    resources : int
        The number of agents that can answer those calls.

    Returns
    -------
    float
        Probability of a call going to the queue.
    """
    num: float = traffic**resources / factorial(resources)
    den: float = (1 - traffic / resources) * sum(
        traffic**i / factorial(i) for i in range(resources)
    )
    return num / (den + num)


def service_level(
    ec: float, resources: int, traffic: float, target_time: float, aht: float
) -> float:
    """Calculates the estimated servive level.

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
