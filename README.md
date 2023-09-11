
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

[
 {'original': '2501000000',
  'output': (('2501000000', 'PWCLNSP'), True),
  'reason': 'NMI Found, Checksum Passed, Found in Range'},
 {'original': 'QB05414270',
  'output': 
{
 'original': '2501000000',
 'output': (('2501000000', 'PWCLNSP'), True),
 'reason': 'NMI Found, Checksum Passed, Found in Range'
}
,
  'reason': 'NMI Found, Checksum Passed, Found in Range'},
 {'original': 'QB09999999',
  'output': (('QB09999999', 'ENERGEXP'), True),
  'reason': 'NMI Found, Checksum Passed, Found in Range'},
 {'original': None,
  'output': (None, False),
  'reason': 'Not in given Ranges of AEMO'},
 {'original': 'QB0A999999',
  'output': (None, False),
  'reason': 'Not in given Ranges of AEMO'}
]

```

2. Using a single string:

```python
result = range_checker.process_input("2501000000")
print(result)
```

Output:
```

{
 'original': '2501000000',
 'output': (('2501000000', 'PWCLNSP'), True),
 'reason': 'NMI Found, Checksum Passed, Found in Range'
}

```


### New Methods in `RangeChecker` class:

There are two new methods added to the `RangeChecker` class: `to_df` and `to_csv`.

<b style="color:red;">NOTE</b> : The `to_df` and `to_csv` methods can only be called when the input to `process_input` is a list of strings. 

#### `to_df`:
This method converts the result of `process_input` into a DataFrame. 

**Usage**:
```python

r = RangeChecker()
result = r.process_input(["2501000000", "QB05414270", "QB09999999", "12345", "QB0A999999"])
out_df = r.to_df()

```
`out_df` now contains the output dataframe.

#### `to_csv`:
This method saves the result of `process_input` to a CSV file. It requires a filename as an argument.

**Usage**:
```python

r = RangeChecker()
result = r.process_input(["2501000000", "QB05414270", "QB09999999", "12345", "QB0A999999"])
r.to_csv("csv_fun_check.csv")

```
This will generate a CSV file named `csv_fun_check.csv`.


## Author

- Akhlaq Ahmed
