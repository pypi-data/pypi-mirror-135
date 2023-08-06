# Search String

![GitHub Workflow Status (branch)](https://github.com/kaas-mulvad/search-string/workflows/CI/badge.svg)
[![PyPI - Version](https://img.shields.io/pypi/v/search-string)][pypi]
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/search-string)

## Installation

You can install `search-string` from [PyPI][pypi]:

```bash
$ pip install search-string-overvaagning
```

The package is supported on Python 3.6+.

## About

This package implements the search string object that is used across [overvaagning.app](https://overvaagning.app/) for different types of surveillance.

It is used for searching a text. For something to be deemed a match, the text must match the `first_str` and if the `second_str` is not empty, the text must also match the `second_str`. If the `not_str` is not empty, the text must *not* match the `not_str`. A logical AND is used between the three conditions. The three strings can each be a collection of strings separated by semicolons wherein a match is deemed by logical OR. You can use '~' to make a word boundary. Finally, you can use `!global` at the end of a string to signal that that part should check globally.

Quick examples:

```python
>>> ss = SearchString('example;hello', 'text', 'elephant', data=None)
>>> ss.match('This is an example text')
True
>>> ss.match('This text says hello')
True
>>> ss.match('This is just an example')
False
```


## Usage


### Creating Search Strings

Start by importing the `SearchString` class:

```python
>>> from search_string import SearchString
```

Construct a new search string by supplying the `first_str`, `second_str`, `not_str` and any data that can be useful to refer back to later, such as an ID:

```python
ss = SearchString('first', '', '', data=2)
```

### Matching text

If you just need to find out whether a given search string matches a text, you can use the method `.match` on a `SearchString` instance.

Often, what you want to do, is to match a collection of search strings across a list of text, e.g. sentences. You can do that the following way:

```python
>>> from search_string import SearchString
>>> search_strings = [
...    SearchString('kan', '', 'ritzau', data=1),
...    SearchString('kan', '', 'ritzau!global', data=2)
... ]
>>> sentences = [
...    'Du kan skrive din tekst her.',
...    'Den kan bestå af flere sætninger.',
...    'Dig og Ritzau kan bestemme hvordan det skal være.',
...    'Nogle kan være lange, andre kan være korte.'
... ]
>>> res = SearchString.find_all(sentences, search_strings)
>>> res
[SearchString(kan, -, ritzau, data=1)]
```

For each of the matched search strings (in the above example, only one), you can extract the data and the matched text as follows:

```python
>>> res[0].data
1
>>> res[0].matched_text
'Du kan skrive din tekst her. Den kan bestå af flere sætninger. (...) Nogle kan være lange, andre kan være korte.'
>>> res[0].matched_text_highligthed
'Du <b>kan</b> skrive din tekst her. Den <b>kan</b> bestå af flere sætninger. (...) Nogle <b>kan</b> være lange, andre <b>kan</b> være korte.'
```


[pypi]: https://pypi.org/project/search-string/
[issues]: https://github.com/kaas-mulvad/search-string/issues
[release]: https://github.com/kaas-mulvad/search-string/releases/latest
