from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.models.settings import SystemConfig
from app.core import config


def get_system_config(db: Optional[Session] = None) -> SystemConfig:
    def _fetch_or_create(session: Session) -> SystemConfig:
        sys_config = session.query(SystemConfig).filter(SystemConfig.id == 1).first()
        if not sys_config:
            sys_config = SystemConfig(
                id=1,
                rate_limit_enabled=config.RATE_LIMIT_ENABLED,
                login_rate_limit=config.DEFAULT_LOGIN_LIMIT,
                submit_rate_limit=config.DEFAULT_SUBMIT_LIMIT,
            )
            session.add(sys_config)
            session.commit()
            session.refresh(sys_config)
        return sys_config

    if db is not None:
        return _fetch_or_create(db)

    with SessionLocal() as session:
        return _fetch_or_create(session)


def is_rate_limit_enabled() -> bool:
    return get_system_config().rate_limit_enabled

def is_rate_limit_disabled() -> bool:
    return not get_system_config().rate_limit_enabled


def dynamic_login_limit() -> str:
    return get_system_config().login_rate_limit


def dynamic_submit_limit() -> str:
    return get_system_config().submit_rate_limit


limiter = Limiter(
    key_func=get_remote_address,
    enabled=config.RATE_LIMIT_ENABLED,
)
