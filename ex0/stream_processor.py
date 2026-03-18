from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"{result}"


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        # Prove it is a list (Adding a list to a non-list causes an error)
        # data + []
        try:
            data + []
            for i in data:
                i + 0
            return True
        except Exception:
            return False

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError("Invalid data type for NumericProcessor.")

        try:
            count = len(data)
            total = sum(data)
            if count > 0:
                avg = total / count
            else:
                avg = 0.0
            return f"Processed {count} numeric values, sum={total}, avg={avg}"
        except Exception as e:
            return f"Error processing numeric data: {e}"


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        try:
            data + ""
            return True
        except Exception:
            return False

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError("Invalid data type for TextProcessor.")

        try:
            chars = len(data)
            words = len(data.split())
            return f"Processed text: {chars} characters, {words} words"
        except Exception as e:
            return f"Error processing text data: {e}"


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        try:
            data["message"]
            data["level"]
            return True
        except Exception:
            return False

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError("Invalid data type for LogProcessor.")
        try:
            message = data["message"]
            level = data["level"]
            tmp = f"{level} level detected: {message}"
            tmp = self.format_output(tmp)
            return tmp
        except Exception as e:
            return f"Error processing log data: {e}"

    def format_output(self, result: str) -> str:
        base_result = super().format_output(result)

        if "ERROR" in base_result:
            return f"[ALERT] {base_result}"
        elif "INFO" in base_result:
            return f"[INFO] {base_result}"
        return f"[*] {base_result}"


if __name__ == "__main__":
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    print()
    print("Initializing Numeric Processor...")
    num_proc = NumericProcessor()
    num_data = [1, 2, 3, 4, 5]
    print(f"Processing data: {num_data}")
    tmp = num_proc.process(num_data)
    print("Validation: Numeric data verified")
    print(f"Output: {num_proc.format_output(tmp)}")

    print()
    print("Initializing Text Processor...")
    text_proc = TextProcessor()
    text_data = "Hello Nexus World"
    print(f'Processing data: "{text_data}"')
    tmp = text_proc.process(text_data)
    print("Validation: Text data verified")
    print(f"Output: {text_proc.format_output(tmp)}")

    print()
    print("Initializing Log Processor...")
    log_proc = LogProcessor()
    dic = {"message": "Connection timeout", "level": "ERROR"}
    tmp = log_proc.process(dic)
    print(f'Processing data: "{dic["level"]}: {dic["message"]}"')
    print("Validation: Log entry verified")
    print(f"Output: {tmp}")

    print()
    print("=== Polymorphic Processing Demo ===")

    num_data = [1, 2, 3]
    text_data = "Hello world."
    dic = {"message": " System ready", "level": "INFO"}
    data = [num_data, text_data, dic]
    processors = [NumericProcessor(), TextProcessor(), LogProcessor()]
    i = 0
    for item in processors:
        print(f" Result {i + 1}: {item.process(data[i])}")
        i += 1
    print()
    print("Foundation systems online. Nexus ready for advanced streams.")
