from typing import Any, Union

from spacedreppy.memory_models.memory_model import MemoryModel


class SM2MemoryModel(MemoryModel):
    """Assumes that

    See SM2Scheduler for more information on the SM-2 algorithm.
    """

    def predicted_recall(self, lag_time: Union[float, int]) -> float:
        pass

    def update_recall(self, result: Any) -> None:
        pass
