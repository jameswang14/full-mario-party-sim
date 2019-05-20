from abc import ABC, abstractmethod
from enum import Enum

class ItemType(Enum):
    SELF = 1
    LAND = 2
    PASS = 3

class ItemBase(object):

    @property
    @abstractmethod
    def cost(self):
        pass

    @property
    def type(self):
        pass
    
    @abstractmethod
    def apply(self, player, state, target=None):
        pass


        
