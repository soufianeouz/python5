from abc import ABC, abstractmethod 
from typing import Any, List, Optional, Dict, Union


class DataStream(ABC):
    def __init__(self, stream_id: str):
        self.stream_id = stream_id
    
    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]= None) -> List[Any]:
        pass
    
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass

class SensorStream(DataStream):
    def process_batch(self, data_batch: List[Any]) -> str:
        result = ""
        count = 0
        for i in data_batch:
            tmp = f"{i}"
            if count < len(data_batch) - 1:
                result = result + tmp + ", "
            else:
                result = result + tmp
            count+=1
        return f"Processing sensor batch: [{result}]"

class TransactionStream(DataStream):
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

class EventStream(DataStream):
    def process_batch(self, data_batch: List[Any]) -> str:
        pass


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    print()
    e = SensorStream(" SENSOR_001")
    x = e.process_batch(["temp:22.5", "humidity:65", "pressure:1013"])
    # x = e.process_batch([1,2,3])
    print(x)
    