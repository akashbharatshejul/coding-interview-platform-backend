import io
import sys

def run_code(code: str, test_input: str):

    try:
        # capture input
        sys.stdin = io.StringIO(test_input)

        # capture output
        output_buffer = io.StringIO()
        sys.stdout = output_buffer

        exec(code)

        # reset
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

        return output_buffer.getvalue().strip()

    except Exception as e:
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
        return str(e)