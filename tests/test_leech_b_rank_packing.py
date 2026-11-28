import os
import tempfile
import unittest

import numpy as np

from experiments.leech24_eqbit_001.leech_b_rank import (
    NPAIRS,
    load_checkpoint,
    packed_column_mask,
    save_checkpoint,
)


class TestPackedColumnMask(unittest.TestCase):
    def test_mask_tracks_packbits_big_order_in_little_endian_words(self):
        # Exercise every bit in one 64-column word, including byte boundaries.
        for column in range(64):
            bits = np.zeros(64, dtype=np.uint8)
            bits[column] = 1
            packed = np.packbits(bits, bitorder="big")
            word = np.frombuffer(packed.tobytes(), dtype="<u8")[0]
            self.assertNotEqual(word & packed_column_mask(column), 0)
            self.assertEqual(
                int(word & (np.uint64(0xFFFFFFFFFFFFFFFF) ^ packed_column_mask(column))),
                int(word) ^ int(packed_column_mask(column)),
            )

    def test_last_partial_word_maps_only_real_columns(self):
        # 98,280 columns occupy 1,536 words; the last word has 40 real bits.
        real_columns = range(98240, NPAIRS)
        masks = [int(packed_column_mask(c)) for c in real_columns]
        self.assertEqual(len(set(masks)), 40)
        self.assertEqual(set(masks), {1 << b for b in (7, 15, 23, 31, 39, 47, 55, 63)} |
                         {1 << b for b in (0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 16, 17,
                                           18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 32,
                                           33, 34, 35, 36, 37, 38)})


class TestEliminationCheckpoint(unittest.TestCase):
    def test_rank_and_column_cursor_are_independent(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "checkpoint.npz")
            save_checkpoint(path, rank=17, next_col=23)
            self.assertEqual(load_checkpoint(path), (17, 23))

    def test_legacy_rank_only_checkpoint_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "legacy.npz")
            np.savez(path, rank=np.array([512]))
            with self.assertRaisesRegex(RuntimeError, "rank-only checkpoint is unsafe"):
                load_checkpoint(path)


if __name__ == "__main__":
    unittest.main()
