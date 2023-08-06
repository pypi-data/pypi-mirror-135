<div align="center">
	<h1 align="center">
		<img src="images/repository-image-crop.png" alt="absfuyu"/>
	</h1>
  <p align="center">
	<a href="https://pypi.org/project/absfuyu/"><img src="https://img.shields.io/pypi/dm/absfuyu?style=flat-square" alt="pypi"/></a>
	<a href="https://pypi.org/project/absfuyu/"><img src="https://img.shields.io/pypi/v/absfuyu?style=flat-square" /></a>
  </p>
</div>

---


*TL;DR: A collection of code*

Soon will have more feature


## INSTALLATION:

```bash
pip install absfuyu
```

## USAGE:

Help
```python
import absfuyu
absfuyu.help()
```

Import specific module
```python
from absfuyu import calculate
```


## LIST:
```
calculate: use to calculate small thing
fibonacci: fibonacci stuff
generate: generate stuff
obfuscator: it does what it said (in dev)
sort: just sort
string: some string method
util: some random utilities
```


## EXAMPLE:
```python
import absfuyu as ab
# check if 6 is a perfect number
print(ab.isPerfect(6))
```
```python
import absfuyu as ab
# generate a random password
print("".join(ab.generator.randStrGen(20,1,"full")))
"""
# or
from absfuyu import generator as gen
print("".join(gen.randStrGen(20,1,"full")))
"""
```


## LICENSE:
```
MIT License

Copyright (c) 2022 AbsoluteWinter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```