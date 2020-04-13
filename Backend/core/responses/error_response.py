from typing import Dict


class ErrorResponse():
    def __init__(self, details: Dict, error: str):
        self.details = details
        self.error = error
