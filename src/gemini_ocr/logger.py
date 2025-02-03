import logging
import sys
sys.path.append("..")
from config.configs import ROOT_DIR

# Path to the log file
LOG_DIR = ROOT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "gemini_ocr.log"


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class AppLogger:
    """
    App-wide logger providing standardized logging.
    """
    @staticmethod
    def log_exception(exception):
        """
        Logs an exception with details of file name, line number, and error message.
        """
        # Get exception details
        exc_type, exc_value, exc_traceback = exception
        error_details = {
            "type": exc_type.__name__,
            "message": str(exc_value),
            "file": exc_traceback.tb_frame.f_code.co_filename,
            "line": exc_traceback.tb_lineno,
        }

        # Log the error details
        logging.error(
            "Exception occurred in file: '%(file)s' at line: %(line)d - [%(type)s]: %(message)s",
            error_details
        )

# Example usage in a project
if __name__ == "__main__":
    try:
        # Intentionally raise an exception
        1 / 0
    except Exception:
        AppLogger.log_exception(sys.exc_info())
        print("An error occurred. Check the log file for details.")
