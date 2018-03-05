import os
import logging
from minitracker import app

try:
    import uvloop
except ImportError:
    pass
else:
    import asyncio

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

DEBUG = os.environ.get('DEBUG', False)
PORT = os.environ.get('PORT', 8765)

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.DEBUG if DEBUG else logging.INFO)
    logging.debug(f'env DEBUG={DEBUG}, PORT={PORT}')
    app.main(PORT, DEBUG)
