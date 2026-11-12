import json
import unittest

from core.seed_sharing.contract import (
    ReceiverState,
    SeedEnvelope,
    SeedIdentityCollision,
    share_seed,
)


class SeedSharingContractTests(unittest.TestCase):
    def test_seed_is_additive_and_base_memory_is_preserved(self):
        receiver = ReceiverState(
            base_memory={"profile": {"epoch": 7, "notes": ["keep"]}},
            seed_ledger={"old": {"seed_id": "old", "content_sha256": "prior"}},
        )
        before = json.dumps(receiver.base_memory, sort_keys=True)
        result = share_seed(
            receiver,
            SeedEnvelope("new", "source-A", "v1", {"signal": 42}, ("old",)),
        )
        self.assertEqual(json.dumps(result.base_memory, sort_keys=True), before)
        self.assertIn("old", result.seed_ledger)
        self.assertIn("new", result.seed_ledger)
        self.assertEqual(result.seed_ledger["new"]["parent_seed_ids"], ["old"])
        self.assertEqual(result.seed_ledger["new"]["source_id"], "source-A")

    def test_identical_share_is_idempotent(self):
        receiver = ReceiverState(base_memory={"keep": True})
        envelope = SeedEnvelope("s1", "source-A", "v1", {"x": [1, 2]})
        once = share_seed(receiver, envelope)
        twice = share_seed(once, envelope)
        self.assertEqual(once, twice)

    def test_same_id_with_different_content_is_rejected(self):
        receiver = ReceiverState()
        first = share_seed(receiver, SeedEnvelope("s1", "source-A", "v1", {"x": 1}))
        with self.assertRaises(SeedIdentityCollision):
            share_seed(first, SeedEnvelope("s1", "source-A", "v1", {"x": 2}))

    def test_inputs_are_not_mutated(self):
        memory = {"nested": {"value": 3}}
        payload = {"items": [1, 2]}
        receiver = ReceiverState(base_memory=memory)
        envelope = SeedEnvelope("s1", "source-A", "v1", payload)
        share_seed(receiver, envelope)
        self.assertEqual(memory, {"nested": {"value": 3}})
        self.assertEqual(payload, {"items": [1, 2]})
        self.assertEqual(receiver.seed_ledger, {})

    def test_non_json_payload_is_rejected(self):
        with self.assertRaises(ValueError):
            SeedEnvelope("s1", "source-A", "v1", {"bad": object()}).to_record()


if __name__ == "__main__":
    unittest.main()
