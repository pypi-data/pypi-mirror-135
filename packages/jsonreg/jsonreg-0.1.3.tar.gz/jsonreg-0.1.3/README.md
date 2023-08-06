# JSONreg

json reg is a python module to quickly create json keys to store data
## Examples
### Simple json key
`main.py`
```python
import jsonreg
jsonreg.create("test.json","Test","This is test data")
```
`test.json`
```json
{
    "name": "Test",
    "id": 408557195864,
    "data": "This is test data"
}
```
### Json key in an external folder
`main.py`
```python
import jsonreg
jsonreg.create("reg/test.json","Test","This is test data")
```
**Note**: The `reg` folder must exist and should look like this

```
.
├── main.py
└── reg
```

`reg/test.json`
```json
{
    "name": "Test",
    "id": 408557195864,
    "data": "This is test data"
}
```