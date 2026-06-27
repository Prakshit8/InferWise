import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


LOG_FILE = "experiments/experiments.json"


def log_request(data: Dict[str, Any], log_file: Optional[str] = None) -> None:
    """Log request data to a JSON file.
    
    Args:
        data: Dictionary containing request/response data
        log_file: Optional custom log file path
    """
    log_path = log_file or LOG_FILE
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            try:
                logs = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                logs = []
    else:
        logs = []

    logs.append(data)

    with open(log_path, "w") as f:
        json.dump(logs, f, indent=4)
        