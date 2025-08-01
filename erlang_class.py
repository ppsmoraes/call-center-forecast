"""Module that calculates important metrics for a call center planinng."""

from datetime import datetime
from math import ceil, exp, factorial

from pandas import DataFrame


class CallCenterPredictions:
    """Classe that contains the predictable variables of a call center in a certain period of time."""

    def __init__(
        self,
        start_time: datetime,
        end_time: datetime,
        calls: int,
        average_handling_time: int,
        target_service_level: float,
        target_answer_time: int,
    ) -> object:
        """Predictable variables of a call center in a certain period of time.

        Parameters
        ----------
        start_time : datetime
            The stating date and time.
        end_time : datetime
            The ending date and time.
        calls : int
            The number of expected calls in thar period of time.
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
                f'The target service level should be a number between 0 and 1 (both ends included). But {self.tsl} were given.'
            )

        self.period: float = self.period_in_seconds()
        self.cph: float = self.calls_per_hour()
        self.erlangs: float = self.traffic_intensity()
        self.raw_agents: int = self.raw_agents_required()

    def period_in_seconds(self) -> float:
        """Calculate the period of time in seconds.

        Returns
        -------
        float
            Period of time in seconds.

        Exemples
        --------
        >>> from erlang_class import CallCenterPredictions
        >>> from datetime import datetime
        >>> predictions = CallCenterPredictions(
        ...     start_time=datetime(2021, 4, 1, 8),
        ...     end_time=datetime(2021, 4, 1, 8, 30),
        ...     calls=100,
        ...     average_handling_time=180,
        ...     target_service_level=0.8,
        ...     target_answer_time=20
        ... )
        >>> predictions.period_in_seconds()
        1800.0
        """
        return (self.end_time - self.start_time).total_seconds()

    def calls_per_hour(self) -> float:
        # TODO Add exemples
        """Calculate the number of calls per hour.

        Returns
        -------
        float
            Calls per hour.
        """
        return self.calls * (3600 / self.period)

    def traffic_intensity(self) -> float:
        # TODO Add exemples
        """Calculate traffic intensity (in Erlangs).

        Returns
        -------
        float
            Traffic intensity in Erlangs.
        """
        return self.cph * (self.aht / 3600)

    def erlang_c(self, agents: int) -> float:
        # TODO Add exemples
        """Calculate the probability that a call will wait in queue (Erlang C formula).

        Parameters
        ----------
        agents : int
            The quantity of agents to answer those calls.

        Returns
        -------
        float
            Probability that a call will wait in queue (Erlang C).
        """
        _num: float = self.erlangs**agents / factorial(agents)
        _den: float = sum(self.erlangs**_ / factorial(_) for _ in range(agents)) * (
            1 - self.erlangs / agents
        )
        return _num / (_den + _num)

    def service_level(self, agents: int) -> float:
        # TODO Add exemples
        """Calculate the estimated service level.

        Parameters
        ----------
        agents : int
            The quantity of agents to answer those calls.

        Returns
        -------
        float
            Estimated service level (probability that a call is answered within the target time).
        """
        return 1 - (
            self.erlang_c(agents) * exp((self.erlangs - agents) * (self.tat / self.aht))
        )

    def raw_agents_required(self) -> int:
        # TODO Create docstring
        agents: int = ceil(self.erlangs)  # Initial guess for agents
        while self.service_level(agents) < self.tsl:
            agents += 1
        return agents

    def to_pandas(self) -> DataFrame:
        # TODO Add docstring
        return DataFrame([self.__dict__])

    def __str__(self) -> str:
        # TODO Add docstring
        return str(self.to_pandas())


# TODO Remove this and add tests.
# For developer phase only
def main() -> None:
    predictions = CallCenterPredictions(
        start_time=datetime(2021, 4, 1, 8),
        end_time=datetime(2021, 4, 1, 8, 30),
        calls=100,
        average_handling_time=180,
        target_service_level=0.8,
        target_answer_time=20,
    )
    print(predictions)


if __name__ == '__main__':
    main()
