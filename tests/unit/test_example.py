"""
Example unit tests to verify testing framework works.
"""


def test_basic_functionality():
    """Test that basic Python functionality works."""
    assert 1 + 1 == 2
    assert "hello" + " world" == "hello world"
    print("✅ Basic functionality test passed!")


def test_list_operations():
    """Test list operations."""
    test_list = [1, 2, 3]
    test_list.append(4)
    assert len(test_list) == 4
    assert test_list[-1] == 4
    print("✅ List operations test passed!")


def test_dictionary_operations():
    """Test dictionary operations."""
    test_dict = {"name": "John", "age": 25}
    test_dict["city"] = "New York"
    assert test_dict["name"] == "John"
    assert test_dict["city"] == "New York"
    print("✅ Dictionary operations test passed!")
