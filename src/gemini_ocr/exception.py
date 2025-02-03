import traceback
from src.logger import AppLogger  # Assumes AppLogger is defined in logger.py
import sys


class OcrException(Exception):
    """
    Custom exception class for the OCR project with integrated logging.
    """

    def __init__(self, message: str, original_exception: Exception = None):
        """
        :param message: Custom error message for the exception.
        :param original_exception: The original exception object, if any.
        """
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)

        # Log the exception when it is instantiated
        self.log_error()

    def __str__(self):
        if self.original_exception:
            return f"{self.message} | Original Exception: {str(self.original_exception)}"
        return self.message

    def log_error(self):
        """
        Logs the error message and stack trace for debugging.
        """
        error_details = {
            "message": self.message,
            "original_exception": str(self.original_exception) if self.original_exception else "None",
            "stack_trace": traceback.format_exc()
        }
        # Log error details with file, line, and error type
        AppLogger.log_exception(
            (
                type(self.original_exception) if self.original_exception else type(self),
                self,
                sys.exc_info()[2],
            )
        )


if __name__ == "__main__":
    try:
        # Example of raising and catching a custom exception
        try:
            1 / 0  # Trigger a ZeroDivisionError
        except ZeroDivisionError as ze:
            raise OcrException("An error occurred in the OCR process.", ze)
    except OcrException as e:
        print(f"Caught an exception: {e}")
