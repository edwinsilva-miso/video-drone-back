from decouple import config


class Config:
    RABBITMQ_URL_CONNECTION = config('RABBITMQ_URL_CONNECTION')


class DevelopmentConfig(Config):
    DEBUG = True


configuration = {
    'development': DevelopmentConfig,
    'production': Config
}
