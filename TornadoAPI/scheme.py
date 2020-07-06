import tornado_swirl as swirl
import config as config

# Swagger 기본 설정
swirl.describe(
    api_version='v0.1',
    title=config.app_desc,
    description=config.app_desc,
    enabled_methods=['get', 'post', 'put', 'delete'],
    servers=[
        {"url": "http://{}:{}/".format(config.app_host, config.app_port)},
        {"url": "http://127.0.0.1:{}/".format(config.app_port)},
    ],
)

# Swagger 그룹 설정
swirl.add_global_tag(
    name="Account",
    description="계정 관련 API",
    url="http://{}:{}/v1/auth".format(config.app_host, config.app_port)
)

import handlers.root