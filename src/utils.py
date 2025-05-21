"""
Utility functions
"""

from src.errors import InternalError

def get_month_range(start: int, end:int, months:list, mark:int=1):
    """
    Returns a list of months between start and end
    """
    if start<end:
        return months[start-1:end-1]
    if start == end and mark==2:
        return []
    return months[start-1:]+months[:end-1]

def count_months(start: int, end:int):
    """
    Returns the number of months between start and end
    """
    if start==end:
        return 12
    return (end-start)%12

# @generated (partially) ChatGPT 4o
def to_float(value: str) :
    """
    Converts a string to a float
    """
    try:
        return float(value.replace(",", "."))
    except Exception as e:
        raise InternalError("⚠️Not a number") from e
