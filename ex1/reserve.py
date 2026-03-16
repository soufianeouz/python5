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