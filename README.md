
# NMI Checker

The NMI Checker is a Python package that checks for Network Metering Identifiers (NMI) within a given text. The package verifies whether the provided NMIs fall within valid ranges as specified in the [NMI Allocation List](https://aemo.com.au/-/media/files/electricity/nem/retail_and_metering/metering-procedures/nmi-allocation-list.pdf?la=en).

## Installation

You can install the NMI Checker package directly from GitHub using the following command:

```
pip install git+https://github.com/Threadlet/nmi-finder.git
```

## Usage

The primary method for checking NMIs is `process_input`, which can take either a single string or a list of strings as input. Based on the input type, it will process and return the results accordingly.

### Example:

<b style="color:red;">NOTE</b>: <i> We have used NMIs directly in this example but `process_input` method is capable to process OCR output of bills in the form of string datatype, it can search for NMI and run it through all the processes. </i>
  


1. Using a list of strings:

```python
from nmi_checker import RangeChecker
r = RangeChecker()
results = r.process_input('123')
print(results)

range_checker = RangeChecker()
test_strings = ["2501000000", "QB05414270", "QB09999999", "12345", "QB0A999999"]
results = range_checker.process_input(test_strings)
print(results)
```

Output:
```
NMI not found in text
[(('2501000000', 'PWCLNSP'), True), (('QB05414270', 'ENERGEXP'), True), (('QB09999999', 'ENERGEXP'), True), (None, False), (None, False)]
```

2. Using a single string:

```python
result = range_checker.process_input("QB05414270")
print(result)
```

Output:
```
(('QB05414270', 'ENERGEXP'), True)
```

#### Output Explanation:

The output is a list of tuples (for list input) or a single tuple (for string input). Each tuple contains:
- Another tuple with the provided NMI and its corresponding identifier.
- A boolean value indicating whether the NMI was found within the valid range.

For instance, the output `(('QB05414270', 'ENERGEXP'), True)` indicates that the NMI "QB05414270" corresponds to the identifier "ENERGEXP" and is within a valid range.

The package is also capable of processing entire text blobs and searching for valid NMIs within them.

## References

This package checks the NMI ranges as per the [NMI Allocation List](https://aemo.com.au/-/media/files/electricity/nem/retail_and_metering/metering-procedures/nmi-allocation-list.pdf?la=en).

## Author

- Akhlaq Ahmed
