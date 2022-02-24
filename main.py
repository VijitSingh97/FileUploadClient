import threading

from service.cmd_prompt import Prompt
from service.helper_thread import HelperThread


def run_helper():
    threading.Timer(5, run_helper).start()
    HelperThread(verbose=False).sync_task()


if __name__ == '__main__':
    run_helper()
    Prompt().cmdloop()
