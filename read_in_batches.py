import json


def read_json_file_in_batches(filename, batch_size=1000):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        num_records = len(data)
        num_batches = (num_records + batch_size - 1) // batch_size

        for batch_idx in range(num_batches):
            start_idx = batch_idx * batch_size
            end_idx = min((batch_idx + 1) * batch_size, num_records)
            yield data[start_idx:end_idx]
