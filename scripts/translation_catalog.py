"""Read plain JSON catalogues with adjacent English translator-comment metadata.

``_fieldContext`` immediately precedes its translated ``field``. Primitive
string lists use one context per list item. Stable ``id``/``chapter`` values
are routing identifiers rather than translations. Metadata never reaches HTML,
speech, captions or runtime iteration over the actual translated fields.
"""
import json


CATALOGUES = (
    'content', 'ux-copy', 'download-copy', 'narration-copy',
    'scene-captions', 'scenario-captions', 'captions',
)


def strip_context(value):
    if isinstance(value, dict):
        return {key: strip_context(item) for key, item in value.items()
                if not (key.startswith('_') and key.endswith('Context'))}
    if isinstance(value, list):
        return [strip_context(item) for item in value]
    return value


def load_catalog(path):
    return strip_context(json.loads(path.read_text()))


def _contexts(value, path=()):
    """Validate coverage/adjacency and retain context by stable source path."""
    result = {}
    if isinstance(value, list):
        for index, item in enumerate(value):
            result.update(_contexts(item, path + (index,)))
    elif isinstance(value, dict):
        keys = list(value)
        for index, (key, item) in enumerate(value.items()):
            if key.startswith('_') and key.endswith('Context'):
                target = key[1:-7]
                assert target in value and index + 1 < len(keys) and keys[index + 1] == target, (path, key, 'orphan/nonadjacent context')
                continue
            primitive_list = isinstance(item, list) and all(isinstance(v, str) for v in item)
            if (isinstance(item, str) and key not in ('id', 'chapter')) or primitive_list:
                context = value.get(f'_{key}Context')
                comments = context if primitive_list else [context]
                assert isinstance(comments, list), (path, key, 'missing context list')
                assert len(comments) == (len(item) if primitive_list else 1), (path, key, 'context count')
                for comment in comments:
                    assert isinstance(comment, str) and all(label in comment for label in ('Context:', 'Display:', 'Source:', 'Args:')), (path, key, 'incomplete context')
                result[path + (key,)] = context
            else:
                result.update(_contexts(item, path + (key,)))
    return result


def check_catalog_contexts(source):
    for name in CATALOGUES:
        catalogue = json.loads((source / f'{name}.json').read_text())['languages']
        assert set(catalogue) == {'es', 'en', 'de', 'fr', 'ru', 'uk', 'pt'}, name
        authoritative = _contexts(catalogue['es'])
        assert authoritative, (name, 'empty context catalogue')
        for language, copy in catalogue.items():
            assert _contexts(copy) == authoritative, (name, language, 'context mismatch')
