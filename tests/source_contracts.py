"""Compare fixed approved source without serializing interpreter AST objects.

AST nodes locate source spans only. Tokens retain spelling, literals, operators,
logical newlines and block boundaries; comments, non-logical newlines, locations
and indentation width are excluded. Formatted strings are outside this small
canonicalizer's supported grammar (their tokenization changed in Python 3.12).
"""

import ast
import io
import tokenize

DOMAIN_NAMES = (
    "Text",
    "DigestionProfile",
    "ClaimLink",
    "Qualification",
    "Claim",
    "StageResult",
    "StageRequest",
)


def source_sections(source, names):
    """Select unique module-level declarations, retaining decorators and bodies."""
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    sections = {}
    for node in tree.body:
        found = []
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            found = [node.name]
        elif isinstance(node, ast.Assign):
            found = [t.id for t in node.targets if isinstance(t, ast.Name)]
        for name in set(found) & set(names):
            if name in sections:
                raise ValueError(f"Duplicate frozen declaration: {name}")
            first = min(
                [node.lineno] + [d.lineno for d in getattr(node, "decorator_list", ())]
            )
            # Column offsets are UTF-8 byte offsets, not character indices.
            last = lines[node.end_lineno - 1].encode()[: node.end_col_offset].decode()
            sections[name] = "".join(lines[first - 1 : node.end_lineno - 1]) + last
    if set(sections) != set(names):
        raise ValueError("Missing frozen declaration")
    return sections


def _tokens(source):
    ignored = {tokenize.COMMENT, tokenize.NL, tokenize.ENCODING, tokenize.ENDMARKER}
    return tuple(
        (
            tokenize.tok_name[t.type],
            "" if t.type in {tokenize.INDENT, tokenize.NEWLINE} else t.string,
        )
        for t in tokenize.generate_tokens(io.StringIO(source).readline)
        if t.type not in ignored
    )


def _diagnostic_policy(reference):
    """Only approved enum reads and already-approved conditional tests are inert.

    The reference is a checked-in fixture, never the current production source.
    New calls, assignments, operators or keyword names cannot disappear through
    the metadata exception. Conditional tests retain their exact approved tokens.
    """
    tree = ast.parse(reference)
    values = [
        keyword.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Raise)
        and isinstance(node.exc, ast.Call)
        and isinstance(node.exc.func, ast.Name)
        and node.exc.func.id == "DigestionError"
        for keyword in node.exc.keywords
        if keyword.arg in {"diagnostic", "reason"}
    ]
    enums = {
        (n.value.id, n.attr)
        for value in values
        for n in ast.walk(value)
        if isinstance(n, ast.Attribute)
        and isinstance(n.value, ast.Name)
        and n.value.id in {"Reason", "ValidationDiagnostic"}
    }
    conditions = {
        _expression_tokens(ast.get_source_segment(reference, n.test))
        for value in values
        for n in ast.walk(value)
        if isinstance(n, ast.IfExp)
    }
    return enums, conditions


def _expression_tokens(source):
    return _tokens("(" + source + ")\n")


def _is_metadata(node, source, enum, enums, conditions):
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        return node.value.id == enum and (enum, node.attr) in enums
    return (
        isinstance(node, ast.IfExp)
        and _expression_tokens(ast.get_source_segment(source, node.test)) in conditions
        and _is_metadata(node.body, source, enum, enums, conditions)
        and _is_metadata(node.orelse, source, enum, enums, conditions)
    )


def canonical_source(source, *, diagnostic_reference=None):
    """Return portable lexical data; optionally omit inert rejection metadata.

    Only diagnostic/reason keywords on a directly raised DigestionError qualify.
    Positional arguments, unknown keywords, predicates and execution order remain
    protected. Its argument separators are reconstructed, so adding/removing
    approved metadata and the associated trailing commas are equivalent.
    """
    tree = ast.parse(source)
    if any(isinstance(n, ast.JoinedStr) for n in ast.walk(tree)):
        raise ValueError("Formatted strings require reviewed canonicalization")
    if diagnostic_reference is None:
        return _tokens(source)
    enums, conditions = _diagnostic_policy(diagnostic_reference)
    lines = source.encode().splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    replacements = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Raise) or not isinstance(node.exc, ast.Call):
            continue
        call = node.exc
        if not isinstance(call.func, ast.Name) or call.func.id != "DigestionError":
            continue
        args = [ast.get_source_segment(source, arg) for arg in call.args]
        for keyword in call.keywords:
            enum = {"diagnostic": "ValidationDiagnostic", "reason": "Reason"}.get(
                keyword.arg
            )
            if enum is None:
                args.append(ast.get_source_segment(source, keyword))
            elif not _is_metadata(keyword.value, source, enum, enums, conditions):
                raise ValueError("Unapproved executable diagnostic metadata")
        replacements.append(
            (
                offsets[call.lineno - 1] + call.col_offset,
                offsets[call.end_lineno - 1] + call.end_col_offset,
                ("DigestionError(" + ", ".join(args) + ")").encode(),
            )
        )
    value = source.encode()
    for start, end, replacement in sorted(replacements, reverse=True):
        value = value[:start] + replacement + value[end:]
    return _tokens(value.decode())


def assert_source_contract(actual, approved, *, allow_diagnostics=False):
    """Fail against independent, reviewable approved source, without refreshes."""
    reference = approved if allow_diagnostics else None
    assert canonical_source(actual, diagnostic_reference=reference) == canonical_source(
        approved, diagnostic_reference=reference
    ), "Frozen source contract changed"
