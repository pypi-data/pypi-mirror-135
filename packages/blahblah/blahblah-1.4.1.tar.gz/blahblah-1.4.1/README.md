# blahblah

[![Codecov](https://img.shields.io/codecov/c/github/nikitanovosibirsk/blahblah/master.svg?style=flat-square)](https://codecov.io/gh/nikitanovosibirsk/blahblah)
[![PyPI](https://img.shields.io/pypi/v/blahblah.svg?style=flat-square)](https://pypi.python.org/pypi/blahblah/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/blahblah?style=flat-square)](https://pypi.python.org/pypi/blahblah/)
[![Python Version](https://img.shields.io/pypi/pyversions/blahblah.svg?style=flat-square)](https://pypi.python.org/pypi/blahblah/)

Fake data generator for [district42](https://github.com/nikitanovosibirsk/district42) schema

(!) Work in progress, breaking changes are possible until v2.0 is released

## Installation

```sh
pip3 install blahblah
```

## Usage

```python
from blahblah import fake
from district42 import schema

UserSchema = schema.dict({
    'id': schema.int.min(1),
    'name': schema.str.regex(r"[a-z0-9_]+"),
    'is_deleted': schema.bool,
})

print(fake(UserSchema))
```

## Documentation

* [Documentation](#documentation)
  * [None](#none)
    * [schema.none](#schemanone)
  * [Bool](#bool)
    * [schema.bool](#schemabool)
    * [schema.bool(`value`)](#schemaboolvalue)
  * [Int](#int)
    * [schema.int](#schemaint)
    * [schema.int(`value`)](#schemaintvalue)
    * [schema.int.min(`value`)](#schemaintminvalue)
    * [schema.int.max(`value`)](#schemaintmaxvalue)
  * [Float](#float)
    * [schema.float](#schemafloat)
    * [schema.float(`value`)](#schemafloatvalue)
    * [schema.float.min(`value`)](#schemafloatminvalue)
    * [schema.float.max(`value`)](#schemafloatmaxvalue)
  * [Str](#str)
    * [schema.str](#schemastr)
    * [schema.str.len(`length`)](#schemastrlenlength)
    * [schema.str.len(`min_length`, `max_length`)](#schemastrlenmin_length-max_length)
    * [schema.str.alphabet(`letters`)](#schemastralphabetletters)
    * [schema.str.contains(`substr`)](#schemastrcontainssubstr)
    * [schema.str.regex(`pattern`)](#schemastrregexpattern)
  * [List](#list)
    * [schema.list](#schemalist)
    * [schema.list(`elements`)](#schemalistelements)
    * [schema.list(`type`)](#schemalisttype)
    * [schema.list(`type`).len(`length`)](#schemalisttypelenlength)
    * [schema.list(`type`).len(`min_length`, `max_length`)](#schemalisttypelenmin_length-max_length)
  * [Dict](#dict)
    * [schema.dict](#schemadict)
    * [schema.dict(`keys`)](#schemadictkeys)
  * [Any](#any)
    * [schema.any](#schemaany)
    * [schema.any(`*types`)](#schemaanytypes)
  * [Custom Types](#custom-types)
    * [1. Declare Schema](#1-declare-schema)
    * [2. Register Generator](#2-register-generator)
    * [3. Use](#3-use)

### None

#### schema.none

```python
sch = schema.none

assert fake(sch) is None
```

### Bool

#### schema.bool

```python
sch = schema.bool

assert fake(sch) in (True, False)
```

#### schema.bool(`value`)

```python
sch = schema.bool(True)

assert fake(sch) is True
```

### Int

#### schema.int

```python
INT_MIN = -(2 ** 63)
INT_MAX = 2 ** 63 - 1

sch = schema.int

assert INT_MIN <= fake(sch) <= INT_MAX
```

#### schema.int(`value`)

```python
sch = schema.int(42)

assert fake(sch) == 42
```

#### schema.int.min(`value`)

```python
sch = schema.int.min(0)

assert 0 <= fake(sch) <= INT_MAX
```

#### schema.int.max(`value`)

```python
sch = schema.int.max(0)

assert INT_MIN <= fake(sch) <= 0
```

### Float

#### schema.float

```python
sch = schema.float

assert isinstance(fake(sch), float)
```

#### schema.float(`value`)

```python
sch = schema.float(3.14)

assert fake(sch) == 3.14
```

#### schema.float.min(`value`)

```python
sch = schema.float.min(0.0)

assert fake(sch) >= 0.0
```

#### schema.float.max(`value`)

```python
sch = schema.float.max(0.0)

assert fake(sch) <= 0.0
```

### Str

#### schema.str

```python
sch = schema.str

generated = fake(sch)
assert isinstance(generated, str)
```

#### schema.str.len(`length`)

```python
sch = schema.str.len(10)

generated = fake(sch)
assert len(generated) == 10
```

#### schema.str.len(`min_length`, `max_length`)

```python
sch = schema.str.len(1, ...)

generated = fake(sch)
assert len(generated) >= 1
```

```python
sch = schema.str.len(..., 32)

generated = fake(sch)
assert len(generated) <= 32
```

```python
sch = schema.str.len(1, 32)

generated = fake(sch)
assert 1 <= len(generated) <= 32
```

#### schema.str.alphabet(`letters`)

```python
digits = "01234567890"
sch = schema.str.alphabet(digits)

generated = fake(sch)
assert all(x in digits for x in generated)
```

#### schema.str.contains(`substr`)

```python
sch = schema.str.contains("@")

generated = fake(sch)
assert "@" in generated
```

#### schema.str.regex(`pattern`)

```python
import re
sch = schema.str.regex(r"[a-z]+")

generated = fake(sch)
assert re.match(r"[a-z]+", generated)
```

### List

#### schema.list

```python
sch = schema.list

generated = fake(sch)
assert isinstance(generated, list)
```

#### schema.list(`elements`)

```python
sch = schema.list([schema.int(1), schema.int(2)])

generated = fake(sch)
assert generated = [1, 2]
```

#### schema.list(`type`)

```python
sch = schema.list(schema.int)

generated = fake(sch)
assert all(isinstance(x) for x in generated)
```

#### schema.list(`type`).len(`length`)

```python
sch = schema.list(schema.int).len(3)

generated = fake(sch)
assert len(generated) == 3
```

#### schema.list(`type`).len(`min_length`, `max_length`)

```python
sch = schema.list(schema.int).len(1, ...)

generated = fake(sch)
assert len(generated) >= 1
```

```python
sch = schema.list(schema.int).len(..., 10)

generated = fake(sch)
assert len(generated) <= 10
```

```python
sch = schema.list(schema.int).len(1, 10)

generated = fake(sch)
assert 1 <= len(generated) <= 10
```

### Dict

#### schema.dict

```python
sch = schema.dict

generated = fake(sch)
assert isinstance(generated, dict)
```

#### schema.dict(`keys`)

```python
sch = schema.dict({
    "id": schema.int,
    "name": schema.str | schema.none,
    optional("platform"): schema.str,
})

generated = fake(sch)
assert isinstance(generated["id"], int)
assert isinstance(generated["name"], (str, type(None))
assert generated.keys() == {"id", "name"}
```

### Any

#### schema.any

```python
sch = schema.any

generated = fake(sch)
assert isinstance(generated, object)
```

#### schema.any(`*types`)

```python
sch = schema.any(schema.str, schema.int)

generated = fake(sch)
assert isinstance(generated, (str, int))
```

### Custom Types

#### 1. Declare Schema

```python
from typing import Any
from uuid import UUID
from district42 import Props, SchemaVisitor, SchemaVisitorReturnType as ReturnType
from district42.types import Schema
from niltype import Nilable


class UUIDProps(Props):
    @property
    def value(self) -> Nilable[UUID]:
        return self.get("value")


class UUIDSchema(Schema[UUIDProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        return visitor.visit_uuid(self, **kwargs)

    def __call__(self, /, value: UUID) -> "UUIDSchema":
        return self.__class__(self.props.update(value=value))
```

#### 2. Register Generator

```python
from typing import Any
from uuid import UUID, uuid4
from blahblah import Generator
from niltype import Nil


class UUIDGenerator(Generator, extend=True):
    def visit_uuid(self, schema: UUIDSchema, **kwargs: Any) -> UUID:
        if schema.props.value is not Nil:
            return schema.props.value
        return uuid4()
```

#### 3. Use

```python
from blahblah import fake
from district42 import register_type, schema

register_type("uuid", UUIDSchema)

print(fake(schema.uuid))
# 0d9d188a-4f1f-4bce-ba6e-51ca3732900e
```

Full code available here: [district42_exp_types/uuid](https://github.com/nikitanovosibirsk/district42-exp-types/tree/master/district42_exp_types/uuid)
