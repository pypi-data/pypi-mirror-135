import time
import contextlib
import shutil

from typing import Union, Generator


class Heartbeat:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.staging_filepath = f"{filepath}.staging"

    def _get_current_time(self):
        return time.time()

    def read(self) -> float:
        """
        Get time value from the heartbeat file.
        """
        with open(self.filepath, "r") as infile:
            last_time = infile.read()
        return float(last_time)

    def write_to_staging_file(self, heartbeat_content: str) -> None:
        """
        Write current time to the staging file.
        """
        with open(self.staging_filepath, "w", encoding="utf-8") as outfile:
            outfile.write(heartbeat_content)

    def write(self, heartbeat_content: str) -> None:
        """
        Write current time to the heartbeat file.
        First, write to a staging file and replace it
        when written. This is to avoid reading from empty file
        that is just being written into.
        """
        self.write_to_staging_file(heartbeat_content)
        shutil.move(self.staging_filepath, self.filepath)

    def update(self, heartbeat_content: str = None) -> None:
        """
        Update heartbeat file to given content or current time.
        """
        heartbeat_content = (
            heartbeat_content
            if heartbeat_content is not None
            else str(self._get_current_time())
        )
        self.write(heartbeat_content)

    def is_alive(self, alive_threshold_ms: float) -> bool:
        """
        Check if timestamp in heartbeat file is newer than alive_threshold_ms.
        """
        last_time = self.read()
        return (
            self._get_current_time() - last_time
        ) * 1000 < alive_threshold_ms

    @contextlib.contextmanager
    def long_operation(
        self, long_operation_duration_seconds: Union[int, float]
    ) -> Generator:
        """
        On entry, updates heartbeat to time which is
        long_operation_duration_seconds from now.
        On exit, updates heartbeat to current timestamp.
        """
        try:
            self.update(
                str(self._get_current_time() + long_operation_duration_seconds)
            )
            yield
        finally:
            self.update()
