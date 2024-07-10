from enum import StrEnum, auto
from typing import Self
from pydantic import BaseModel, Field, model_validator


class LaunchMode(StrEnum):
    AUTO = auto()
    MANUAL = auto()
    DELAY = auto()


class LaunchParams(BaseModel):
    mode: LaunchMode
    delay_time: int = Field(default=0)

    @model_validator(mode="after")
    def delay_time_validator(self) -> Self:
        if self.mode in (LaunchMode.AUTO, LaunchMode.MANUAL):
            self.delay_time = 0

        if self.mode == LaunchMode.DELAY:
            if self.delay_time < 5 or self.delay_time > 240:
                raise ValueError(
                    "the number of minutes for delayed start should be from 5 to 240"
                )

        return self
