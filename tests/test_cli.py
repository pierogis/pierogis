import os
import subprocess


def test_cli_1():
    subprocess.call("pyrogis sort demo/gnome.jpg".split())

    assert os.path.isfile("cooked.png")

    os.remove("cooked.png")


def test_cli_2():
    subprocess.run("pyrogis threshold demo/output.mp4".split())

    assert len(os.listdir("cooked")) > 1


def test_cli_3():
    subprocess.run("pyrogis plate cooked".split())

    assert os.path.isfile("cooked.gif")

    os.remove("cooked.gif")
