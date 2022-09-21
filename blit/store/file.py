"""Simple file storage for Blit objects"""

from pathlib import Path
from hashlib import sha256, blake2b

from blit.store import BlitStore, BlitStoreError


class BlitFileStore(BlitStore):
    """A file-based storage for Blit objects"""

    def __init__(self, *args, **kwargs):
        """Initialize a BlitFileStore"""

        super().__init__(*args, **kwargs)

        for d in args:

            dir_path = Path(d)

            if not dir_path.exists():
                dir_path.mkdir(parents=True)

            if not dir_path.is_dir():
                raise BlitStoreError(f"{d} exists, not a directory")
