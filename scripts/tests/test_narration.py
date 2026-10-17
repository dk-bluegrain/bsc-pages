import importlib.util
import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('narrate', Path(__file__).parents[1] / 'narrate-media.py')
media = importlib.util.module_from_spec(spec)
spec.loader.exec_module(media)


class PacingTest(unittest.TestCase):
    def test_idle_edits_preserve_actions_and_leave_input_markers_readable(self):
        events = [
            {'type': 'hold', 'timeSeconds': 0, 'durationMs': 10000, 'cue': 'review'},
            {'type': 'tap', 'timeSeconds': 3},
            {'type': 'sms-autofill', 'timeSeconds': 6},
        ]
        cuts = media.idle_cuts(events, 10, [(0, 10)], [4])
        self.assertTrue(cuts)
        for start, end in cuts:
            self.assertLess(start, end)
            for point in (0, 3, 6, 10):
                self.assertTrue(end <= point - .6 + .00001 or start >= point + 1.2 - .00001)
        for frame in range(151):
            at = frame / 15
            self.assertLessEqual(media.mapped_time(at, cuts), at)
        self.assertAlmostEqual(media.mapped_time(10, cuts), 10 - sum(b - a for a, b in cuts))

    def test_narration_budget_limits_pause_removal(self):
        events = [{'type': 'hold', 'timeSeconds': 0, 'durationMs': 10000, 'cue': 'read'}]
        cuts = media.idle_cuts(events, 10, [(0, 10)], [9])
        self.assertGreaterEqual(media.mapped_time(10, cuts), 9)

    def test_overlapping_holds_never_remove_the_same_frame_twice(self):
        hold = {'type': 'hold', 'timeSeconds': 0, 'durationMs': 10000, 'cue': 'read'}
        cuts = media.idle_cuts([hold, dict(hold)], 10, [(0, 10)], [7])
        self.assertLessEqual(sum(b - a for a, b in cuts), 3.00001)
        self.assertTrue(all(b <= c for (a, b), (c, d) in zip(cuts, cuts[1:])))

    def test_no_holds_means_no_cuts(self):
        self.assertEqual([], media.idle_cuts([{'type': 'tap', 'timeSeconds': 2}], 10, [(0, 10)], [4]))


class EditorialEvidenceTest(unittest.TestCase):
    def test_excluded_attempt_is_archived_and_retained_hold_spans_both_timelines(self):
        original = {'events': [{'type': 'tap', 'timeSeconds': 1, 'x': 100, 'y': 100},
                               {'type': 'hold', 'timeSeconds': 2, 'durationMs': 8000},
                               {'type': 'tap', 'timeSeconds': 3},
                               {'type': 'tap', 'timeSeconds': 8}]}
        exclusions = [{'start': 3, 'end': 7, 'reason': 'Repeated attempt'}]
        result = media.remap_events(original, [(3, 7)], exclusions)
        self.assertEqual(original['events'], result['originalEvents'])
        self.assertEqual([1, 2, 4], [e['timeSeconds'] for e in result['events']])
        self.assertEqual(4000, result['events'][1]['durationMs'])
        self.assertEqual(original['events'][2], result['excludedEvents'][0]['event'])
        self.assertEqual('Repeated attempt', result['excludedEvents'][0]['reason'])
        self.assertNotIn('sourceTimeSeconds', original['events'][0])

    def test_every_authored_cue_survives_explicit_source_exclusions(self):
        original = media.source_json(media.SOURCE, 'src/media.json')
        for id, info in original.items():
            with self.subTest(chapter=id):
                events = media.source_json(media.SOURCE, f'docs/media/events/{id}.json')['events']
                groups = media.groups_for(id, info, events)
                cues = media.narration_candidates(media.SOURCE, id, groups)
                exclusions = media.editorial_cuts(media.SOURCE, id, info['duration'])
                self.assertFalse(any(c['start'] <= cue['sourceStart'] < c['end']
                                     for c in exclusions for cue in cues))
                retained = media.remap_events({'events': events},
                    [(c['start'], c['end']) for c in exclusions], exclusions)
                self.assertEqual(len(events), len(retained['events']) + len(retained['excludedEvents']))



class NarrationSchedulingTest(unittest.TestCase):
    def cue(self, at, end, required=True, group=0):
        return {'sourceStart': at, 'sourceEnd': end, 'group': group,
                'required': required, 'text': {'en': 'English', 'de': 'Deutsch'}}

    def test_longest_translation_reserves_space_without_overlap(self):
        clips = {('en', 'English'): b'\0' * (2 * media.SAMPLE_RATE),
                 ('de', 'Deutsch'): b'\0' * (4 * media.SAMPLE_RATE)}
        cues = media.schedule([self.cue(0, 5), self.cue(1, 7, False)], [(0, 8)], [], clips)
        self.assertEqual(2, len(cues))
        self.assertGreaterEqual(cues[1]['start'], cues[0]['start'] + max(cues[0]['lengths'].values()) + .249)

    def test_required_speech_cannot_overrun_a_scene(self):
        clips = {('en', 'English'): b'\0' * (6 * media.SAMPLE_RATE),
                 ('de', 'Deutsch'): b'\0' * (6 * media.SAMPLE_RATE)}
        with self.assertRaisesRegex(ValueError, 'does not fit'):
            media.schedule([self.cue(0, 1)], [(0, 2)], [], clips)

    def test_optional_state_description_is_omitted_if_it_would_describe_a_later_state(self):
        clips = {('en', 'English'): b'\0' * (4 * media.SAMPLE_RATE),
                 ('de', 'Deutsch'): b'\0' * (4 * media.SAMPLE_RATE)}
        cues = media.schedule([self.cue(0, 3), self.cue(1, 2, False)], [(0, 10)], [], clips)
        self.assertEqual(1, len(cues))

    def test_required_action_cannot_spill_into_the_next_authored_step(self):
        clips = {('en', 'English'): b'\0' * (4 * media.SAMPLE_RATE),
                 ('de', 'Deutsch'): b'\0' * (4 * media.SAMPLE_RATE)}
        cue = dict(self.cue(0, 1), stateBounded=True)
        with self.assertRaisesRegex(ValueError, 'does not fit'):
            media.schedule([cue], [(0, 10)], [], clips)

    def test_idle_cuts_never_remove_frames_reserved_for_speech(self):
        events = [{'type': 'hold', 'timeSeconds': 0, 'durationMs': 10000, 'cue': 'read'}]
        cuts = media.idle_cuts(events, 10, [(0, 10)], [1], protected_windows=[(2, 5)])
        self.assertTrue(cuts)
        for a, b in cuts:
            self.assertTrue(b <= 2 or a >= 5)

    def test_rounded_excerpt_boundary_resolves_only_events_in_the_new_group(self):
        catalogue = {'phrases': {'action': {'context': 'A recorded task.',
                     'text': {lang: 'Task' for lang in media.VOICES}}},
                     'timelines': {'overview': [[{'key': 'action', 'anchor':
                         {'type': 'tap', 'occurrence': 1}}]] * 2}}
        events = {'events': [{'type': 'tap', 'timeSeconds': 87.665},
                             {'type': 'tap', 'timeSeconds': 94.598}]}
        groups = [(87.665, 94.59800000000001), (94.598, 101.531)]
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'src').mkdir()
            (root / 'src/narration-actions.json').write_text(json.dumps(catalogue))
            with patch.object(media, 'ROOT', root), patch.object(media, 'source_json', return_value=events):
                cues = media.narration_candidates('unused', 'overview', groups)
        self.assertEqual([0, 1], [cue['group'] for cue in cues])
        self.assertEqual([87.665, 94.598], [cue['sourceStart'] for cue in cues])
        self.assertTrue(all(cue['required'] and cue['stateBounded'] for cue in cues))


class AuthoredCaptureAlignmentTest(unittest.TestCase):
    def test_every_authored_action_resolves_to_the_pinned_capture(self):
        original = media.source_json(media.SOURCE, 'src/media.json')
        catalogue = json.loads((media.ROOT / 'src/narration-actions.json').read_text())
        self.assertEqual(set(original), set(catalogue['timelines']))
        for id, info in original.items():
            with self.subTest(chapter=id):
                events = media.source_json(media.SOURCE, f'docs/media/events/{id}.json')['events']
                groups = media.groups_for(id, info, events)
                cues = media.narration_candidates(media.SOURCE, id, groups)
                self.assertTrue(all(cue['required'] for cue in cues))
                self.assertEqual(len(groups), sum(cue['summary'] for cue in cues))
                self.assertTrue(all(cue['sourceEnd'] - cue['sourceStart'] >= 4 for cue in cues))
                self.assertEqual([cue['sourceStart'] for cue in cues],
                                 sorted(cue['sourceStart'] for cue in cues))


if __name__ == '__main__':
    unittest.main()
