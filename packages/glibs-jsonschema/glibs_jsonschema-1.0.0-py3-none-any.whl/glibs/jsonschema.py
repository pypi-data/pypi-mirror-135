from __future__ import absolute_import

import jsonschema


# Custom "required" and "additionlProperties" validators
# --------------------
# Those "fixes" are needed because the default jsonschema behaviour is to NOT inform us which field
# triggered error when the validation that generated the error is a schema-wide validation
# (e.g.: validating if all required fields have been passed) and not a property specific validation
# such as checking for correct types.

# "required" fix
# https://github.com/Julian/jsonschema/issues/119
def _required(validator, required, instance, schema):
    """Validate 'required' properties."""
    if not validator.is_type(instance, "object"):  # pragma: no cover
        return

    for index, requirement in enumerate(required):
        if requirement not in instance:
            error = jsonschema.ValidationError(
                "{0!r} is a required property".format(requirement)
            )
            error.schema_path.append(index)
            error.path.append(requirement)
            yield error


# "additionalProperties" fix
# https://github.com/Julian/jsonschema/blob/master/jsonschema/_validators.py
def _additional_properties(validator, aP, instance, schema):
    """Validate 'additionalProperties' properties."""
    from jsonschema import _utils

    if not validator.is_type(instance, "object"):  # pragma: no cover
        return

    extras = set(_utils.find_additional_properties(instance, schema))

    if validator.is_type(aP, "object"):
        # We hardly use this below
        for extra in extras:  # pragma: no cover
            for error in validator.descend(instance[extra], aP, path=extra):
                yield error

    elif not aP and extras:
        for extra in extras:
            error = jsonschema.ValidationError("Unrecognized property")
            error.path.append(extra)
            yield error


# Construct validator as extension of Json Schema Draft 4.
Validator = jsonschema.validators.extend(
    validator=jsonschema.validators.Draft4Validator,
    validators={
        "required": _required,
        "additionalProperties": _additional_properties,
    },
)


# This class stores the errors coming from jsonschema in a more 'geekie-friendly' format
class SchemaValidationError(Exception):
    def __init__(self, errors):
        super(SchemaValidationError, self).__init__("Error validating the schema")
        self.errors = errors


def validate(instance, schema):
    def error_path(error, suberror=None):
        path = list(error.path)
        if suberror:
            path += list(suberror.path)
        if not path:
            return "<instance>"

        final_path = str(path[0])
        for part in path[1:]:
            if isinstance(part, int):
                final_path += "[{}]".format(part)
            else:
                final_path += ".{}".format(part)

        return final_path

    errors = {}
    validator = Validator(schema)

    for error in sorted(validator.iter_errors(instance), key=str):
        if error.context:
            for suberror in sorted(error.context, key=lambda e: e.schema_path):
                errors[error_path(error, suberror)] = suberror.message
        else:
            errors[error_path(error)] = error.message

    if errors:
        raise SchemaValidationError(errors)
