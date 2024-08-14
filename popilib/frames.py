from escape_codes import text2escape, escape_code_dict
from functools import reduce


def create_frame(
    text: str,
    padding: int = 1,
    length: int = ...,
    frame_props: str = ""
) -> str:
    # Calculate max line width (without Escape Codes)
    if length is ...:
        max_length = max(
            [len(reduce(lambda x, line: x.replace(line, ''), escape_code_dict.keys(), line))
             for line in text.split('\n')]
        )
    else:
        max_length = length

    # First frame line
    top_border = f"{escape_code_dict[frame_props]}╭{'─' * (max_length + 2 * padding)}╮{escape_code_dict['<reset>']}"

    # Process each line of the text
    lines = []
    for ln in text.split('\n'):
        if "<hr>" not in ln:
            # Calculate empty space before and after the text
            clean_len = len(reduce(lambda x, k: x.replace(k, ''), escape_code_dict.keys(), ln))
            line = (
                f"{escape_code_dict[frame_props]}│{escape_code_dict['<reset>']}{' ' * padding}"
                f"{text2escape(ln)}"
                f"{' ' * (max_length - clean_len + padding)}"
                f"{escape_code_dict[frame_props]}│{escape_code_dict['<reset>']}"
            )
        else:
            # If <hr> contained, create a horizontal line
            line = f"{escape_code_dict[frame_props]}├{'─' * (max_length + 2 * padding)}┤{escape_code_dict['<reset>']}"

        lines.append(line)

    # Last frame line
    bottom_border = f"{escape_code_dict[frame_props]}╰{'─' * (max_length + 2 * padding)}╯{escape_code_dict['<reset>']}"

    # Create the frame
    frame = "\n".join([top_border] + lines + [bottom_border])

    return frame


# The exact same function as above, but in extremely compact form
# Why? Because it is possible
def cf(text: str, padding: int = 1, length: int = ..., frame_props: str = "") -> str:
    m = max([len(reduce(lambda x, k: x.replace(k, ''), escape_code_dict.keys(), k)) for k in text.split('\n')]) if length is ... else length
    return "\n".join([escape_code_dict[frame_props] + "╭" + "─" * (m + 2 * padding) + "╮" + escape_code_dict["<reset>"]] + [f"{escape_code_dict[frame_props] + '│' + escape_code_dict['<reset>'] + ' ' * padding}{text2escape(ln)}{' ' * (m - len(reduce(lambda x, k: x.replace(k, ''), escape_code_dict.keys(), ln)) + padding)}{escape_code_dict[frame_props] + '│' + escape_code_dict['<reset>']}" if "<hr>" not in ln else f"{escape_code_dict[frame_props]}├{'─' * (m + 2 * padding)}┤{escape_code_dict['<reset>']}" for ln in text.split("\n")] + [escape_code_dict[frame_props] + "╰" + "─" * (m + 2 * padding) + "╯" + escape_code_dict['<reset>']])


if __name__ == '__main__':
    test_content = """<b>Hello<reset> <u>World<reset>!
<hr>
<blue_bg><black><i> This is a test. <reset>
Welcome to the world of <bright_blue>Pyt<bright_yellow>hon<reset>!
<hr>
Do you like it?"""
    print(create_frame(test_content, 1, frame_props="<yellow>"))
    print(cf(test_content, 1, frame_props="<yellow>"))
