"""
Facade Pattern - Provide simplified interface to complex subsystem.

Hides complexity of subsystems behind a simple interface.
"""

from __future__ import annotations


# Complex subsystem classes
class VideoFile:
    """Video file handler."""

    def __init__(self, filename: str) -> None:
        """Load video file."""
        self.filename = filename
        print(f"Loading video file: {filename}")


class AudioMixer:
    """Audio processing subsystem."""

    def fix_audio(self, file: VideoFile) -> str:
        """Fix audio issues."""
        return f"Fixing audio in {file.filename}"


class VideoCodec:
    """Video codec subsystem."""

    def __init__(self, codec_type: str) -> None:
        """Initialize codec."""
        self.codec_type = codec_type

    def compress(self, file: VideoFile) -> str:
        """Compress video."""
        return f"Compressing {file.filename} with {self.codec_type}"


class BitrateReader:
    """Read bitrate information."""

    def read(self, file: VideoFile) -> int:
        """Read bitrate."""
        print(f"Reading bitrate of {file.filename}")
        return 1000  # kb/s

    def convert(self, file: VideoFile, bitrate: int) -> str:
        """Convert to target bitrate."""
        return f"Converting {file.filename} to {bitrate}kb/s"


# Facade
class VideoConverter:
    """
    Simplified interface for video conversion.

    Hides complexity of audio, video, and bitrate subsystems.

    Examples:
        >>> converter = VideoConverter()
        >>> result = converter.convert("video.mp4", "avi")
        Loading video file: video.mp4
        Reading bitrate of video.mp4
        Fixing audio in video.mp4
        Compressing video.mp4 with avi
        Converting video.mp4 to 1000kb/s
        >>> "Conversion complete" in result
        True
    """

    def convert(self, filename: str, format: str) -> str:
        """
        Convert video file to specified format.

        This single method hides all the complexity of:
        - Loading the file
        - Reading bitrate
        - Fixing audio
        - Compressing video
        - Converting bitrate

        Args:
            filename: Input file
            format: Target format

        Returns:
            Conversion result message
        """
        file = VideoFile(filename)
        bitrate_reader = BitrateReader()
        audio_mixer = AudioMixer()
        codec = VideoCodec(format)

        # Complex orchestration hidden from client
        bitrate = bitrate_reader.read(file)
        audio_mixer.fix_audio(file)
        codec.compress(file)
        bitrate_reader.convert(file, bitrate)

        return f"Conversion complete: {filename} -> {format}"


# Another example: Home Theater Facade
class DVDPlayer:
    """DVD player subsystem."""

    def on(self) -> str:
        """Turn on DVD player."""
        return "DVD Player ON"

    def play(self, movie: str) -> str:
        """Play movie."""
        return f"Playing: {movie}"

    def off(self) -> str:
        """Turn off DVD player."""
        return "DVD Player OFF"


class Amplifier:
    """Amplifier subsystem."""

    def on(self) -> str:
        """Turn on amplifier."""
        return "Amplifier ON"

    def set_volume(self, level: int) -> str:
        """Set volume."""
        return f"Volume set to {level}"

    def off(self) -> str:
        """Turn off amplifier."""
        return "Amplifier OFF"


class Projector:
    """Projector subsystem."""

    def on(self) -> str:
        """Turn on projector."""
        return "Projector ON"

    def set_input(self, source: str) -> str:
        """Set input source."""
        return f"Input set to {source}"

    def off(self) -> str:
        """Turn off projector."""
        return "Projector OFF"


class Lights:
    """Lights subsystem."""

    def dim(self, level: int) -> str:
        """Dim lights."""
        return f"Lights dimmed to {level}%"

    def on(self) -> str:
        """Turn on lights."""
        return "Lights ON"


class HomeTheaterFacade:
    """
    Simplified interface for home theater operations.

    Examples:
        >>> theater = HomeTheaterFacade(
        ...     DVDPlayer(),
        ...     Amplifier(),
        ...     Projector(),
        ...     Lights()
        ... )
        >>> theater.watch_movie("Inception")
        'Ready to watch: Inception'
        >>> theater.end_movie()
        'Movie ended. Systems off.'
    """

    def __init__(
        self,
        dvd: DVDPlayer,
        amp: Amplifier,
        projector: Projector,
        lights: Lights,
    ) -> None:
        """Initialize with subsystems."""
        self.dvd = dvd
        self.amp = amp
        self.projector = projector
        self.lights = lights

    def watch_movie(self, movie: str) -> str:
        """
        Start watching a movie (one simple method).

        Handles all the complexity of:
        - Dimming lights
        - Turning on equipment
        - Setting correct inputs
        - Playing the movie
        """
        steps = [
            self.lights.dim(10),
            self.projector.on(),
            self.projector.set_input("DVD"),
            self.amp.on(),
            self.amp.set_volume(5),
            self.dvd.on(),
            self.dvd.play(movie),
        ]

        print("\n".join(f"  {step}" for step in steps))
        return f"Ready to watch: {movie}"

    def end_movie(self) -> str:
        """Turn off everything."""
        steps = [
            self.dvd.off(),
            self.amp.off(),
            self.projector.off(),
            self.lights.on(),
        ]

        print("\n".join(f"  {step}" for step in steps))
        return "Movie ended. Systems off."


def demonstrate_all() -> None:
    """Demonstrate Facade pattern."""
    print("=== Facade Pattern ===\n")

    # Video converter facade
    print("1. Video Converter Facade:")
    converter = VideoConverter()
    result = converter.convert("vacation.mp4", "avi")
    print(f"   {result}")
    print()

    # Home theater facade
    print("2. Home Theater Facade:")
    theater = HomeTheaterFacade(
        dvd=DVDPlayer(),
        amp=Amplifier(),
        projector=Projector(),
        lights=Lights(),
    )

    print("   Starting movie...")
    theater.watch_movie("The Matrix")
    print()

    print("   Ending movie...")
    theater.end_movie()


if __name__ == "__main__":
    demonstrate_all()
