from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class SystemConfig(Base):
    __tablename__ = "system_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    rate_limit_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    login_rate_limit: Mapped[str] = mapped_column(String(50), default="5/minute", nullable=False)
    submit_rate_limit: Mapped[str] = mapped_column(String(50), default="10/minute", nullable=False)

