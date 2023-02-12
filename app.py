import os

from crosscutting.core.app.app import HourlyAPI
from flask_limiter import Limiter
from crosscutting.core.config.config import config

app = HourlyAPI(specification_dir="openapi/")
limiter = Limiter(
    app.app,
    default_limits=config.DEFAULT_RATE_LIMIT
)

if __name__ == '__main__' and os.environ.get("APP_ENV") == "prod":
    bind_address = '0.0.0.0:' + str(config.PORT)
    app.run(host=bind_address)
else:
    app.run(port=8080)