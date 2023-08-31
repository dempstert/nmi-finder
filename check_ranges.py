
import json


def lies_in_numeric_range(s, numeric_data):
    """Check if the string `s` lies in any of the numeric ranges provided in `numeric_data`."""
    for key in numeric_data:
        for range_info in numeric_data[key]["ranges"]:
            if int(range_info["from"]) <= int(s) <= int(range_info["to"]):
                return ((s, numeric_data[key]["id"]), True)
    return (None, False)


def lies_in_alphanumeric_range(s, range_info):
    """Check if the alphanumeric string `s` lies in the specified alphanumeric range `range_info`."""
    from_val = range_info["from"]
    to_val = range_info["to"]

    if len(s) != len(from_val) or len(s) != len(to_val):
        return False

    for char_s, char_from, char_to in zip(s, from_val, to_val):
        if char_to == "Z":
            if not char_s.isalnum():
                return False
        else:
            if not char_from <= char_s <= char_to:
                return False

    return True


def lies_in_alphanumeric_ranges(s, alphanumeric_data):
    """Check if the string `s` lies in any of the alphanumeric ranges provided in `alphanumeric_data`."""
    for key in alphanumeric_data:
        for range_info in alphanumeric_data[key]["ranges"]:
            if lies_in_alphanumeric_range(s, range_info):
                return ((s, alphanumeric_data[key]["id"]), True)
    return (None, False)


def check_string_in_ranges(s, data):
    """Check if the string `s` lies in any of the ranges specified in `data`."""
    if s.isnumeric():
        return lies_in_numeric_range(s, data["numeric"])
    else:
        return lies_in_alphanumeric_ranges(s, data["alphanumeric"])


if __name__ == "__main__":
    # This section is for testing when running the script directly
    with open("combined_aemo.json", "r") as file:
        data = json.load(file)

    test_strings = ["2501000000", "QB05414270",
                    "QB09999999", "12345", "QB0A999999"]
    results = [check_string_in_ranges(
        test, data) for test in test_strings]
    print(results)
