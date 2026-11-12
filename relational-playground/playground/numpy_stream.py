"""numpy.random.default_rng(seed), replayed in the standard library.

SeedSequence -> PCG64 (XSL-RR 128/64) -> random() and integers(n). Written so
the original forest runs (which draw from numpy) can be ported draw for draw
without numpy at runtime and without multi-megabyte draw fixtures.

Trusted only as far as it is checked: fixtures/numpy_stream_check.json holds
numpy's own output for an interleaved call pattern, with the numpy version that
produced it, and tests/test_numpy_stream.py compares this module against it
value for value. Covered calls: random(), integers(n) for 0 < n <= 2**32.
Anything else numpy offers is not here and raises AttributeError.
"""
M32, M64, M128 = (1 << 32) - 1, (1 << 64) - 1, (1 << 128) - 1
_MULT = 0x2360ED051FC65DA44385DF649FCCF645


def _seed_words(seed, n_words):
    """numpy SeedSequence(seed).generate_state(n_words, uint32)."""
    if seed < 0:
        raise ValueError("seed must be >= 0")
    ent = []
    while True:
        ent.append(seed & M32)
        seed >>= 32
        if not seed:
            break
    hc = [0x43B0D7E5]

    def hashmix(v):
        v ^= hc[0]
        hc[0] = (hc[0] * 0x931E8875) & M32
        v = (v * hc[0]) & M32
        return v ^ (v >> 16)

    def mix(x, y):
        r = (0xCA01F9DD * x - 0x4973F715 * y) & M32
        return r ^ (r >> 16)

    pool = [hashmix(ent[i] if i < len(ent) else 0) for i in range(4)]
    for i in range(4):
        for j in range(4):
            if i != j:
                pool[j] = mix(pool[j], hashmix(pool[i]))
    for k in range(4, len(ent)):
        for j in range(4):
            pool[j] = mix(pool[j], hashmix(ent[k]))
    hb, out = 0x8B51F9DD, []
    for i in range(n_words):
        v = pool[i % 4] ^ hb
        hb = (hb * 0x58F38DED) & M32
        v = (v * hb) & M32
        out.append(v ^ (v >> 16))
    return out


class Generator:
    def __init__(self, seed):
        w = _seed_words(seed, 8)
        q = [w[2 * i] | (w[2 * i + 1] << 32) for i in range(4)]
        initstate, initseq = (q[0] << 64) | q[1], (q[2] << 64) | q[3]
        self.inc = ((initseq << 1) | 1) & M128
        self.state = 0
        self._step()
        self.state = (self.state + initstate) & M128
        self._step()
        self._has32, self._buf32 = False, 0
        self.seed = seed

    def _step(self):
        self.state = (self.state * _MULT + self.inc) & M128

    def _next64(self):
        self._step()
        s = self.state
        x, rot = ((s >> 64) ^ s) & M64, s >> 122
        return ((x >> rot) | (x << ((64 - rot) & 63))) & M64

    def _next32(self):
        if self._has32:
            self._has32 = False
            return self._buf32
        v = self._next64()
        self._has32, self._buf32 = True, v >> 32
        return v & M32

    def random(self):
        return (self._next64() >> 11) * (1.0 / 9007199254740992.0)

    def integers(self, n):
        """Uniform integer in [0, n): numpy's Lemire rejection on 32-bit draws."""
        if not 0 < n <= 1 << 32:
            raise ValueError("integers(n): 0 < n <= 2**32 only")
        rng = n - 1
        if rng == 0:
            return 0
        if rng == M32:
            return self._next32()
        m = self._next32() * n
        left = m & M32
        if left < n:
            thr = (M32 - rng) % n
            while left < thr:
                m = self._next32() * n
                left = m & M32
        return m >> 32


def default_rng(seed):
    return Generator(seed)
