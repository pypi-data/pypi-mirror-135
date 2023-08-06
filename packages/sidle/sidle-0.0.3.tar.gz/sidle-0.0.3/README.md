# sidle
A simple data encryption with password for Python

Example with `Sidle`:
```python
from sidle import Sidle
#: Sidle is a class for handling storing files and more.

sidle = Sidle(filename='data', password='12345')
sidle['username'] = 'zenqi'
```
Using `SidleData`
```python
from sidle import SidleData
#: SidleData is a simple datastructure that hold key and the value
#: given.

sidle = SidleData()
sidle['username'] = 'zenqi'

```

