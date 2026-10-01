# Startup Entry Points

**Canonical Boot Path:** `src/boot.ts`

## Primary Entry Points

- `npm start` → runs `src/boot.ts` via package.json
- `deno run --allow-all src/boot.ts` → direct TypeScript execution
- `deno run --allow-all main.ts` → root-level canonical entry (delegates to src/boot.ts)
- `deno run --allow-all src/main.ts` → src-level canonical entry (delegates to src/boot.ts)

## Legacy Compatibility Shims (Deprecated)

The following files are maintained for backward compatibility but should not be used in new code:

- `boot.ts` ⚠️ deprecated
- `start.ts` ⚠️ deprecated
- `run.ts` ⚠️ deprecated
- `cli/start.ts` ⚠️ deprecated
- `cli/run.ts` ⚠️ deprecated

All legacy entry points now delegate to `src/boot.ts` to ensure a single canonical startup flow.

## Boot Sequence

1. Kernel initialization
2. Feed integration layer
3. RAMS pre-audit
4. RSDV (scarcity vector) computation
5. PAR economy initialization
6. Demurrage engine activation
7. Stagnation metric setup
8. Node network boot
9. Dashboard and visualization online
10. System ready

All functions are orchestrated from `src/boot.ts`.
