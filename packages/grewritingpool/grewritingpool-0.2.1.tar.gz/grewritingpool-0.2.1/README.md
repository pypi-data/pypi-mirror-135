# Helper for GRE Writing Pool

[![pypi](https://flat.badgen.net/pypi/v/grewritingpool)](https://pypi.org/project/grewritingpool/)

Because why not?

## Install

`pip install grewritingpool`

or install from source:
`python3 setup.py install`

## Usage

### As a API

**get_list(writing_type='default')**

Return a json list of articles. Input can be `all`, `issue` or `argument`, default to `all`.

Returned json format:
```
[
    {
        'type': <writing type>,
        'first': <first part of the question>,
        'second': <first part of the question, might not exist>,
        'instruc': <instruction>
    },
    ...
]
```

**get_random(writing_type='default')**

Return a random json string from the json list of articles. Input can be `all`, `issue` or `argument`, default to `all`.

Returned json format:
```
{
    'type': <writing type>,
    'first': <first part of the question>,
    'second': <first part of the question, might not exist>,
    'instruc': <instruction>
}
```

### As a executable

```bash
grewriting [all|issue|argument]
```

## License

GPLv3.
