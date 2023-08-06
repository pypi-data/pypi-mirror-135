# redistricting-tools

`redistricing-tools` is a set of Python scripts for use with US legislative redistricting.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install redistricting-tools.

```bash
pip3 install redistricting-tools
```

## Usage

```bash
# Nest House districts into Senate districts. See examples in the nestings folder.
# nestings.csv          First column is the senate district and each following column is a nested house district.
nest-districts [-h] blocks.csv nestings.csv output-senate-blocks.csv

# Combine two maps. If there are BLOCKID collisions, warnings are given for the districts in source-two.csv
# that already have set the same BLOCKIDs in source-one.csv
combine-districts [-h] source-one.csv source-two.csv output-blocks.csv

# Remove districts from a map. Useful to create non-overlapping maps to combine using combine-districts
remove-districts [-h] [--districts DISTRICTS] blocks.csv output-blocks.csv
```

## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)