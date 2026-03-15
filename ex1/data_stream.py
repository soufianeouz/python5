from abc import ABC, abstractmethod 
from typing import Any, List, Optional, Dict, Union


class DataStream(ABC):
    def __init__(self, stream_id: str):
        self.stream_id = stream_id
    
    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    @abstractmethod
    def filter_data(self, data_batch: List[Any], criteria: Optional[str]= None) -> List[Any]:
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass

class SensorStream(DataStream):
    pass

class TransactionStream(DataStream):
    pass

class EventStream(DataStream):
    pass