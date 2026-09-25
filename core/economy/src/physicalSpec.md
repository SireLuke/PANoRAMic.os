# Physical PAR Specification

Physical PAR represents real‑asset‑backed certificates, not fiat.

---

## Properties

Each note has:
- `parAmount` — backed by real assets
- `assetSignatureId` — links to a real asset bundle
- `serial` — unique physical identifier
- `issuedAt` — timestamp
- `expiresAt` (optional) — for time‑bound vouchers

---

## Minting Rules

- Physical PAR is minted only from existing digital PAR.
- A max ratio (e.g. 20%) limits how much PAR can exist physically.
- Minting reduces digital PAR balance by the note’s `parAmount`.

---

## Verification

A note is valid if:
- `parAmount > 0`
- not expired
- has a valid `assetSignatureId`

---

## Purpose

- provide a physical, symbolic form of PAR
- remain non‑inflationary and non‑fiat
- be redeemable only against real assets
- embody humanitarian and ecological values
