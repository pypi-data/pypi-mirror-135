from typing import Any, Union


class MemoryModel:
    def __init__(self):
        pass

    def predicted_recall(self, lag_time: Union[float, int]) -> float:
        """The current probability of recall."""
        raise NotImplementedError

    def update_recall(self, result: Any) -> None:
        """Update the recall probability given a result."""
        raise NotImplementedError
