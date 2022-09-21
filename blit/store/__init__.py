"""Blit storage prototypes"""

from pkg_resources import iter_entry_points


class BlitStoreError(IOError):
    """simple class to handle errors"""

    pass


class BlitStore:
    """Parent class for all Blit storage"""

    def __init__(self, *args, **kwargs):
        """Default constructor for Blit storage objects"""

        self.uri = args[0]

    def __repr__(self):
        return f"{self.__class__}({self.uri})"

    @staticmethod
    def handler(*args, **kwargs):

        for entry in iter_entry_points("blit_store"):
            if entry.name == proto:
                return entry.load()(name, entry.extras)
