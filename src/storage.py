"""
Module for reading and writing data to and from JSON files.
"""

import json
import os
from src.errors import InternalError

def load_data(file: str):
    """
    Loads JSON data from the specified file path.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            content=f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        raise InternalError("⚠️Error loading JSON file from") from e

def save_data(data, file:str):
    """
    Saves the given data to a JSON file at the specified path.
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise InternalError("⚠️Error saving JSON file") from e

def save_data_append(new_result, file: str):
    """
    Appends a new result to a list of results in the given JSON file.
    """
    try:
        try:
            data=load_data(file)
        except InternalError:
            data = []

        if not isinstance(data, list):
            raise InternalError("⚠️JSON file does not contain a list")

        data.append(new_result)
        save_data(data, file)
    except Exception as e:
        raise InternalError("⚠️Error saving JSON file") from e

def delete_file(file: str):
    """
    Deletes the given file if it exists.
    Does nothing if the file does not exist.
    """
    if os.path.isfile(file):
        os.remove(file)

def clear_file(file: str):
    """
    Clears the contents of the given file if it exists.
    If the file does not exist, does nothing.
    """
    if os.path.isfile(file):
        with open(file, "w", encoding="utf-8") as f:
            f.truncate(0)
