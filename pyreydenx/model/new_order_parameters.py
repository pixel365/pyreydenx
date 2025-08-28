import re
from enum import StrEnum, auto
from typing import Self, Optional
from pydantic import BaseModel, model_validator, Field

from .platform import Platform

_youtube_patterns = (
    re.compile(r"https:\/\/www\.youtube\.com\/@([a-zA-Z\d]+)$"),
    re.compile(r"https:\/\/www\.youtube\.com\/channel\/([a-zA-Z_\d]+)$"),
)


class SmoothGain(BaseModel):
    enabled: bool
    minutes: int = Field(gt=0)

class LaunchMode(StrEnum):
    AUTO = auto()
    MANUAL = auto()
    DELAY = auto()


class NewOrderParameters(BaseModel):
    price_id: int = Field(gt=0)
    number_of_views: int = Field(gt=0)
    number_of_viewers: int = Field(gt=0)
    launch_mode: LaunchMode
    delay_time: int = Field(gt=0)
    smooth_gain: SmoothGain
    fixed_allocation: Optional[int] = Field(default=0)
    on_overflow: Optional[bool] = Field(default=False)

    @property
    def platform(self) -> str:
        return ""

    @model_validator(mode="after")
    def validate_delay_time(self) -> Self:
        if self.launch_mode == LaunchMode.DELAY:
            if self.delay_time < 5 or self.delay_time > 240:
                raise ValueError(
                    "the number of minutes for delayed start should be from 5 to 240"
                )
        return self

    @model_validator(mode="after")
    def validate_allocation(self) -> Self:
        if self.fixed_allocation == 0:
            if self.number_of_viewers == 0:
                raise ValueError (
                    "Number of viewers must be greater than 0 if fixed_allocation is 0",
                )

        if self.fixed_allocation > 0:
            if self.fixed_allocation > self.number_of_views:
                raise ValueError (
                    "Number of viewers must be greater or equal than number of viewers",
                )

            if self.no_overflow and self.number_of_viewers == 0:
                raise ValueError (
                    "Number of viewers must be greater than 0 if no_overflow is True",
                )


class TwitchOrder(NewOrderParameters):
    twitch_id: int = Field(gt=0, le=10_000_000_000)

    @property
    def platform(self) -> str:
        return Platform.TWITCH


class YouTubeOrder(NewOrderParameters):
    channel_url: str

    @property
    def platform(self) -> str:
        return Platform.YOUTUBE

    @model_validator(mode="after")
    def validate_channel_url(self) -> Self:
        for pattern in _youtube_patterns:
            if re.search(pattern=pattern, string=self.channel_url):
                return self

        raise ValueError("this is not a YouTube link")

class KickOrder(NewOrderParameters):
    channel_url: str

    @property
    def platform(self) -> str:
        return Platform.KICK

    @model_validator(mode="after")
    def validate_channel_url(self) -> Self:
        if not self.channel_url.startswith("https://kick.com/"):
            raise ValueError("invalid Kick channel url")
