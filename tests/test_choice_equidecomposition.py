import unittest

from core.geometry.choice_equidecomposition import (
    ChoiceExistenceClaim, FiniteEquidecompositionCertificate,
    FiniteGroupAction, MeasureLedger, MeasureStatus, PieceMove,
    SelectionKind, banach_tarski_scope_note, finite_choice,
)


class FiniteChoiceTests(unittest.TestCase):
    def test_deterministic_choice_records_provenance(self):
        family = {"beta": ("b", "a"), "alpha": (3, 1)}
        selected, records = finite_choice(family)
        self.assertEqual(selected, {"alpha": 1, "beta": "a"})
        self.assertEqual([r.family_key for r in records], ["alpha", "beta"])
        self.assertTrue(all(r.alternatives_preserved for r in records))

    def test_custom_selector_is_validated(self):
        family = {"x": (1, 2)}
        selected, records = finite_choice(family, lambda _key, values: values[-1])
        self.assertEqual(selected["x"], 2)
        self.assertEqual(records[0].method, "<lambda>")
        with self.assertRaises(ValueError):
            finite_choice(family, lambda _key, _values: 99)

    def test_empty_family_member_rejected(self):
        with self.assertRaises(ValueError):
            finite_choice({"empty": ()})

    def test_full_ac_is_existence_only(self):
        claim = ChoiceExistenceClaim("arbitrary family of nonempty sets")
        self.assertEqual(claim.selection_kind, SelectionKind.EXISTENCE_ONLY)
        with self.assertRaises(ValueError):
            ChoiceExistenceClaim("bad", selection_kind=SelectionKind.CONSTRUCTIVE)


class FiniteEquidecompositionTests(unittest.TestCase):
    def test_two_point_finite_certificate(self):
        carrier = ("a", "b")
        identity, swap = (0, 1), (1, 0)
        group = FiniteGroupAction(carrier, (identity, swap))
        certificate = FiniteEquidecompositionCertificate(
            source=frozenset({"a", "b"}),
            target_a=frozenset({"a"}), target_b=frozenset({"b"}),
            pieces={"left": frozenset({"a"}), "right": frozenset({"b"})},
            moves=(PieceMove("left", "A", identity),
                   PieceMove("right", "B", identity)),
            group=group,
        )
        self.assertTrue(certificate.validate())

    def test_invalid_partition_rejected(self):
        group = FiniteGroupAction(("a", "b"), ((0, 1), (1, 0)))
        certificate = FiniteEquidecompositionCertificate(
            source=frozenset({"a", "b"}),
            target_a=frozenset({"a"}), target_b=frozenset({"b"}),
            pieces={"left": frozenset({"a", "b"}), "right": frozenset({"b"})},
            moves=(PieceMove("left", "A", (0, 1)),
                   PieceMove("right", "B", (0, 1))),
            group=group,
        )
        with self.assertRaises(ValueError):
            certificate.validate()

    def test_measure_ledger_rejects_fake_nonmeasurable_volume(self):
        MeasureLedger("ball", MeasureStatus.MEASURABLE, 1.0)
        MeasureLedger("piece", MeasureStatus.NONMEASURABLE, None,
                      "not Lebesgue measurable")
        with self.assertRaises(ValueError):
            MeasureLedger("piece", MeasureStatus.NONMEASURABLE, 0.5)

    def test_banach_tarski_scope_is_explicit(self):
        note = banach_tarski_scope_note()
        self.assertEqual(note["status"], "abstract_existence_theorem")
        self.assertIn("no matter duplication", note["physical_interpretation"])


if __name__ == "__main__":
    unittest.main()
