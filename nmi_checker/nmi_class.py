import re
import json
from itertools import chain
import pandas as pd
import pkg_resources

__JSON_CONFIG_FILE__ = "separated_data.json"


class RangeChecker:
    def __init__(self, json_name=None):

        self.is_list = False
        self.csv_output = []

        if json_name is None:
            print("Loading JSON from package")
            self.json_name = pkg_resources.resource_filename(
                __name__, __JSON_CONFIG_FILE__)
        else:
            self.json_name = json_name

        with open(self.json_name, 'r') as json_file:
            self.data = json.load(json_file)

        self.checker = NmiChecker()

    def lies_in_numeric_range(self, s, numeric_data):
        for key in numeric_data:
            for range_info in numeric_data[key]["ranges"]:
                if int(range_info["from"]) <= int(s) <= int(range_info["to"]):
                    return ((s, numeric_data[key]["id"]), True)
        return (None, False)

    def lies_in_alphanumeric_range(self, s, range_info):
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

    def lies_in_alphanumeric_ranges(self, s, alphanumeric_data):
        for key in alphanumeric_data:
            for range_info in alphanumeric_data[key]["ranges"]:
                if self.lies_in_alphanumeric_range(s, range_info):
                    return ((s, alphanumeric_data[key]["id"]), True)
        return (None, False)

    def check_string_in_ranges(self, s, original_nmi):
        if not s:
            return {
                "original": original_nmi,
                "output": (None, False)
            }
        if s.isnumeric():
            return {
                "original": original_nmi,
                "output": self.lies_in_numeric_range(s, self.data["numeric"])
            }
        else:
            return {"original": original_nmi, "output": self.lies_in_alphanumeric_ranges(s, self.data["alphanumeric"])}

    def generate_reason_and_results(self, nmi, found_status):
        reason = "NMI not found" if not found_status else ""
        output, result = self.checker.compare_checksum(nmi, found_status)
        reason = "Checksum Failed" if not found_status else ""
        range_out = self.check_string_in_ranges(output, nmi)
        reason = "Not in given Ranges of AEMO" if not range_out[
            "output"][1] else "NMI Found, Checksum Passed, Found in Range"
        range_out["reason"] = reason
        return range_out

    def process_input(self, input_data):
        # If it's a single string, return the tuple

        if any(isinstance(input_data, t) for t in [str, int]):
            self.is_list = False
            reason = ""
            nmi, found_status = self.checker.find_special_string(
                str(input_data))

            return self.generate_reason_and_results(nmi, found_status)
        # If it's a list of strings, return the list of tuples
        elif isinstance(input_data, list):
            self.is_list = True
            self.csv_output = []
            for s in input_data:
                nmi, found_status = self.checker.find_special_string(str(s))
                self.csv_output.append(
                    self.generate_reason_and_results(nmi, found_status))
            return self.csv_output
        else:
            raise ValueError(
                "Input data must be either a string or a list of strings")

    def to_df(self):

        if not self.is_list:
            raise ValueError(
                "Input data must be list of strings to get output as Pandas DataFrame")

        data = {
            'NMI': [],
            'modified_nmi': [],
            'State': [],
            'Result': [],
            'Remarks': []
        }

        for item in self.csv_output:
            data['NMI'].append(item["original"] if item["original"] else None)
            data['modified_nmi'].append(
                item["output"][0][0] if item["output"][1] else None)
            data['State'].append(item["output"][0][1]
                                 if item["output"][1] else None)
            data['Result'].append(item["output"][1])
            data['Remarks'].append(item["reason"])

        # Create and save the DataFrame directly
        return pd.DataFrame(data)

    def to_csv(self, filename):

        if not self.is_list:
            raise ValueError(
                "Input data must be list of strings to get output as CSV")

        self.to_df().to_csv(filename, index=False)


class NmiChecker:

    @staticmethod
    def load_string_from_file(filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
                content = content.replace('\n', ' ')
                clean_string = ' '.join(content.split())
                clean_string = clean_string.strip()
                clean_string = str(re.sub('\W+', ' ', clean_string))
                return clean_string
        except FileNotFoundError:
            print(f"The file '{filename}' was not found.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None

    def generate(self, nmi):
        if len(nmi) > 10:
            nmi = nmi[0:10]
        ascii_values = chain(
            map(lambda x: ord(x) * 2, nmi[-1::-2]), map(lambda x: ord(x), nmi[-2::-2]))
        ascii_digits = ''.join(map(lambda x: str(x), ascii_values))
        digits = map(lambda x: ord(x) - ord('0'), ascii_digits)
        reduction = sum(digits)
        return (10 - (reduction % 10)) % 10

    def find_special_string(self, text):
        """
        -> [A-HJ-NP-Z0-9]*: Matches zero or more uppercase letters and digits (excluding 'O' and 'I')
        -> [0-9]: Matches exactly one digit
        -> [A-HJ-NP-Z0-9]*: Matches zero or more uppercase letters and digits (excluding 'O' and 'I')
        -> {10,11} string should be 10 or 11 characters long
        """

        if not text:
            return None, False

        pattern = r'\b(?=[A-HJ-NP-Z0-9]*[0-9])[A-HJ-NP-Z0-9]{10,11}\b'
        match = re.search(pattern, text)
        if match:
            found_string = match.group()
            if 'O' not in found_string and 'I' not in found_string:
                print(f"String found {found_string}")
                return found_string, True
        print("NMI not found in text")
        return None, False

    def compare_checksum(self, result, found):

        if found and result:
            if not result[-1].isnumeric():
                print(f"{result} Last character is not a numeric ")
                char = str(ord(result[-1]))
                result = result[:-1] + char
                print(f"New NMI after replacing {result}")
            generated_digit = self.generate(result)
            last_character = int(result[-1])
            if len(result) > 10 and generated_digit == last_character:
                print(f"Checksum passed for {result[:10]}")
                return result[:10], True
            elif len(result) == 10:
                print(f"Checksum passed for {result}")
                return result, True
            else:
                print(
                    f"Checksum failed for string {result} and generated_digit {generated_digit}")
                return None, False
        return None, False

    def check(self, text):
        nmi, found_status = self.find_special_string(text)
        output, result = self.compare_checksum(nmi, found_status)
        if not result:
            return None, False
        # numeric_data = ''.join(filter(str.isdigit, output))
        return self.check_string_in_ranges(output)


if __name__ == "__main__":

    # Loading class and checking text output
    range_checker = RangeChecker()

    test_strings = ["2501000000", "QB05414270",
                    "QB09999999", "12345", "QB0A999999"]

    results = range_checker.process_input("QB05414270")

    print(results)
