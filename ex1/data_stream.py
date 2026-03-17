from abc import ABC, abstractmethod 
from typing import Any, List, Optional, Dict, Union


class DataStream(ABC):
    def __init__(self, stream_id: str) ->None:
        self.stream_id = stream_id
        self.total_processed = 0
        self.message = ""
        self.show_info = ""
    
    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]= None) -> List[Any]:
        return data_batch
    
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"processed": self.total_processed}

class SensorStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        
        self.show_info = f"Stream ID: {self.stream_id}, Type: Environmental Data"

    def process_batch(self, data_batch: List[Any]) -> str:
        if not isinstance(data_batch, list):
            return "Error: Invalid batch format."
        count = 0
        total_temp = 0.0
        try:
            temperatures = [
                float(item[5:]) 
                for item in data_batch 
                if isinstance(item, str) and item[:5] == "temp:"
            ]
        except ValueError:
            return "Error: we expect a number in temp and you passed a string"
        total_items = len(data_batch)
        self.total_processed+=total_items
        temp_count = len(temperatures)
            
        if temp_count > 0:
            for item in temperatures:
                total_temp+=item
            avg_temp = total_temp / temp_count
        else:
            avg_temp = 0.0
            
        result = ""
        count = 0
        for i in data_batch:
            tmp = f"{i}"
            if count < len(data_batch) - 1:
                result = result + tmp + ", "
            else:
                result = result + tmp
            count+=1
        self.message = f"Processing sensor batch: [{result}]"
        return f"Sensor analysis: {total_items} readings processed, avg temp: {avg_temp}°C"

    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        if criteria == "High-priority":
            return [
                item
                for item in data_batch
                if isinstance(item, str) and item[:5] == "temp:" and float(item[5:]) > 20.0
            ]
        return []
    
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"readings processed": self.total_processed}
class TransactionStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        
        self.show_info = f"Stream ID: {self.stream_id}, Type: Financial Data"

    def process_batch(self, data_batch: List[Any]) -> str:
        if not isinstance(data_batch, list):
            return "Error: Invalid batch format."
        try:
            buy = [
                int(item[4:]) 
                for item in data_batch 
                if isinstance(item, str) and (item[:4] == "buy:")
            ]
            sell = [
                int(item[5:]) 
                for item in data_batch 
                if isinstance(item, str) and (item[:5] == "sell:")
            ]
        except ValueError:
            return "Error: expected a number in transaction but got a string"
        self.total_processed+=len(data_batch)
        total_buy = 0
        for i in buy:
            total_buy+=i
        total_sell = 0
        for i in sell:
            total_sell+=i
        net = total_buy - total_sell
        result = ""
        count = 0
        for i in data_batch:
            tmp = f"{i}"
            if count < len(data_batch) - 1:
                result = result + tmp + ", "
            else:
                result = result + tmp
            count+=1
        self.message = f"Processing transaction batch: [{result}]"
        return f"Transaction analysis: {len(data_batch)} operations, net flow: {net:+} units"

    
    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        if criteria == "High-priority":
            filtered = []
            for item in data_batch:
                if isinstance(item, str):
                    if item[:4] == "buy:" and int(item[4:]) >= 100:
                        filtered+=[item]
                    elif item[:5] == "sell:" and int(item[5:]) >= 100:
                        filtered+=[item]
            return filtered
        return data_batch
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"operations processed": self.total_processed}
class EventStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        
        self.show_info = f"Stream ID: {self.stream_id}, Type: System Events"

    def process_batch(self, data_batch: List[Any]) -> str:
        if not isinstance(data_batch, list):
            return "Error: Invalid batch format."
        errors = [
            item for item in data_batch 
            if isinstance(item, str) and item == "error" 
        ]
        self.total_processed+=len(data_batch)
        count_err = len(errors)
        result = ""
        count = 0
        for i in data_batch:
            tmp = f"{i}"
            if count < len(data_batch) - 1:
                result = result + tmp + ", "
            else:
                result = result + tmp
            count+=1
        self.message = f"Processing event batch: [{result}]"
        return f"Event analysis: {len(data_batch)} events, {count_err} error detected"
    
    
    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        if criteria == "High-priority":
            return [item for item in data_batch if item == "error"]
        return data_batch
    
    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"events processed": self.total_processed}



class StreamProcessor:
    def __init__(self) -> None:
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        self.streams+=[stream]

    def process_all(self, batches: List[List[Any]], criteria: str = "High-priority") -> None:
        print("=== Polymorphic Stream Processing ===")
        print("Processing mixed stream types through unified interface...\n")
        print("Batch 1 Results:")
        i = 0
        for stream in self.streams:
            stream.process_batch(batches[i])
            stats = stream.get_stats()            
            if isinstance(stream, SensorStream):
                print(f"- Sensor data: {stats['readings processed']} readings processed")
            elif isinstance(stream, TransactionStream):
                print(f"- Transaction data: {stats['operations processed']} operations processed")
            elif isinstance(stream, EventStream):
                print(f"- Event data: {stats['events processed']} events processed")
            i+=1
        
        print()
        print(f"Stream filtering active: {criteria} data only")
        string = "Filtered results: "
        i = 0
        for item in self.streams:
            if isinstance(item, SensorStream):
                string+=f"{len(item.filter_data(batches[i], criteria))} critical sensor alerts, "
            if isinstance(item, TransactionStream):
                string+=f"{len(item.filter_data(batches[i], criteria))} large transaction"
            i+=1
        print(string)
if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    print()
    
    print("Initializing Sensor Stream...")
    e = SensorStream("SENSOR_001")
    print(e.show_info)
    x = e.process_batch(["temp:22.5", "humidity:65", "pressure:1013"])
    print(e.message)
    print(x)
    print()
    
    print("Initializing Transaction Stream...")
    f = TransactionStream("TRANS_001")
    print(f.show_info)
    x = f.process_batch(["buy:100", "sell:150", "buy:75"])
    print(f.message)
    print(x)
    print()
    
    print("Initializing Event Stream...")
    g = EventStream("EVENT_001")
    print(g.show_info)
    x = g.process_batch(["login", "error", "logout"])
    print(g.message)
    print(x)
    print()
    
    poly_sensor = SensorStream("SENSOR_POLY")
    poly_finance = TransactionStream("TRANS_POLY")
    poly_event = EventStream("EVENT_POLY")
    
    poly_sensor_data = ['temp:30.0', 'temp:26.5']
    poly_finance_data = ['buy:10', 'sell:5', 'buy:120', 'sell:2']
    poly_event_data = ['error', 'login', 'error']

    batches = [poly_sensor_data, poly_finance_data, poly_event_data]
    
    processor = StreamProcessor()
    processor.add_stream(poly_sensor)
    processor.add_stream(poly_finance)
    processor.add_stream(poly_event)
    
    processor.process_all(batches, criteria="High-priority")
    print()
    print("All streams processed successfully. Nexus throughput optimal.")