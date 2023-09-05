
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
[(('2501000000', 'PWCLNSP'), True), (('2502000000', 'ENERGEXP'), True), (('2503000000', 'ENERGEXP'), True), (None, False), (None, False)]
```

2. Using a single string:

```python
result = range_checker.process_input("2501000000")
print(result)
```

Output:
```
(('QB05414270', 'ENERGEXP'), True)
```



## Author

- Akhlaq Ahmed
