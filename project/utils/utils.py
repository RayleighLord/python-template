import sys
import os


__all__ = ["check_and_create_directory", "progress_bar"]


def check_and_create_directory(directory):
    """
    Checks if a directory exists. If it doesn't, create the directory.

    Parameters:
        - directory: string with the name of the directory
    """
    if not os.path.isdir(directory):
        os.makedirs(directory)


def progress_bar(index, total, bar_len=30, title="Animation Progress"):
    """
    Displays a progress bar in the terminal

    Parameters:
        - index: current index of the process
        - total: total length of the taskANIMATION_FRAMES =
        anim.get_animation_frames()
        - bar_len: length of the displayed bar
        - title: title for the progress bar
    """

    percent_done = (index + 1) / total * 100
    percent_done = round(percent_done, 1)

    done = round(percent_done / (100 / bar_len))
    togo = bar_len - done

    done_str = "█" * int(done)
    togo_str = "░" * int(togo)

    sys.stdout.write(
        f"\r⏳{title}: [{done_str}{togo_str}] {percent_done}% done"
    )
    sys.stdout.flush()

    if percent_done == 100:
        print("\t✅")
