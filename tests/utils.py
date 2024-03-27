from textwrap import dedent


def diff_output(output1: str, output2: str) -> str:
    if output1 != output2:
        print("Output:")
        print(output1)
        print("Expected output:")
        print(output2)

        print("Output:")
        print(repr(output1))
        print("Expected output:")
        print(repr(output2))

    assert output1 == output2


def adjust_output(expected_output: str) -> str:
    return dedent("\n".join(expected_output.split("\n")[1:]))
