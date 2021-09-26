from . import snowflake


class BaseDiscordObject:

    def __init__(self):
        self.id: snowflake.Snowflake

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def ingest_raw_dict(self, data: dict) -> 'BaseDiscordObject':
        '''
        Ingest and cache a given object for future use.
        '''
        raise NotImplementedError(f'{self.__class__.__name__} does not yet implement this function.')

    def from_dict(self, data: dict) -> 'BaseDiscordObject':
        '''
        Parse an object from a dictionary and return it.
        '''
        raise NotImplementedError(f'{self.__class__.__name__} does not yet implement this function.')

    def cache(self):
        '''
        Save object to the cache for faster recall in the future.
        '''
        raise NotImplementedError(f'{self.__class__.__name__} does not yet implement this function.')

    def to_dict(self) -> dict:
        '''
        Convert object to dictionary suitable for API or other generic useage.
        '''
        raise NotImplementedError(f'{self.__class__.__name__} does not yet implement this function.')
