import re
from typing import Self
from pydantic import BaseModel, model_validator

from .platform import Platform

_youtube_patterns = (
    re.compile(r"https:\/\/www\.youtube\.com\/@([a-zA-Z\d]+)$"),
    re.compile(r"https:\/\/www\.youtube\.com\/channel\/([a-zA-Z_\d]+)$"),
)


class SmoothGain(BaseModel):
    enabled: bool
    minutes: int


class NewOrderParameters(BaseModel):
    price_id: int
    number_of_views: int
    number_of_viewers: int
    launch_mode: str
    delay_time: int
    smooth_gain: SmoothGain

    @property
    def platform(self) -> str:
        return ""

    @model_validator(mode="after")
    def validate_launch_mode(self) -> Self:
        if self.launch_mode not in ("auto", "manual", "delay"):
            raise ValueError("valid launch mode values are 'auto', 'manual' or 'delay'")
        return self

    @model_validator(mode="after")
    def validate_delay_time(self) -> Self:
        if self.launch_mode == "delay":
            if self.delay_time < 5 or self.delay_time > 240:
                raise ValueError(
                    "the number of minutes for delayed start should be from 5 to 240"
                )
        return self


class TwitchOrder(NewOrderParameters):
    twitch_id: int

    @property
    def platform(self) -> str:
        return Platform.TWITCH.value

    @model_validator(mode="after")
    def validate_twitch_id(self) -> Self:
        if self.twitch_id < 1:
            raise ValueError("twitch id must be greater than zero")
        return self


class YouTubeOrder(NewOrderParameters):
    channel_url: str

    @property
    def platform(self) -> str:
        return Platform.YOUTUBE.value

    @model_validator(mode="after")
    def validate_channel_url(self) -> Self:
        for pattern in _youtube_patterns:
            if re.search(pattern=pattern, string=self.channel_url):
                return self

        raise ValueError("this is not a YouTube link")
