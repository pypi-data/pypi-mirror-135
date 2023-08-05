# Chela
Chela is a Python library to handle chemical formula.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Chela

```bash
pip install chela
```

## Usage
From bash:
```bash
# Check correctness of chemical formula
python3 -m chela -c CHEMICAL_FORMULA

# Transform a csv file with a column containing the formulas
#into a dataframe with atomic symbols as columns and save it as a csv file
python3 -m chela -d FILE.csv NEW_FILE.csv
```
From python script:
```python3
import chela as cl

# check chemical formula with a function
cl.check_formula(CHEMICAL_FORMULA)

import pandas as pd

# check chemical formula with a pandas extensions
pd.DataFrame().chela.check_formula(CHEMICAL_FORMULA)

# Transform a csv file with a column containing the formulas
#into a dataframe with atomic symbols as columns
dataframe = cl.csv_to_dataframe(FILE.csv)

dataframe = pd.DataFrame().chela.csv_to_dataframe(FILE.csv)

# Drop formulas contaning elements with atomic number greater than Z
dataframe = dataframe.chela.drop_heavy_elements(Z)
```
## License
[MIT](https://choosealicense.com/licenses/mit/)
