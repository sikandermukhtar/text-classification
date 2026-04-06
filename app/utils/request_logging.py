from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

def logging_request_time(request_url: str, response_time: float, time:str, status: int):
    with open(f'{BASE_DIR}/request_logs.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f"Request url : {request_url} | Status -> {status} | duration : {response_time:.4f}ms | time: {time}\n")