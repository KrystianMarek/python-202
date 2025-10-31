"""
Adapter Pattern - Convert interface of a class into another interface.

Makes incompatible interfaces work together using Protocol-based duck typing.
"""

from __future__ import annotations

from typing import Protocol


# Target interface (what client expects)
class MediaPlayer(Protocol):
    """Protocol for media players."""

    def play(self, filename: str) -> str:
        """Play media file."""
        ...


# Adaptee (existing incompatible class)
class LegacyAudioPlayer:
    """Legacy audio player with different interface."""

    def play_audio_file(self, file_path: str) -> str:
        """Play audio using legacy method."""
        return f"Playing audio: {file_path}"


class LegacyVideoPlayer:
    """Legacy video player."""

    def start_video(self, video_path: str) -> str:
        """Start video playback."""
        return f"Playing video: {video_path}"


# Adapters
class AudioPlayerAdapter:
    """
    Adapt legacy audio player to MediaPlayer protocol.

    Examples:
        >>> player = AudioPlayerAdapter(LegacyAudioPlayer())
        >>> player.play("song.mp3")
        'Playing audio: song.mp3'
    """

    def __init__(self, legacy_player: LegacyAudioPlayer) -> None:
        """Initialize adapter with legacy player."""
        self.legacy_player = legacy_player

    def play(self, filename: str) -> str:
        """Adapt play method to legacy interface."""
        return self.legacy_player.play_audio_file(filename)


class VideoPlayerAdapter:
    """Adapt legacy video player to MediaPlayer protocol."""

    def __init__(self, legacy_player: LegacyVideoPlayer) -> None:
        """Initialize adapter with legacy video player."""
        self.legacy_player = legacy_player

    def play(self, filename: str) -> str:
        """Adapt play method to legacy interface."""
        return self.legacy_player.start_video(filename)


# Client code
def play_media(player: MediaPlayer, filename: str) -> str:
    """
    Play media using any player that conforms to MediaPlayer protocol.

    Args:
        player: Any object implementing MediaPlayer protocol
        filename: File to play

    Returns:
        Result message
    """
    return player.play(filename)


# Class adapter (using inheritance)
class ModernAudioPlayer:
    """Modern audio player."""

    def play(self, filename: str) -> str:
        """Play audio file."""
        return f"ModernPlayer: {filename}"


class AudioAdapter(LegacyAudioPlayer):
    """
    Class adapter using inheritance.

    Why avoid this in Python?
    - Multiple inheritance can be complex
    - Object adapter (composition) is more flexible
    - Protocol-based approach is more Pythonic
    """

    def play(self, filename: str) -> str:
        """Adapt using inheritance."""
        return self.play_audio_file(filename)


# Two-way adapter
class TwoWayAdapter:
    """Adapter that works both ways."""

    def __init__(self, legacy: LegacyAudioPlayer) -> None:
        """Initialize with legacy player."""
        self.legacy = legacy

    def play(self, filename: str) -> str:
        """Modern interface."""
        return self.legacy.play_audio_file(filename)

    def play_audio_file(self, file_path: str) -> str:
        """Legacy interface."""
        return self.play(file_path)


# Real-world example: API adapter
class OldWeatherAPI:
    """Legacy weather API."""

    def get_temperature_fahrenheit(self, city: str) -> float:
        """Get temperature in Fahrenheit."""
        # Simulate API call
        return 72.5

    def get_condition_code(self, city: str) -> int:
        """Get weather condition as code."""
        return 1  # 1 = sunny


class WeatherService(Protocol):
    """Modern weather service protocol."""

    def get_temperature(self, city: str, unit: str = "celsius") -> float:
        """Get temperature in specified unit."""
        ...

    def get_condition(self, city: str) -> str:
        """Get weather condition as string."""
        ...


class WeatherAPIAdapter:
    """
    Adapt old weather API to modern service.

    Examples:
        >>> old_api = OldWeatherAPI()
        >>> service = WeatherAPIAdapter(old_api)
        >>> service.get_temperature("NYC", "celsius")
        22.5
        >>> service.get_condition("NYC")
        'sunny'
    """

    _conditions = {
        1: "sunny",
        2: "cloudy",
        3: "rainy",
        4: "snowy",
    }

    def __init__(self, old_api: OldWeatherAPI) -> None:
        """Initialize with old API."""
        self.old_api = old_api

    def get_temperature(self, city: str, unit: str = "celsius") -> float:
        """Get temperature in specified unit."""
        fahrenheit = self.old_api.get_temperature_fahrenheit(city)
        if unit == "celsius":
            return round((fahrenheit - 32) * 5 / 9, 1)
        elif unit == "fahrenheit":
            return fahrenheit
        elif unit == "kelvin":
            return round((fahrenheit - 32) * 5 / 9 + 273.15, 1)
        else:
            raise ValueError(f"Unknown unit: {unit}")

    def get_condition(self, city: str) -> str:
        """Get weather condition as string."""
        code = self.old_api.get_condition_code(city)
        return self._conditions.get(code, "unknown")


def demonstrate_all() -> None:
    """Demonstrate Adapter pattern."""
    print("=== Adapter Pattern ===\n")

    # Object adapter
    print("1. Object Adapter:")
    audio_adapter = AudioPlayerAdapter(LegacyAudioPlayer())
    video_adapter = VideoPlayerAdapter(LegacyVideoPlayer())

    print(f"   {play_media(audio_adapter, 'song.mp3')}")
    print(f"   {play_media(video_adapter, 'movie.mp4')}")
    print()

    # Direct modern player (no adapter needed)
    print("2. Modern Player (no adapter):")
    modern = ModernAudioPlayer()
    print(f"   {play_media(modern, 'podcast.mp3')}")
    print()

    # Weather API adapter
    print("3. Weather API Adapter:")
    old_weather = OldWeatherAPI()
    weather_service = WeatherAPIAdapter(old_weather)

    print(f"   Temperature (C): {weather_service.get_temperature('NYC', 'celsius')}°C")
    print(f"   Temperature (F): {weather_service.get_temperature('NYC', 'fahrenheit')}°F")
    print(f"   Condition: {weather_service.get_condition('NYC')}")
    print()

    # Two-way adapter
    print("4. Two-way Adapter:")
    two_way = TwoWayAdapter(LegacyAudioPlayer())
    print(f"   Modern: {two_way.play('file.mp3')}")
    print(f"   Legacy: {two_way.play_audio_file('file.mp3')}")


if __name__ == "__main__":
    demonstrate_all()
