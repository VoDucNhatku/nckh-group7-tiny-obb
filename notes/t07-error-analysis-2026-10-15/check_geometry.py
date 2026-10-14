# Re-check of the geometry and angle claims audited in C-19 (14-15/10 session errors E3-E5).
# Pure standard library; prints Monte Carlo estimates next to the closed-form bounds.
import math, random, sys
sys.stdout.reconfigure(encoding='utf-8')
random.seed(0)
s = 1.0
def count_pts(cx, cy, w, h, th):
    # closed rotated rectangle, lattice step s, count lattice points inside
    c, sn = math.cos(th), math.sin(th)
    R = math.hypot(w, h) / 2 + 1
    n = 0
    for i in range(math.floor(cx - R), math.ceil(cx + R) + 1):
        for j in range(math.floor(cy - R), math.ceil(cy + R) + 1):
            dx, dy = i - cx, j - cy
            u = dx * c + dy * sn
            v = -dx * sn + dy * c
            if abs(u) <= w / 2 + 1e-12 and abs(v) <= h / 2 + 1e-12:
                n += 1
    return n
# 1) equal-area counterexample, axis-aligned, uniform phase
T = 200000
def stats(w, h):
    z = 0; tot = 0
    for _ in range(T):
        n = count_pts(random.random(), random.random(), w, h, 0.0)
        tot += n; z += (n == 0)
    return tot / T, z / T
print('square s x s      E[N], P(N=0) =', stats(1.0, 1.0))
print('rect 2s x s/2     E[N], P(N=0) =', stats(2.0, 0.5))
# 2) sqrt2*s coverage: random pose, short side >= sqrt2
mn = 10**9
for _ in range(100000):
    w = math.sqrt(2) * (1 + random.random() * 2); h = math.sqrt(2)
    n = count_pts(random.random(), random.random(), w, h, random.random() * math.pi)
    mn = min(mn, n)
print('min count, short side = sqrt2*s, random pose:', mn)
# worst case: 45deg square side sqrt2 centred at cell centre
print('45deg sqrt2 square at cell centre (closed):', count_pts(0.5, 0.5, math.sqrt(2), math.sqrt(2), math.pi / 4))
print('45deg (sqrt2-1e-6) square at cell centre:', count_pts(0.5, 0.5, math.sqrt(2) - 1e-6, math.sqrt(2) - 1e-6, math.pi / 4))
# 3) angle bounds: L=10, delta=2
L, d = 10.0, 2.0
best_perp = 0; best_euc = 0
for _ in range(400000):
    t1 = random.uniform(-d, d); t2 = random.uniform(-d, d)
    a = abs(math.atan2(t2 - t1, L)); best_perp = max(best_perp, a)
    r1 = d * math.sqrt(random.random()); p1 = random.uniform(0, 2 * math.pi)
    r2 = d * math.sqrt(random.random()); p2 = random.uniform(0, 2 * math.pi)
    vx = L + r2 * math.cos(p2) - r1 * math.cos(p1); vy = r2 * math.sin(p2) - r1 * math.sin(p1)
    best_euc = max(best_euc, abs(math.atan2(vy, vx)))
# adversarial Euclidean: endpoints move opposite, tangent configuration
phi = math.asin(2 * d / L)
print('perp-only  MC max deg=%.3f  arctan(2d/L) deg=%.3f' % (math.degrees(best_perp), math.degrees(math.atan(2 * d / L))))
print('euclid     MC max deg=%.3f  asin(2d/L)   deg=%.3f' % (math.degrees(best_euc), math.degrees(phi)))
