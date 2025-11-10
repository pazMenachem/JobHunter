"""Relevance status enumeration with priority levels."""

from enum import Enum


class RelevanceStatus(Enum):
    """
    Job relevance status with priority levels for filtering.
    """
    YES       = 1
    MAYBE     = 2
    NO        = 3
    DUPLICATE = 4
    UNKNOWN   = 5
    ALL       = 6
    
    @classmethod
    def from_string(cls, status_str: str) -> 'RelevanceStatus':
        """Convert string to RelevanceStatus enum.
        
        Args:
            status_str: String representation of status
            
        Returns:
            RelevanceStatus enum value
        """

        match status_str.lower().strip():
            case "yes":
                return cls.YES
            case "maybe":
                return cls.MAYBE
            case "no":
                return cls.NO
            case "duplicate":
                return cls.DUPLICATE
            case _:
                return cls.UNKNOWN
