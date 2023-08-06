from pydantic import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = 'dev'
    AWS_REGION: str = 'ap-southeast-1'
    VIALINK_TASK_BUCKET_NAME_PREFIX: str = 'vialink-background-task'
    VIALINK_TASK_TABLE_NAME_PREFIX: str = 'vialink-background-task'


settings = Settings()
