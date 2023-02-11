from crosscutting.core.app.app import HourlyAPI
from flask_limiter import Limiter

from crosscutting.core.config.config import config

app = HourlyAPI(specification_dir="openapi/")
limiter = Limiter(
    app.app,
    # key_func=get_remote_address,
    default_limits=config.DEFAULT_RATE_LIMIT
)
app.run(port=8080)


# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 8080))
#     port = 80
#     bind_address = '0.0.0.0:' + str(port)
#     app.run(host=bind_address)
