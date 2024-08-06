import sys


class ProgressBar:
    """
    A progress bar that can be used to display the progress of a task.

    :param total: The maximum value of the progress bar.
    :param length: The length of the progress bar.
    :param initial_progress: The progress value on initialisation.
    :param fill: The character used to fill the progress bar.
    :param empty: The character used to fill the empty space of the progress bar.
    :param prefix: Some text before the progress bar.
    :param suffix: Some text after the progress bar.
    :param start_fill: The filled character used at the beginning of the progress bar.
    :param end_fill: The very last character used for the filled progress bar.
    :param start_empty: The very first character used for the empty progress bar.
    :param end_empty: The empty character used at the end of the progress bar.
    :param show_percent: Whether to show the percentage of the progress.
    :param show_count: Whether to show the count of the progress.
    :param show_count_leading_zero: Whether to show the leading zero of the count of the progress.
    :param percentage_floating_digits: The number of floating digits to show in the percentage.
    """
    def __init__(self, total: int, length: int = 20, initial_progress: int = 0, fill: str = "█", empty: str = " ",
                 prefix: str = "", suffix: str = "", start_fill: str | None = None, end_fill: str | None = None,
                 start_empty: str | None = None, end_empty: str | None = None, show_percent: bool = True,
                 show_count: bool = True, show_count_leading_zero: bool = False,
                 percentage_floating_digits: int = 2) -> None:
        self.total = total
        self.length = length
        self.progress = initial_progress
        self.fill = fill
        self.empty = empty
        self.prefix = prefix
        self.start_fill = start_fill if start_fill is not None else self.fill
        self.start_empty = start_empty if start_empty is not None else self.start_fill
        self.suffix = suffix
        self.end_fill = end_fill if end_fill is not None else self.fill
        self.end_empty = end_empty if end_empty is not None else end_fill if end_fill is not None else self.empty
        self.show_percent = show_percent
        self.show_count = show_count
        self.show_count_leading_zero = show_count_leading_zero
        self.percentage_floating_digits = percentage_floating_digits if percentage_floating_digits >= 0 else 2

    def __len__(self) -> int:
        return self.total

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(\n  total={self.total},\n  progress={self.progress},\n"
                f"  length={self.length},  \n  fill=\"{self.fill}\",\n  empty=\"{self.empty}\",\n"
                f"  prefix=\"{self.prefix}\",\n  start_fill=\"{self.start_fill}\",\n  end_fill=\"{self.end_fill}\",\n"
                f"  start_empty=\"{self.start_empty}\",\n  end_empty=\"{self.end_empty}\",\n"
                f"  suffix=\"{self.suffix}\",\n  show_percent={self.show_percent},\n  show_count={self.show_count},\n"
                f"  show_count_leading_zero={self.show_count_leading_zero},\n"
                f"  percentage_floating_digits={self.percentage_floating_digits}\n)")

    def __eq__(self, other):
        if not isinstance(other, ProgressBar):
            return False
        return self.total == other.total and self.progress == other.progress and self.length == other.length and \
            self.fill == other.fill and self.empty == other.empty and self.prefix == other.prefix and \
            self.start_fill == other.start_fill and self.start_empty == other.start_empty and \
            self.end_fill == other.end_fill and self.end_empty == other.end_empty and self.suffix == other.suffix and \
            self.show_percent == other.show_percent and self.show_count == other.show_count and \
            self.show_count_leading_zero == other.show_count_leading_zero and \
            self.percentage_floating_digits == other.percentage_floating_digits

    def display(self):
        """
        Display the progress bar in the console.
        :return: The progress bar itself.
        """
        percent = self.progress / self.total
        fill_length = int(self.length * percent)
        empty_length = self.length - fill_length
        start_bar = self.start_fill if fill_length > 0 else self.start_empty
        middle_fill = "" if fill_length == 0 else \
            self.fill * (fill_length - 1) if fill_length < self.length else \
            self.fill * (fill_length - 2)
        middle_empty = "" if empty_length == 0 else \
            self.empty * (empty_length - 1) if empty_length < self.length else \
            self.empty * (empty_length - 2)
        end_bar = self.end_empty if empty_length > 0 else self.end_fill
        bar = start_bar + middle_fill + middle_empty + end_bar
        percent = f"{percent * 100:.{self.percentage_floating_digits}f} %" if self.show_percent else ""
        count = (f"({self.progress:{0 if self.show_count_leading_zero else ""}{len(str(self.total))}d}/"
                 f"{self.total:{0 if self.show_count_leading_zero else ""}{len(str(self.total))}d}"
                 ")  ") if self.show_count else ""
        sys.stdout.write(f"\r{self.prefix}{bar}{self.suffix}  {count}{percent}")
        sys.stdout.flush()
        return self

    def add(self, amount: int):
        """
        Add to the progress.
        :param amount: The amount to add.
        :return: The progress bar itself.
        """
        self.progress += amount
        if self.progress > self.total:
            self.progress = self.total
        if self.progress < 0:
            self.progress = 0
        return self

    def set(self, amount: int):
        """
        Set the progress to a specific value.
        :param amount: The value to set the progress to.
        :return: The progress bar itself.
        """
        self.progress = amount
        if self.progress > self.total:
            self.progress = self.total
        if self.progress < 0:
            self.progress = 0
        return self


class StandardProgressBar(ProgressBar):
    """
    A standard progress bar that uses the characters "#" and "-" to display the progress bar.

    :param total: The maximum value of the progress bar.
    :param length: The length of the progress bar.
    :param initial_progress: The progress value on initialisation.
    :param prefix: The prefix of the progress bar.
    :param suffix: The suffix of the progress bar.
    """
    def __init__(self, total: int, length: int = 20, initial_progress: int = 0, prefix: str = "", suffix: str = "",
                 *args,
                 **kwargs) -> None:
        super().__init__(total, length, initial_progress, "#", "-", prefix, suffix, "[", "]", *args, **kwargs)


class FiraCodeProgressBar(ProgressBar):
    """
    A progress bar that uses custom characters features from the Fira Code font to display the progress bar.

    :param total: The maximum value of the progress bar.
    :param length: The length of the progress bar.
    :param initial_progress: The progress value on initialisation.
    :param prefix: The prefix of the progress bar.
    :param suffix: The suffix of the progress bar.
    """

    def __init__(self, total: int, length: int = 20, initial_progress: int = 0, prefix: str = "", suffix: str = "",
                 *args,
                 **kwargs) -> None:
        super().__init__(total, length, initial_progress, "", "", prefix, suffix, "", "", "", "", *args, **kwargs)
