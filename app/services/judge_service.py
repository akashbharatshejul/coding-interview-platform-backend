import io
import sys

def run_code(code: str):

    try:
        output_buffer = io.StringIO()
        sys.stdout = output_buffer

        exec(code)

        sys.stdout = sys.__stdout__

        return output_buffer.getvalue().strip()

    except Exception as e:
        sys.stdout = sys.__stdout__
        return str(e)