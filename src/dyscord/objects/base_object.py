from abc import ABC
from ..utilities import log


class BaseDiscordObject(ABC):
    '''Abstract base of all common discord objects. All subclasses map directly to an actual API object.'''

    _log = log.Log()

    def from_dict(self, data: dict) -> 'BaseDiscordObject':
        '''Parse an object from a dictionary and return it.'''
        raise NotImplementedError(f'{self.__class__.__name__} does not yet implement this function.')

    def to_dict(self) -> dict:
        '''Convert object to dictionary suitable for API or other generic useage.'''
        raise NotImplementedError(f'{self.__class__.__name__} does not yet implement this function.')
