## glibs-jsonschema

A wrapper around `jsonschema` for a nicer API.

### Usage

`glibs.jsonschema.validate(object, schema)`

The library only supports the [Draft 4](https://json-schema.org/specification-links.html#draft-4) of spec.

If the validation succeeds, the function returns nothing. If it fails, it will raise the `glibs.jsonschema.SchemaValidationError` exception. The exception should have an attribute `errors` that's a dict whose keys are the fields that failed validation.

Example:

```python
from glibs.jsonschema import validate, SchemaValidationError

schema = {
  "type": "object",
  "properties": {
    "user_id": {"type": "string"}
  }
}

try:
  validate({"user_id": 0}, schema)
except SchemaValidationError as exc:
  print(exc.errors)  # -> {"user_id": "0 is not of type 'string'"}
```
