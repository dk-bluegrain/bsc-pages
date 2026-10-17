import importlib.util
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

    def test_rounded_excerpt_boundary_assigns_caption_to_the_new_scene(self):
        data = b'WEBVTT\n\n1\n00:01:27.665 --> 00:01:30.000\nFirst scene\n\n2\n00:01:34.598 --> 00:01:38.000\nNext scene\n'
        groups = [(87.665, 94.59800000000001), (94.598, 101.531)]
        with patch.object(media, 'source_bytes', return_value=data), patch.object(media, 'source_json', return_value={'languages': {'en': {}}}):
            cues = media.narration_candidates('unused', 'test', groups)
        self.assertEqual([0, 1], [cue['group'] for cue in cues])
        self.assertTrue(all(cue['required'] for cue in cues))


if __name__ == '__main__':
    unittest.main()
