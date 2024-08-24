from time import sleep

from popi_lib.utilities.progressbar import Bar, FiraCodeProgressBar
from popi_lib.utilities.frame import Frame


total = 24
length = 25


def main():
    # bar_test()
    # frame_test()
    print(Frame.get_all())
    print(Frame.get("Frame"))


def bar_test():
    bar1 = Bar(total, length, percentage_floating_digits=0)
    for i in range(total):
        bar1.display().add(1)
        sleep(0.1)
    bar1.display()
    print()
    bar2 = FiraCodeProgressBar(total, length, percentage_floating_digits=0)
    for i in range(total):
        bar2.display().add(1)
        sleep(0.1)
    bar2.display()
    print()


def frame_test():
    test_content = """<b><bright_white>Hello<reset> <u>World<reset>!
<hr>
<cyan_bg><black><i> This is a test. <reset>
Welcome to the world of <bright_blue>Pyt<bright_yellow>hon<reset>!"""
    frame = Frame(test_content, 2, frame_style="<bright_cyan>")
    with frame as f:
        sleep(1)
        f.add_horizontal_rule().add_line("This is a new line").print_frame()
        sleep(1)
        txt = "This is another new line - "
        f.add_line(txt).print_frame()
        sleep(0.5)
        for c in ["a ", "<i>", "l", "o", "o", "o", "n", "g", "<reset> ", "l", "i", "n", "e"]:
            txt += c
            f.edit_line(6, txt).print_frame()
            sleep(0.1)
        sleep(0.5)
        f.add_hr().add_ln("Btw - I am aware that this frame is ugly\nas f*ck.").print_frame()
        sleep(1)
        f.add_line("But it's just a test.").print_frame()
        f.add_horizontal_rule()
        f.add_line("Bye!")
        sleep(1)
        f.print_frame()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ...
