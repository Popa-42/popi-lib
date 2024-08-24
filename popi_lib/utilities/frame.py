from __future__ import annotations
import sys
from functools import reduce

from ..core import Base
from ..escape_codes import text2escape as t2e, escape_code_dict, terminal_supports_colors as tsc


class Frame(Base):
    reset_code = t2e("<reset>")

    def __init__(self, content: list[str] | str, padding: int = 1, width: int = None, frame_style: str = "") -> None:
        """
        Initialize the Frame object.

        :param content: List of strings or a single string to be framed.
        :param padding: Padding around the text within the frame.
        :param width: Width of the frame. If None, it will be auto-calculated.
        :param frame_style: Escape code for frame styling.
        """
        self.lines = content.split('\n') if isinstance(content, str) else content
        self.padding = padding
        self.width = self._calculate_width() if width is None else width
        self.frame_style = frame_style
        self.num_lines = len(self.lines)

        self.add_ln = self.add_line
        self.add_hr = self.add_horizontal_rule
        self.edit_ln = self.edit_line

    def __enter__(self) -> Frame:
        """Enter the runtime context for using 'with' statement."""
        self._display_frame()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the runtime context. No action needed."""
        pass

    def __repr__(self) -> str:
        """Return a string representation of the frame."""
        return "\n".join(self._build_frame())

    def add_line(self, content: list[str] | str) -> Frame:
        """
        Add lines to the frame.

        :param content: Line(s) to add to the frame.
        :return: The updated Frame object.
        """
        self.lines.extend(content.split('\n') if isinstance(content, str) else content)
        return self._update_frame()

    def add_horizontal_rule(self) -> Frame:
        """
        Add a horizontal rule (divider) to the frame.

        :return: The updated Frame object.
        """
        self.lines.append("<hr>")
        return self

    def edit_line(self, line_index: int, new_content: str) -> Frame:
        """
        Edit a specific line in the frame.

        :param line_index: Index of the line to edit.
        :param new_content: New content for the line.
        :return: The updated Frame object.
        """
        self.lines[line_index] = new_content
        return self._update_frame()

    def print_frame(self) -> None:
        """Print the frame to the console."""
        self.width = self._calculate_width()
        sys.stdout.write(f"\033[{self.num_lines + 2}F")
        sys.stdout.flush()
        self._display_frame()
        self.num_lines = len(self.lines)

    def _display_frame(self) -> None:
        """Write the frame to the console output."""
        if not tsc():
            self.logger.critical("Terminal does not fully support ANSI escape codes. Frame cannot be displayed.")
            return
        for line in self._build_frame():
            sys.stdout.write(f"\033[K{line}\n")
        sys.stdout.flush()

    def _build_frame(self) -> list[str]:
        """
        Construct the frame with borders and content.

        :return: List of strings representing the frame.
        """
        top_border = f"{t2e(self.frame_style)}╭{'─' * (self.width + 2 * self.padding)}╮{self.reset_code}"
        bottom_border = f"{t2e(self.frame_style)}╰{'─' * (self.width + 2 * self.padding)}╯{self.reset_code}"

        frame_lines = [top_border]
        for line in self.lines:
            if line == "<hr>":
                frame_lines.append(f"{t2e(self.frame_style)}├{'─' * (self.width + 2 * self.padding)}┤{self.reset_code}")
            else:
                clean_length = len(reduce(lambda s, esc: s.replace(esc, ''), escape_code_dict.keys(), line))
                padded_line = (
                    f"{self.reset_code}{t2e(self.frame_style)}│{self.reset_code}{' ' * self.padding}"
                    f"{t2e(line)}{' ' * (self.width - clean_length + self.padding)}"
                    f"{self.reset_code}{t2e(self.frame_style)}│{self.reset_code}"
                )
                frame_lines.append(padded_line)

        frame_lines.append(bottom_border)
        return frame_lines

    def _calculate_width(self) -> int:
        """Calculate the width of the frame based on content."""
        return max(
            len(reduce(lambda s, esc: s.replace(esc, ''), escape_code_dict.keys(), line))
            for line in self.lines
        )

    def _update_frame(self) -> Frame:
        """Update the frame's dimensions and line count."""
        self.width = self._calculate_width()
        return self
