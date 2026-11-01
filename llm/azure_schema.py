"""Azure strict structural subset, version azure-strict/1.

Only string format/length/pattern constraints move to application validation.
Titles/defaults are generation annotations; const is represented as singleton enum.
Unknown constructs fail closed. This converter never processes model output.
"""
from llm.inference import InferenceConfigurationError

PROFILE = 'azure-strict/1'


def provider_schema(schema):
    """Copy a closed application schema into the deliberately narrow Azure subset."""
    def fail():
        raise InferenceConfigurationError('Unsupported strict provider schema configuration.')

    def convert(node, root=False):
        if not isinstance(node, dict):
            fail()
        allowed = {'type', 'properties', 'required', 'additionalProperties', 'items',
                   '$defs', '$ref', 'anyOf', 'enum', 'const', 'title', 'description',
                   'default', 'format', 'minLength', 'maxLength', 'pattern'}
        if set(node) - allowed:
            fail()
        if any(k in node for k in ('format', 'minLength', 'maxLength', 'pattern')):
            if node.get('type') != 'string' or ('format' in node and node['format'] != 'uuid'):
                fail()
        out = {k: v for k, v in node.items() if k not in {
            'title', 'default', 'format', 'minLength', 'maxLength', 'pattern'}}
        if 'const' in out:
            if 'enum' in out:
                fail()
            out['enum'] = [out.pop('const')]
        kind = out.get('type')
        if root and kind != 'object':
            fail()
        if '$ref' in out:
            if set(out) != {'$ref'} or not isinstance(out['$ref'], str):
                fail()
        elif 'anyOf' in out:
            if root or set(out) != {'anyOf'} or not isinstance(out['anyOf'], list) or not out['anyOf']:
                fail()
            out['anyOf'] = [convert(v) for v in out['anyOf']]
        elif kind not in ('object', 'array', 'string', 'integer', 'number', 'boolean', 'null'):
            fail()
        if kind == 'object':
            props = out.get('properties')
            if not isinstance(props, dict) or out.get('additionalProperties') is not False:
                fail()
            required = out.get('required', [])
            if not isinstance(required, list) or any(k not in props for k in required):
                fail()
            out['properties'] = {k: convert(v) for k, v in props.items()}
            out['required'] = list(props)
        elif any(k in out for k in ('properties', 'required', 'additionalProperties')):
            fail()
        if kind == 'array':
            out['items'] = convert(out.get('items'))
        elif 'items' in out:
            fail()
        if '$defs' in out:
            if not root or not isinstance(out['$defs'], dict):
                fail()
            out['$defs'] = {k: convert(v) for k, v in out['$defs'].items()}
        if 'enum' in out:
            values = out['enum']
            types = {'string': str, 'integer': int, 'number': (int, float), 'boolean': bool,
                     'null': type(None)}
            if kind not in types or not isinstance(values, list) or not values:
                fail()
            if any(not isinstance(v, types[kind]) for v in values):
                fail()
            out['enum'] = list(values)
        return out

    try:
        result = convert(schema, root=True)
        definitions = result.get('$defs', {})
        count = 0

        def count_properties(node):
            nonlocal count
            count += len(node.get('properties', {}))
            for child in node.get('properties', {}).values():
                count_properties(child)
            for child in node.get('$defs', {}).values():
                count_properties(child)
            for child in node.get('anyOf', []):
                count_properties(child)
            if 'items' in node:
                count_properties(node['items'])
        count_properties(result)
        if count > 100:
            fail()

        def depth(node, level=-1, seen=()):
            if '$ref' in node:
                ref = node['$ref']
                if not ref.startswith('#/$defs/') or ref[8:] not in definitions or ref in seen:
                    fail()  # Recursive constructs are outside this finite stage contract.
                return depth(definitions[ref[8:]], level, (*seen, ref))
            # Root is depth zero; count nested containers, resolving local refs.
            level += node.get('type') in ('object', 'array')
            if level > 5:
                fail()
            for child in node.get('properties', {}).values():
                depth(child, level, seen)
            for child in node.get('anyOf', []):
                depth(child, level, seen)
            if 'items' in node:
                depth(node['items'], level, seen)
        depth(result)
        for definition in definitions.values():
            depth(definition)
        return result
    except (TypeError, ValueError, RecursionError):
        fail()
