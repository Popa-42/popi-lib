from popilib.bars import Bar, FiraCodeProgressBar
from time import sleep

total = 24
length = 25


def main():
    bar1 = Bar(total, length, percentage_floating_digits=0)
    for i in range(total):
        bar1.display().add(1)
        sleep(0.25)
    bar1.display()
    print()
    bar2 = FiraCodeProgressBar(total, length, percentage_floating_digits=0)
    for i in range(total):
        bar2.display().add(1)
        sleep(0.25)
    bar2.display()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ...
