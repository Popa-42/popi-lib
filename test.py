from popi_lib.bars import Bar, FiraCodeProgressBar
from popi_lib.frames import Frame
from time import sleep

total = 24
length = 25


def main():
    # bar_test()
    frame_test()


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
<blue_bg><black><i> This is a test. <reset>
Welcome to the world of <bright_blue>Pyt<bright_yellow>hon<reset>!"""
    frame = Frame(test_content, 2, frame_props="<bright_cyan>")
    with frame as f:
        f.print()
        sleep(1)
        f.add_hr().add_ln("This is a new line").print()
        sleep(1)
        f.add_ln("This is another new line – a <i>looong<reset> line.").print()
        sleep(1)
        f.add_hr().add_ln("Btw - I am aware that this frame is ugly\naf.").print()
        sleep(1)
        f.add_ln("But it's just a test.").print()
        f.add_hr()
        f.add_ln("Bye!")
        sleep(1)
        f.print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ...
