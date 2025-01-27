# Pancham Data Pipelines

Pancham simplifies the process of reading and processing data with Pandas. 

## What is it for

A common scenario in data migration projects is to need to take exports from one system, apply some transformation rules and write the data somewhere else. This could be files, a database or an API. All of this can be done with Pandas but we would need to write a lot of code, Pancham is here to make that process easier.

```mermaid
flowchart LR;
    s[Source Files]-->t[Transformation];
    t-->o[Output Files];
```
### Key features

- Load files
- Rename fields
- Validate data types and not-null columns
- Apply python functions to transform values
- Return data as a Pandas DataFrame

### Supported Source Files

- Excel

### Supported Output

- SQL
- CSV

Additional sources and output formats will be added with time.

## Example

```python
loader = DataFrameLoader({FileType.EXCEL_XLSX: ExcelFileLoader()}, PrintReporter())
configuration = DataFrameConfiguration(self.filename, FileType.EXCEL_XLSX, sheet='Sheet1')
configuration.add_field('Order', 'Order Id', int)
configuration.add_field('Date', 'Rec Date', datetime.datetime)
configuration.add_dynamic_field('Sent', field_type=bool, func=lambda row: row['Disp.'] == 'X')

data = loader.load(configuration)
```