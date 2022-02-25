import threading

from service.cmd_prompt import Prompt
from service.helper_thread import HelperThread


# alternate thread for running helper
def run_helper():
    threading.Timer(5, run_helper).start()
    HelperThread(verbose=True).sync_task()


# start helper thread and then cmd prompt for user
if __name__ == '__main__':
    run_helper()
    Prompt().cmdloop()
