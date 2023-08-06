
# Pycosmic

A Simple Package that makes Your Code Simple




## Installation

Install pycosmic with `pip`

```bash
  pip install pycosmic
```
or 


```
git clone https://github.com/rishabh-creator601/pycosmic.git
cd pycosmic
python setup.py install 
```

    
## Usage/Examples

1) Get code of any function / class 
```python
from pc import codeof

def test(a,b):
    return a + b

print(codeof(test))
>>> def test(a,b):
     return a + b

   
```

2) download a file from github

```python 
from pc import SetCode

SetCode(repo={reponame},filename={filename},user={username})


```

3) Extract Mathematical Equations from string 

```python 
from pc import Parser

exp = "hello string 2 + 2"
eq = Parser(exp).exp
print(eq)
>>> 2 + 2

```

