# PyDepends
Python3 project to plot file dependency graphs and write ```requirements.txt``` automatically

## Dependencies
- Install dependencies using:
```
  pip install -r requirements.txt
```

## Usage
- Use```python3 main.py -h``` to see argument usage 
- ```python3 main.py -mr={module_root}``` to specify module root to inspect
- ```python3 main.py -af``` to inspect all files aside from ```.py``` files
- ```python3 main.py -ic={ignoreConfig}``` to specify which config file to read ignore files from
- ```python3 main.py -vb``` to print verbosely when finding dependencies

## Outputs
- Output png file as ```{module_root}_file_structure.png```

## Issues
- Currently not supporting
