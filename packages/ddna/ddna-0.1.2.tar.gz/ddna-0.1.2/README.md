# DDNA
Program / Library that converts sentences to DNA sequence and vice-versa.

[![Pylint](https://github.com/Aayush9029/DDNA/actions/workflows/pylint.yml/badge.svg)](https://github.com/Aayush9029/DDNA/actions/workflows/pylint.yml) [![pytest](https://github.com/Aayush9029/DDNA/actions/workflows/pytest.yml/badge.svg)](https://github.com/Aayush9029/DDNA/actions/workflows/pytest.yml)
```js
O       o O       o O       o
A O   o | A O   o | | O   o G
| G O | C 1 | O G | T | O | 1
1 o   O | T o   O A | o   O C
o       O o       O o       O
```

### Installation:
```sh
pip install ddna
```


### Usage:

- *program*
```
 python3 -m ddna -h    
usage: ddna.py [-h] [-e ENCODE] [-d DECODE]

DDNA - DNA Encoder/Decoder

optional arguments:
  -h, --help            show this help message and exit
  -e ENCODE, --encode ENCODE
                        Encode String to DNA
  -d DECODE, --decode DECODE
                        Decode DNA to String
```

- *pip package*
```
>>> from ddna import DDNA
>>> DDNA().encode("HELLO WORLD")
'CAGACACCCATACATACATTAGAACCCTCATTCCAGCATACACA'
>>> DDNA().decode("CAGACACCCATACATACATTAGAACCCTCATTCCAGCATACACA")
'HELLO WORLD'
```

### Plans:
- [ ] Introduce Mutations
- [ ] Introduce new form of encryption based on mutations

