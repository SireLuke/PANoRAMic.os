"""Leech eqbit: build the antipodal cut matrix B and probe its F2 rank.

Definition (Lucas/Cosmo, 2026-11-22): vertices = 196,560 Leech minimal
vectors (bench Golay construction, scaled coords, norm^2 = 32);
adjacency tau = 2 (lattice units; scaled inner product +16);
transversal T = first-nonzero-coordinate-positive (98,280 reps);
B[a][b] = 1 iff <a,b> = -16 scaled (i.e. <a,-b> = +16: the 60-degree
cut across antipodal pairs). rank_F2(B) is the eqbit signature.

Stages: gen -> build -> probe -> subrank -> eliminate (checkpointed).
B is stored bit-packed with columns padded to 98,304 (1536 uint64/row).
"""
import itertools, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VEC_NPZ = os.path.join(HERE, "leech_T.npz")
B_BIN = os.path.join(HERE, "B_padded.bin")
NPAIRS = 98280
PADCOLS = 98304
WORDS = PADCOLS // 64
CHECKPOINT_SCHEMA = 2


def packed_column_mask(column):
    """Mask for a packbits(bitorder='big') column in a little-endian uint64 word.

    The on-disk matrix is a byte stream. NumPy's uint64 memmap below uses
    explicit little-endian words, so byte order is stable across hosts.
    """
    within_word = column % 64
    bit_in_word = 8 * (within_word // 8) + 7 - (within_word % 8)
    return np.uint64(1) << np.uint64(bit_in_word)


def save_checkpoint(path, rank, next_col):
    """Atomically save both independent elimination cursors."""
    tmp = path + ".tmp"
    with open(tmp, "wb") as stream:
        np.savez(
            stream,
            schema=np.array([CHECKPOINT_SCHEMA], dtype=np.int64),
            rank=np.array([rank], dtype=np.int64),
            next_col=np.array([next_col], dtype=np.int64),
        )
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(tmp, path)


def load_checkpoint(path):
    """Load a v2 checkpoint; reject legacy rank-only cursors as unsafe."""
    with np.load(path) as saved:
        required = {"schema", "rank", "next_col"}
        if not required.issubset(saved.files):
            raise RuntimeError(
                "Legacy rank-only checkpoint is unsafe: it does not store "
                "the next column cursor. Preserve it for audit, move it aside, "
                "regenerate B_padded.bin from the gen/build stages, then restart."
            )
        schema = int(saved["schema"][0])
        rank = int(saved["rank"][0])
        next_col = int(saved["next_col"][0])
    if schema != CHECKPOINT_SCHEMA:
        raise RuntimeError(f"Unsupported checkpoint schema {schema}")
    if not (0 <= rank <= next_col <= NPAIRS):
        raise RuntimeError(f"Invalid checkpoint cursors: rank={rank}, next_col={next_col}")
    return rank, next_col


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

# ---------------------------------------------------------------- gen
def gen():
    if os.path.exists(VEC_NPZ):
        log("gen: cached"); return
    G = sum(1 << i for i in (0, 1, 5, 6, 7, 9, 11))
    words = []
    for msg in range(1 << 12):
        w = 0
        for b in range(12):
            if (msg >> b) & 1: w ^= G << b
        if w.bit_count() & 1: w |= 1 << 23
        words.append(w)
    vecs, fam = [], []
    for i, j in itertools.combinations(range(24), 2):
        for si, sj in itertools.product((-4, 4), repeat=2):
            v = [0]*24; v[i], v[j] = si, sj; vecs.append(v); fam.append(0)
    for octad in (w for w in words if w.bit_count() == 8):
        sup = [i for i in range(24) if (octad >> i) & 1]
        for signs in itertools.product((-2, 2), repeat=8):
            if sum(1 for s in signs if s < 0) % 2: continue
            v = [0]*24
            for i, s in zip(sup, signs): v[i] = s
            vecs.append(v); fam.append(1)
    for special in range(24):
        base = [1]*24; base[special] = -3
        for w in words:
            vecs.append([-x if (w >> i) & 1 else x for i, x in enumerate(base)])
            fam.append(2)
    V = np.array(vecs, dtype=np.int16); fam = np.array(fam, dtype=np.int8)
    assert len(V) == 196560 and len(set(map(tuple, vecs))) == 196560
    # transversal: first nonzero coordinate positive
    firstnz = np.argmax(V != 0, axis=1)
    keep = V[np.arange(len(V)), firstnz] > 0
    T = V[keep]; Tf = fam[keep]
    assert len(T) == NPAIRS, len(T)
    # antipodal completeness: -T must be exactly the complement
    key = {tuple(v) for v in vecs}
    assert all(tuple(-v) in key for v in T)
    np.savez(VEC_NPZ, T=T, fam=Tf)
    log(f"gen: T saved ({len(T)} reps; families A/B/C = "
        f"{int((Tf==0).sum())}/{int((Tf==1).sum())}/{int((Tf==2).sum())})")

# ---------------------------------------------------------------- build
def build():
    gen()
    if os.path.exists(B_BIN) and os.path.getsize(B_BIN) == NPAIRS * (PADCOLS // 8):
        log("build: B cached"); return
    d = np.load(VEC_NPZ); T = d["T"].astype(np.float32)
    mm = np.memmap(B_BIN, dtype=np.uint8, mode="w+",
                   shape=(NPAIRS, PADCOLS // 8))
    rowB = np.empty(NPAIRS, dtype=np.int32)
    nnz = 0; block = 1024
    for s in range(0, NPAIRS, block):
        e = min(s + block, NPAIRS)
        G = T[s:e] @ T.T
        Gi = np.rint(G).astype(np.int32)
        mb = Gi == -16; mc = Gi == 16
        rb = mb.sum(axis=1); rc = mc.sum(axis=1)
        assert int((rb + rc).min()) == 4600 == int((rb + rc).max()), \
            f"row audit failed at block {s}: {(rb+rc).min()}..{(rb+rc).max()}"
        rowB[s:e] = rb; nnz += int(rb.sum())
        packed = np.packbits(mb, axis=1)
        pad = np.zeros((e - s, PADCOLS // 8 - packed.shape[1]), dtype=np.uint8)
        mm[s:e] = np.concatenate([packed, pad], axis=1)
        if s % (block * 16) == 0: log(f"build: rows {s}/{NPAIRS}")
    mm.flush()
    stats = dict(nonzeros=nnz, density=nnz / NPAIRS**2,
                 rowB_min=int(rowB.min()), rowB_max=int(rowB.max()),
                 rowB_mean=float(rowB.mean()))
    json.dump(stats, open(os.path.join(HERE, "B_stats.json"), "w"), indent=1)
    log(f"build: done {stats}")

# ---------------------------------------------------------------- probe
def candidates(T, Tf):
    c = {}
    for i in range(24):
        col = T[:, i].astype(np.int32)
        for v in (4, 3, 2, 1, -1, -2, -3, -4, 0):
            c[f"coord{i}=={v:+d}"] = col == v
        c[f"coord{i}>0"] = col > 0
        c[f"coord{i}<0"] = col < 0
        c[f"coord{i} odd"] = (col % 2) != 0
    for f, name in ((0, "A"), (1, "B"), (2, "C")):
        c[f"family=={name}"] = Tf == f
    c["all-ones"] = np.ones(len(T), dtype=bool)
    return c

def probe():
    build()
    d = np.load(VEC_NPZ); T, Tf = d["T"], d["fam"]
    B = np.memmap(B_BIN, dtype=np.uint64, mode="r", shape=(NPAIRS, WORDS))
    hits = []
    for name, mask in candidates(T, Tf).items():
        if mask.sum() == 0: continue
        acc = np.bitwise_xor.reduce(B[mask], axis=0)
        if not acc.any():
            hits.append((name, int(mask.sum())))
            log(f"probe: KERNEL HIT {name} (weight {int(mask.sum())})")
    # independence of hits (as vectors over T, Python-int bitsets)
    cand = candidates(T, Tf)
    basis_by_len = {}
    indep = 0
    for name, _ in hits:
        y = int.from_bytes(np.packbits(cand[name].astype(np.uint8)).tobytes(), "big")
        while y and y.bit_length() in basis_by_len:
            y ^= basis_by_len[y.bit_length()]
        if y:
            basis_by_len[y.bit_length()] = y
            indep += 1
    res = dict(hits=hits, independent_hits=indep,
               nullity_lower_bound=indep)
    json.dump(res, open(os.path.join(HERE, "kernel_probe.json"), "w"), indent=1)
    log(f"probe: done, {len(hits)} hits, {indep} independent")

# ---------------------------------------------------------------- subrank
def subrank(n=8192):
    build()
    B = np.memmap(B_BIN, dtype=np.uint8, mode="r",
                  shape=(NPAIRS, PADCOLS // 8))
    rows = []
    for i in range(n):
        rows.append(int.from_bytes(B[i, : n // 8].tobytes(), "big"))
    rank = 0
    for c in range(n):
        bit = 1 << (n - 1 - c)
        piv = next((r for r in range(rank, n) if rows[r] & bit), None)
        if piv is None: continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        for r in range(n):
            if r != rank and rows[r] & bit: rows[r] ^= rows[rank]
        rank += 1
        if rank % 1024 == 0: log(f"subrank: {rank}/{n}")
    res = dict(submatrix=n, rank=rank, nullity=n - rank)
    json.dump(res, open(os.path.join(HERE, "subrank.json"), "w"), indent=1)
    log(f"subrank: {res}")

# ---------------------------------------------------------------- eliminate
def eliminate():
    """Full GF(2) rank of B via bit-packed elimination, checkpointed.
    Sized for a workstation (Lucas's 5600X / 48 GB), not the VM."""
    build()
    CKPT = os.path.join(HERE, "elim_ckpt.npz")
    B = np.memmap(B_BIN, dtype="<u8", mode="r+", shape=(NPAIRS, WORDS))
    rank = 0
    next_col = 0
    if os.path.exists(CKPT):
        rank, next_col = load_checkpoint(CKPT)
        log(f"eliminate: resume at rank {rank}, column {next_col}")
    for c in range(next_col, NPAIRS):
        w, bit = c // 64, packed_column_mask(c)
        col = B[rank:, w]
        piv = np.argmax(col & bit != 0) if (col & bit != 0).any() else -1
        if piv < 0: continue
        piv += rank
        if piv != rank: B[[rank, piv]] = B[[piv, rank]]
        below = np.where((B[rank+1:, w] & bit) != 0)[0] + rank + 1
        if len(below):
            B[below] ^= B[rank]
        rank += 1
        if rank and rank % 512 == 0:
            B.flush()
            save_checkpoint(CKPT, rank, c + 1)
            log(f"eliminate: rank {rank} (next col {c + 1})")
    # Persist matrix pages before publishing the terminal cursor.
    B.flush()
    # Persist the terminal cursor too, including trailing zero-pivot columns.
    save_checkpoint(CKPT, rank, NPAIRS)
    res = dict(rank=rank, nullity=NPAIRS - rank, n=NPAIRS)
    json.dump(res, open(os.path.join(HERE, "rank_result.json"), "w"), indent=1)
    log(f"eliminate: DONE {res}")

if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "probe"
    {"gen": gen, "build": build, "probe": probe,
     "subrank": subrank, "eliminate": eliminate}[stage]()