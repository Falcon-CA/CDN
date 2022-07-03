import sys
import threading

from cdn_global import cdn
from fca_cdn import clock
from fca_cdn import init
import fca_cdn.routes

init.load_environ()
cdn.db = init.get_connection()
init.create_tables(cdn.db)
if "--tables" in sys.argv:
    init.create_tables(cdn.db)
init.load_indexes(cdn.db)

clock_t = threading.Thread(target=clock.run_clock)
clock_t.start()

if "--debug" in sys.argv:
    cdn.run()