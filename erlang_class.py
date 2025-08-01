"""Module that calculates important metrics for a call center planinng."""

from datetime import datetime
from math import ceil, exp, factorial

from pandas import DataFrame

# from typing import overload


class CallCenterPredictions:
    """Classe that contains the predictable variables of a call center in a certain period of time.

    In this class you gonna find those propreties:
        Those ones should be given to the constructor of the class:
        - id: An index of the information.
        - start_time: The starting date and time.
        - end_time: The ending date and time.
        - calls: The number of expected calls in thar period of time.
        - aht: The average handling time in seconds.

        From now on, those propeties are calculated based on the premisses.
        - period: The total time, in seconds, between the `start_time` and `end_time`.
        - cph: The number of calls per hour.
        - erlgangs: Traffic intensity in Erlangs.
    """

    def __init__(
        self,
        id: str,
        start_time: datetime,
        end_time: datetime,
        calls: int,
        average_handling_time: int,
    ) -> object:
        """Predictable variables of a call center in a certain period of time.

        Parameters
        ----------
        id : str
            The index.
        start_time : datetime
            The stating date and time.
        end_time : datetime
            The ending date and time.
        calls : int
            The number of expected calls in thar period of time.
        average_handling_time : int
            The average handling time in seconds.

        Returns
        -------
        CallCenterPredictions
            The predictable variables of a call center in a certain period of time.
        """
        self.id: str = id
        self.start_time: datetime = start_time
        self.end_time: datetime = end_time
        self.calls: int = calls
        self.aht: int = average_handling_time

        self.period: float = self.period_in_seconds()
        self.cph: float = self.calls_per_hour()
        self.erlangs: float = self.traffic_intensity()

        # self.agents: int =

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
        ...     id=1,
        ...     start_time=datetime(2021, 4, 1, 8),
        ...     end_time=datetime(2021, 4, 1, 8, 30),
        ...     calls=100,
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

    def erlang_c(self) -> float:
        # TODO Add exemples
        """
        Calculate the probability that a call will wait in queue (Erlang C formula).

        Returns
        -------
        float
            Probability that a call will wait in queue (Erlang C).
        """
        _num: float = self.erlangs**self.agents / factorial(self.agents)
        _den: float = (1 - self.erlangs / self.agents) * sum(
            self.erlangs**i / factorial(i) for i in range(self.agents)
        )
        return _num / (_den + _num)

    def to_pandas(self) -> DataFrame:
        # TODO Add docstring
        return DataFrame([self.__dict__]).set_index('id')

    def __str__(self) -> str:
        return str(self.to_pandas())


# TODO Remove this and add tests.
# For developer phase only
def main() -> None:
    predictions = CallCenterPredictions(
        id=1,
        start_time=datetime(2021, 4, 1, 8),
        end_time=datetime(2021, 4, 1, 8, 30),
        calls=100,
        average_handling_time=180,
    )
    print(predictions)


if __name__ == '__main__':
    main()
