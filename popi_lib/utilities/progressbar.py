import sys
from typing import Optional

from popi_lib import Base


class ProgressBar(Base):
    """
    A class to display a progress bar in the console.

    :param total: The maximum value of the progress bar.
    :param length: The length of the progress bar.
    :param initial_progress: The initial progress value.
    :param fill: The character used to fill the progress bar.
    :param empty: The character used to represent the empty space in the progress bar.
    :param prefix: Text before the progress bar.
    :param suffix: Text after the progress bar.
    :param start_fill: The character at the start of the filled portion.
    :param end_fill: The character at the end of the filled portion.
    :param start_empty: The character at the start of the empty portion.
    :param end_empty: The character at the end of the empty portion.
    :param show_percent: Whether to display the percentage of progress.
    :param show_count: Whether to display the progress count.
    :param show_count_leading_zero: Whether to display leading zeros in the progress count.
    :param percentage_floating_digits: Number of decimal places in the percentage.
    """

    def __init__(
        self,
        total: int,
        length: int,
        initial_progress: int = 0,
        fill: str = '#',
        empty: str = '-',
        prefix: str = '',
        suffix: str = '',
        start_fill: Optional[str] = None,
        end_fill: Optional[str] = None,
        start_empty: Optional[str] = None,
        end_empty: Optional[str] = None,
        show_percent: bool = True,
        show_count: bool = True,
        show_count_leading_zero: bool = False,
        percentage_floating_digits: int = 2,
    ) -> None:
        self.total = max(1, total)  # Avoid division by zero
        self.length = max(1, length)  # Length should be at least 1
        self.progress = max(0, min(initial_progress, self.total))
        self.fill = fill
        self.empty = empty
        self.prefix = prefix
        self.suffix = suffix
        self.start_fill = start_fill if start_fill is not None else fill
        self.end_fill = end_fill if end_fill is not None else fill
        self.start_empty = start_empty if start_empty is not None else self.start_fill
        self.end_empty = end_empty if end_empty is not None else self.empty
        self.show_percent = show_percent
        self.show_count = show_count
        self.show_count_leading_zero = show_count_leading_zero
        self.percentage_floating_digits = max(0, percentage_floating_digits)

    def __len__(self) -> int:
        return self.total

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"total={self.total}, progress={self.progress}, length={self.length}, "
            f"fill='{self.fill}', empty='{self.empty}', prefix='{self.prefix}', "
            f"suffix='{self.suffix}', start_fill='{self.start_fill}', end_fill='{self.end_fill}', "
            f"start_empty='{self.start_empty}', end_empty='{self.end_empty}', "
            f"show_percent={self.show_percent}, show_count={self.show_count}, "
            f"show_count_leading_zero={self.show_count_leading_zero}, "
            f"percentage_floating_digits={self.percentage_floating_digits})"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, ProgressBar):
            return False
        return (
            self.total == other.total and
            self.progress == other.progress and
            self.length == other.length and
            self.fill == other.fill and
            self.empty == other.empty and
            self.prefix == other.prefix and
            self.start_fill == other.start_fill and
            self.end_fill == other.end_fill and
            self.start_empty == other.start_empty and
            self.end_empty == other.end_empty and
            self.suffix == other.suffix and
            self.show_percent == other.show_percent and
            self.show_count == other.show_count and
            self.show_count_leading_zero == other.show_count_leading_zero and
            self.percentage_floating_digits == other.percentage_floating_digits
        )

    def display(self) -> 'ProgressBar':
        """
        Display the progress bar in the console.
        """
        percent = self.progress / self.total
        fill_length = int(self.length * percent)
        empty_length = self.length - fill_length
        start_bar = self.start_fill if fill_length > 0 else self.start_empty
        middle_fill = self.fill * max(0, fill_length - 1)
        middle_empty = self.empty * max(0, empty_length - 1)
        end_bar = self.end_empty if empty_length > 0 else self.end_fill
        bar = start_bar + middle_fill + middle_empty + end_bar

        percent_display = f"{percent * 100:.{self.percentage_floating_digits}f}%" if self.show_percent else ""
        count_display = f"({self.progress:0{len(str(self.total))}d}/{self.total}) " if self.show_count else ""

        sys.stdout.write(f"\r{self.prefix}{bar}{self.suffix} {count_display}{percent_display}")
        sys.stdout.flush()
        return self

    def add(self, amount: int) -> 'ProgressBar':
        """
        Increase the progress by a specified amount.
        """
        self.set(self.progress + amount)
        return self

    def set(self, amount: int) -> 'ProgressBar':
        """
        Set the progress to a specific value.
        """
        self.progress = max(0, min(amount, self.total))
        return self


class Bar(ProgressBar):
    """
    A standard progress bar using '#' and '-' to display progress.
    """

    def __init__(
        self, total: int, length: int = 20, initial_progress: int = 0,
        prefix: str = "Bar", suffix: str = "", *args, **kwargs
    ) -> None:
        super().__init__(total, length, initial_progress, "#", " ", prefix, suffix, "|", "|", *args, **kwargs)


class FiraCodeProgressBar(ProgressBar):
    """
    A progress bar using Fira Code font characters to display progress.
    """

    def __init__(
        self, total: int, length: int = 20, initial_progress: int = 0,
        prefix: str = "", suffix: str = "", *args, **kwargs
    ) -> None:
        super().__init__(total, length, initial_progress, "", "", prefix, suffix, "", "", "", "", *args, **kwargs)
