from pydantic_settings import BaseSettings


class AttendanceRules(BaseSettings):
    ENABLE_DAILY_LIMIT: bool = True
    ENABLE_WEEKLY_LIMIT: bool = True
    ENABLE_MIN_REST: bool = True
    ENABLE_OVERLAP_CHECK: bool = True

    MAX_HOURS_PER_DAY: int = 12
    MAX_HOURS_PER_WEEK: int = 48
    MIN_REST_HOURS: int = 11

    class Config:
        env_prefix = "ATT_"
