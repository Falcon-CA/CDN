import math
import time

from cdn_global import cdn
from fca_cdn.util import log


def run_clock():
    c = cdn.db.cursor()

    while True:
        start_time = time.time()

        c.execute("UPDATE tokens SET exp_sec = exp_sec - 300 WHERE exp_sec IS NOT NULL")

        c.execute("SELECT token FROM tokens WHERE exp_sec <= 0")
        c_timers = c.fetchall()
        for timer in c_timers:
            cdn.token_index.remove(timer[0])

        c.execute("DELETE FROM tokens WHERE exp_sec <= 0")
        cdn.db.commit()

        wait_time = 300 - (time.time() - start_time)
        if wait_time > 0:
            time.sleep(300)
        else:
            log(f"Clock is {wait_time * -1} seconds behind", level="warning")