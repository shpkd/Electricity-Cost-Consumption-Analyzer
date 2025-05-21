"""
Tests for JSON file input/output functions without using fixtures.
"""

import json
import os
import tempfile
import pytest
from src.errors import InternalError
from src.storage import load_data, save_data, save_data_append, delete_file


def create_temp_json_file():
    """Helper function that creates a temporary JSON file for testing."""
    temp_fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(temp_fd)

    test_data = [{"name": "test1", "value": 1}, {"name": "test2", "value": 2}]

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    return temp_path


def create_non_list_json_file():
    """Helper function that creates a temporary JSON file with non-list data."""
    temp_fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(temp_fd)

    test_data = {"name": "test", "value": 1}

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    return temp_path


def test_delete_file_existing():
    """Test deleting an existing file."""
    #Create a temporary file
    temp_fd, temp_path = tempfile.mkstemp()
    os.close(temp_fd)

    #Verify the file exists
    assert os.path.isfile(temp_path)

    #Delete the file
    delete_file(temp_path)

    #Verify the file was deleted
    assert not os.path.isfile(temp_path)

def test_load_data_success():
    """Test that data is properly loaded from a JSON file."""
    # Create a temporary file with data
    temp_path=create_temp_json_file()

    try:
        data=load_data(temp_path)

        assert isinstance(data, list)
        assert len(data)==2
        assert data[0]["name"]=="test1"
        assert data[1]["value"]==2
    finally:
        delete_file(temp_path)


def test_load_data_file_not_found():
    """Test that InternalError is raised when file is not found."""
    with pytest.raises(InternalError) as exc_info:
        load_data("non_existent_file.json")

    assert "⚠️Error loading JSON file from" in str(exc_info.value)


def test_save_data_success():
    """Test that data is properly saved to a JSON file."""
    temp_fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(temp_fd)

    test_data={
        "key": "value",
        "list": [1, 2, 3]
    }

    try:
        save_data(test_data, temp_path)
        saved_data=load_data(temp_path)

        assert saved_data == test_data
    finally:
        delete_file(temp_path)


def test_save_data_append_to_existing_list():
    """Test appending data to an existing list in a JSON file."""
    temp_path = create_temp_json_file()

    try:
        new_item={
            "name": "test3",
            "value": 3
        }
        save_data_append(new_item, temp_path)

        updated_data = load_data(temp_path)

        assert len(updated_data)==3
        assert updated_data[2]==new_item
    finally:
        delete_file(temp_path)


def test_save_data_append_to_new_file():
    """Test appending data to a new file (should create a list)."""
    temp_fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(temp_fd)
    os.remove(temp_path)

    try:
        new_item = {
            "name": "test1",
            "value": 1
        }

        save_data_append(new_item, temp_path)
        data = load_data(temp_path)

        assert isinstance(data, list)
        assert len(data)==1
        assert data[0]==new_item
    finally:
        delete_file(temp_path)


def test_save_data_append_to_non_list():
    """Test that InternalError is raised when appending to a non-list."""
    temp_path=create_non_list_json_file()

    try:
        with pytest.raises(InternalError) as exc_info:
            save_data_append({"new": "item"}, temp_path)

        assert "⚠️Error saving JSON file" in str(exc_info.value)
    finally:
        delete_file(temp_path)
