import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location(
    'translation_catalog', Path(__file__).parents[1] / 'translation_catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)
COMMENT = 'Context: Login. Display: Button. Source: build.py. Args: none.'


class TranslationCatalogTest(unittest.TestCase):
    def test_renderer_receives_original_shape_without_speaking_comments(self):
        source = {'languages': {'es': {
            '_titleContext': COMMENT, 'title': 'Acceso',
            'steps': [{'_bodyContext': COMMENT, 'body': 'Revisa'}],
            '_cuesContext': [COMMENT], 'cues': ['Código recibido'],
        }}}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'copy.json'
            path.write_text(json.dumps(source))
            self.assertEqual({'languages': {'es': {
                'title': 'Acceso', 'steps': [{'body': 'Revisa'}],
                'cues': ['Código recibido'],
            }}}, catalog.load_catalog(path))

    def test_missing_and_nonadjacent_comments_fail(self):
        for source in ({'title': 'Acceso'},
                       {'title': 'Acceso', '_titleContext': COMMENT},
                       {'_titleContext': COMMENT, 'id': 'login', 'title': 'Acceso'},
                       {'_cuesContext': [COMMENT], 'cues': ['Uno', 'Dos']}):
            with self.subTest(source=source), self.assertRaises(AssertionError):
                catalog._contexts(source)

    def test_checked_in_catalogues_have_shared_context_in_all_languages(self):
        catalog.check_catalog_contexts(Path(__file__).parents[2] / 'src')


if __name__ == '__main__':
    unittest.main()
