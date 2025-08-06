"""Module that calculates important metrics for call center planning."""

from datetime import datetime
from math import ceil, exp, factorial

from pandas import DataFrame


class CallCenterPredictions:
    """Class that contains the predictable variables of a call center in a certain period of time."""

    def __init__(
        self,
        start_time: datetime,
        end_time: datetime,
        calls: int,
        average_handling_time: int,
        target_service_level: float,
        target_answer_time: int,
    ) -> None:
        """Initialize predictable variables of a call center in a certain period of time.

        Parameters
        ----------
        start_time : datetime
            The starting date and time.
        end_time : datetime
            The ending date and time.
        calls : int
            The number of expected calls in that period of time.
        average_handling_time : int
            The average handling time in seconds.
        target_service_level : float
            The service level required in that period of time. This should be a number between 0 and 1 (both ends included).
        target_answer_time : int
            The target service level time to answer a call in seconds.

        Returns
        -------
        CallCenterPredictions
            The predictable variables of a call center in a certain period of time.

        Raises
        ------
        ValueError
            If ``target_service_level`` given is not a number between 0 and 1 (both ends included).
        """
        self.start_time: datetime = start_time
        self.end_time: datetime = end_time
        self.calls: int = calls
        self.aht: int = average_handling_time
        self.tsl: float = target_service_level
        self.tat: int = target_answer_time

        if self.tsl > 1 or self.tsl < 0:
            raise ValueError(
                f'The target service level should be a number between 0 and 1 (both ends included). But {self.tsl} was given.'
            )

        self.erlangs: float = self.traffic_intensity()
        self.raw_agents: int = self.raw_agents_required()
        self.p_wait: float = self.erlang_c(self.raw_agents)

    def traffic_intensity(self) -> float:
        # TODO Add tests
        """Calculate traffic intensity (in Erlangs).

        Returns
        -------
        float
            Traffic intensity in Erlangs.

        Examples
        --------
        >>> from datetime import datetime
        >>> pred = CallCenterPredictions(
        ...     start_time=datetime(2021, 4, 1, 8),
        ...     end_time=datetime(2021, 4, 1, 9),
        ...     calls=390,
        ...     average_handling_time=300,
        ...     target_service_level=0.8,
        ...     target_answer_time=30,
        ... )
        >>> pred.traffic_intensity()
        32.5
        """
        _period = (self.end_time - self.start_time).total_seconds()
        return self.calls * (self.aht / _period)

    def erlang_c(self, agents: int) -> float:
        # TODO Add tests
        """Calculate the probability that a call will wait in queue (Erlang C formula).

        Parameters
        ----------
        agents : int
            The quantity of agents to answer those calls.

        Returns
        -------
        float
            Probability that a call will wait in queue (Erlang C).

        Examples
        --------
        >>> from datetime import datetime
        >>> pred = CallCenterPredictions(
        ...     start_time=datetime(2021, 4, 1, 8),
        ...     end_time=datetime(2021, 4, 1, 9),
        ...     calls=390,
        ...     average_handling_time=300,
        ...     target_service_level=0.8,
        ...     target_answer_time=30,
        ... )
        >>> pred.erlang_c(35)
        0.5700850250324968
        """
        _num: float = self.erlangs**agents / factorial(agents)
        _den: float = sum(self.erlangs**_ / factorial(_) for _ in range(agents)) * (
            1 - self.erlangs / agents
        )
        return _num / (_den + _num)

    def service_level(self, agents: int) -> float:
        # TODO Add tests
        """Calculate the estimated service level.

        Parameters
        ----------
        agents : int
            The quantity of agents to answer those calls.

        Returns
        -------
        float
            Estimated service level (probability that a call is answered within the target time).

        Examples
        --------
        >>> from datetime import datetime
        >>> pred = CallCenterPredictions(
        ...     start_time=datetime(2021, 4, 1, 8),
        ...     end_time=datetime(2021, 4, 1, 9),
        ...     calls=390,
        ...     average_handling_time=300,
        ...     target_service_level=0.8,
        ...     target_answer_time=30,
        ... )
        >>> pred.service_level(35)
        0.5560173360874101
        """
        return 1 - (
            self.erlang_c(agents) * exp((self.erlangs - agents) * (self.tat / self.aht))
        )

    def raw_agents_required(self) -> int:
        # TODO Considere the maximum occupancy too
        # TODO Add tests
        """Calculate the quantity of agents required to achieve the target service level.

        Returns
        -------
        int
            The minimum number of agents required to meet the target service level.

        Examples
        --------
        >>> from datetime import datetime
        >>> pred = CallCenterPredictions(
        ...     start_time=datetime(2021, 4, 1, 8),
        ...     end_time=datetime(2021, 4, 1, 9),
        ...     calls=390,
        ...     average_handling_time=300,
        ...     target_service_level=0.8,
        ...     target_answer_time=30,
        ... )
        >>> pred.raw_agents_required()
        38
        """
        agents: int = ceil(self.erlangs)  # Initial guess for agents
        while self.service_level(agents) < self.tsl:
            agents += 1
        return agents

    def average_speed_of_answer(self) -> float:
        # TODO Add exemples
        # TODO Add tests
        """Calculate the average speed of answer (ASA) in seconds.

        Returns
        -------
        float
            The average time callers wait before being answered, in seconds.
        """
        return (self.p_wait * self.aht) / (self.raw_agents - self.erlangs)

    def percentage_calls_answered_immediately(self) -> float:
        # TODO Add exemples
        # TODO Add tests
        """Calculate the percentage of calls answered immediately without waiting.

        Returns
        -------
        float
            The probability that a call will be answered immediately (no queue).
        """
        return 1 - self.p_wait

    def occupancy(self) -> float:
        # TODO Add exemples
        # TODO Add tests
        """Calculate the agent occupancy rate.

        Returns
        -------
        float
            The fraction of time agents are busy handling calls (value between 0 and 1).
        """
        return self.erlangs / self.raw_agents

    def agents_required(self, shrinkage: float) -> int:
        # TODO Add exemples
        # TODO Add tests
        """Calculate the actual number of agents needed accounting for shrinkage.

        Parameters
        ----------
        shrinkage : float
            The fraction of time agents are unavailable (value between 0 and 1).

        Returns
        -------
        int
            The total number of agents needed including shrinkage factor.
        """
        return ceil(self.raw_agents / (1 - shrinkage))

    def erlang_a(self, average_patience: int) -> float:
        # TODO Add exemples
        # TODO Add tests
        """Calculate the probability of abandonment using Erlang A formula.

        Parameters
        ----------
        average_patience : int
            The average time in seconds that callers will wait before hanging up.

        Returns
        -------
        float
            The probability that a call will be abandoned before being answered.
        """
        return self.p_wait * exp(
            (self.erlangs - self.raw_agents) * (average_patience / self.aht)
        )

    def to_pandas(self) -> DataFrame:
        # TODO Add tests
        """Return the data in a pandas.DataFrame.

        Returns
        -------
        DataFrame
            The data, both given and calculated, in DataFrame format.

        Examples
        --------
        >>> from datetime import datetime
        >>> pred = CallCenterPredictions(
        ...     start_time=datetime(2021, 4, 1, 8),
        ...     end_time=datetime(2021, 4, 1, 9),
        ...     calls=390,
        ...     average_handling_time=300,
        ...     target_service_level=0.8,
        ...     target_answer_time=30,
        ... )
        >>> pred.to_pandas()
                   start_time            end_time  calls  aht  tsl  tat  erlangs  raw_agents    p_wait
        0 2021-04-01 08:00:00 2021-04-01 09:00:00    390  300  0.8   30     32.5          38  0.261203
        """
        return DataFrame([self.__dict__])

    def __str__(self) -> str:
        # TODO Add tests
        """Return the data in a string format.

        Returns
        -------
        str
            The data in string format, similar to pandas.DataFrame style.

        Examples
        --------
        >>> from datetime import datetime
        >>> pred = CallCenterPredictions(
        ...     start_time=datetime(2021, 4, 1, 8),
        ...     end_time=datetime(2021, 4, 1, 9),
        ...     calls=390,
        ...     average_handling_time=300,
        ...     target_service_level=0.8,
        ...     target_answer_time=30,
        ... )
        >>> print(pred)
                   start_time            end_time  calls  aht  tsl  tat  erlangs  raw_agents    p_wait
        0 2021-04-01 08:00:00 2021-04-01 09:00:00    390  300  0.8   30     32.5          38  0.261203
        """
        return str(self.to_pandas())
