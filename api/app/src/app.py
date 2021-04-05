import os
from time import sleep
from flask import Flask

from .utils.Logger import Logger
from .utils.Database import Database
from .utils.ApiResponse import ApiResponse

from .config import config_by_name


FLASK_LEVEL = os.environ.get("FLASK_LEVEL", "dev")

logger = Logger()
database = Database()

def page_not_found(e):
    apiResponse = ApiResponse()
    apiResponse.setMessage("Page not found")
    apiResponse.setHTTPCode(404)
    return apiResponse.getResponse()

def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    app.config.from_object(config_by_name[FLASK_LEVEL])
    os.environ["FLASK_ENV"] = config_by_name[FLASK_LEVEL].FLASK_ENV

    # Waiting for database to be available
    while database.isDatabaseAvailable(app) is False:
        logger.warning("Database unreachable. Waiting for 3 seconds to be up...")
        sleep(3.0)
    logger.info("Database is up and running ✓")
    database.initDatabase(app)
    return app