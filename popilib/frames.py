from __future__ import annotations
import sys

from .escape_codes import text2escape as t2e, escape_code_dict
from functools import reduce


class Frame:
    reset = t2e("<reset>")

    def __init__(self, lines: list[str] | str, padding: int = 1, width: int = ..., frame_props: str = "") -> None:
        self.lines = lines.split('\n') if isinstance(lines, str) else lines
        self.num_lines = len(self.lines)
        self.padding = padding
        self.width = width if width is not ... else max(
            [len(reduce(lambda x, line: x.replace(line, ''), escape_code_dict.keys(), line))
             for line in self.lines]
        )
        self.frame_props = frame_props

    def __enter__(self) -> Frame:
        for line in self.create_frame():
            sys.stdout.write(f"\033[K{line}\n")
        sys.stdout.flush()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __repr__(self) -> str:
        return "\n".join(self.create_frame())

    def add_ln(self, lines: list[str] | str):
        """
        Add a line to the frame.
        :param lines: The line(s) to add.
        :return: self
        """
        self.lines.extend(lines.split('\n') if isinstance(lines, str) else lines)
        return self

    def add_hr(self):
        """
        Add a horizontal line to the frame.
        :return: self
        """
        self.lines.append("<hr>")
        return self

    def create_frame(self) -> list[str]:
        """
        Create the frame.
        :return: The frame as a list of strings.
        """
        self.update()

        # First frame line
        top_border = f"{t2e(self.frame_props)}╭{'─' * (self.width + 2 * self.padding)}╮{self.reset}"

        # Process each line of the text
        lines = []
        for ln in self.lines:
            if "<hr>" not in ln:
                # Calculate empty space before and after the text
                clean_len = len(reduce(lambda x, k: x.replace(k, ''), escape_code_dict.keys(), ln))
                line = (
                    f"{t2e(self.frame_props)}│{self.reset}{' ' * self.padding}"
                    f"{t2e(ln)}"
                    f"{' ' * (self.width - clean_len + self.padding)}"
                    f"{t2e(self.frame_props)}│{self.reset}"
                )
            else:
                # If <hr> contained, create a horizontal line
                line = f"{t2e(self.frame_props)}├{'─' * (self.width + 2 * self.padding)}┤{self.reset}"

            lines.append(line)

        # Last frame line
        bottom_border = f"{t2e(self.frame_props)}╰{'─' * (self.width + 2 * self.padding)}╯{self.reset}"

        # Create the frame
        frame = [top_border] + lines + [bottom_border]

        return frame

    def edit_line(self, line_num: int, new_line: str) -> Frame:
        """
        Edit a line of the frame.
        :param line_num: The line index to edit.
        :param new_line: The new line.
        :return: self
        """
        self.lines[line_num] = new_line
        return self

    def update_width(self) -> Frame:
        """
        Update the width of the frame.
        :return: self
        """
        self.width = max(
            [len(reduce(lambda x, line: x.replace(line, ''), escape_code_dict.keys(), line))
             for line in self.lines]
        )
        return self

    def update_num_lines(self) -> Frame:
        """
        Update the number of lines in the frame.
        :return: self
        """
        self.num_lines = len(self.lines)
        return self

    def update(self) -> Frame:
        """
        Update the frame.
        :return: self
        """
        self.update_width().update_num_lines()
        return self

    def print(self) -> None:
        """
        Print the frame.
        """
        self.update_width()
        sys.stdout.write(f"\033[{self.num_lines + 2}F")
        sys.stdout.flush()
        for line in self.create_frame():
            sys.stdout.write(f"\033[K{line}\n")
        sys.stdout.flush()
