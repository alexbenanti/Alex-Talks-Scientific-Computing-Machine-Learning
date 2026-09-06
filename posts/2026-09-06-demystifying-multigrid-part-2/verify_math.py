"""Check the post's formulas and solver: py verify_math.py."""

import ast
from pathlib import Path
import re

import numpy as np


source = Path(__file__).with_name("index.qmd").read_text(encoding="utf-8")
code = re.search(r"```\{python\}\n(.*?)\n```", source, re.S).group(1)
tree = ast.parse(code)
definitions = ast.Module(body=[node for node in tree.body
                              if isinstance(node, ast.FunctionDef)], type_ignores=[])
scope = {"np": np}
exec(compile(definitions, "post-solver", "exec"), scope)
hierarchy, v_cycle = scope["hierarchy"], scope["v_cycle"]

rng = np.random.default_rng(42)
for n in (4, 8, 16, 64):
    Alevels, Ps = hierarchy(n)
    A, P = Alevels[0], Ps[0]
    R = P.T
    N = n // 2
    ell = np.arange(1, n)
    coarse_ell = np.arange(1, N)
    G = np.eye(n - 1) - (2 / 3) * A / np.diag(A)[:, None]
    for j in range(1, n):
        v = np.sin(np.pi * j * ell / n)
        eigenvalue = 4 * n**2 * np.sin(np.pi * j / (2 * n))**2
        gamma = 1 - (4 / 3) * np.sin(np.pi * j / (2 * n))**2
        np.testing.assert_allclose(A @ v, eigenvalue * v, atol=2e-10)
        np.testing.assert_allclose(G @ v, gamma * v, atol=2e-13)
        if j >= N:
            assert abs(gamma) <= 1 / 3 + 1e-14
        injected = v[1::2]
        if j > N:
            alias = -np.sin(np.pi * (n - j) * coarse_ell / N)
            np.testing.assert_allclose(injected, alias, atol=1e-12)
        elif j == N:
            np.testing.assert_allclose(injected, 0, atol=1e-12)
        # Transpose restriction has a different amplitude from injection.
        np.testing.assert_allclose(R @ v,
                                   (1 + np.cos(np.pi * j / n)) * injected,
                                   atol=1e-12)

    coarse_values = rng.normal(size=N - 1)
    interpolated = np.interp(np.arange(1, n) / n, np.arange(N + 1) / N,
                             np.r_[0, coarse_values, 0])
    np.testing.assert_allclose(P @ coarse_values, interpolated)
    rediscretized = N**2 * (2 * np.eye(N - 1) - np.eye(N - 1, k=1)
                           - np.eye(N - 1, k=-1))
    np.testing.assert_allclose(R @ A @ P, 2 * rediscretized)
    np.testing.assert_allclose(0.5 * R @ A @ P, rediscretized)
    residual = rng.normal(size=n - 1)
    correction = P @ np.linalg.solve(R @ A @ P, R @ residual)
    full_weighting_correction = P @ np.linalg.solve(0.5 * R @ A @ P,
                                                   0.5 * R @ residual)
    np.testing.assert_allclose(correction, full_weighting_correction)
    Q = P @ np.linalg.solve(R @ A @ P, R @ A)
    np.testing.assert_allclose(Q @ Q, Q, atol=1e-13)
    np.testing.assert_allclose(Q @ P, P, atol=1e-13)
    np.testing.assert_allclose(Q.T @ A, A @ Q, atol=1e-10)
    np.testing.assert_allclose(R @ (residual - A @ correction), 0, atol=1e-12)
print("PASS: sine eigenpairs, Jacobi damping, aliasing, interpolation, RAP scaling,")
print("      correction scaling invariance, and Galerkin projection identities.")

# Check the numerical values used in both transfer illustrations.
_, Ps = hierarchy(8)
P = Ps[0]
c = np.array([1, 0.5, 1.5])
f = np.array([0.5, 1, 0.75, 0.5, 1, 1.5, 0.75])
np.testing.assert_allclose(P @ c, f)
np.testing.assert_allclose(P.T @ f, [1.625, 1.375, 2.375])

# Exercise arbitrary mixtures of modes, the one-unknown base case, and zero RHS.
for n in (2, 4, 8, 16, 64):
    matrices, transfers = hierarchy(n)
    b = rng.normal(size=n - 1)
    v = rng.normal(size=n - 1)
    for cycle in range(60):
        v = v_cycle(matrices, transfers, 0, b, v)
        relative = np.linalg.norm(b - matrices[0] @ v) / np.linalg.norm(b)
        if relative < 1e-10:
            break
    assert relative < 1e-10, (n, relative)
    np.testing.assert_allclose(v, np.linalg.solve(matrices[0], b),
                               rtol=1e-8, atol=1e-11)
    zero = np.zeros_like(b)
    np.testing.assert_array_equal(v_cycle(matrices, transfers, 0, zero, zero), zero)
    print(f"PASS: n={n:2d}, mixed-mode RHS, {cycle + 1} cycles, residual={relative:.2e}")

errors = []
for n in (16, 32, 64):
    matrices, transfers = hierarchy(n)
    x = np.arange(1, n) / n
    b = np.pi**2 * np.sin(np.pi * x)
    v = np.zeros_like(b)
    for cycle in range(50):
        v = v_cycle(matrices, transfers, 0, b, v)
        relative = np.linalg.norm(b - matrices[0] @ v) / np.linalg.norm(b)
        if relative < 1e-10:
            break
    assert relative < 1e-10
    exact_discrete = np.pi**2 / (4 * n**2 * np.sin(np.pi / (2 * n))**2) * np.sin(np.pi * x)
    np.testing.assert_allclose(v, exact_discrete, atol=1e-10, rtol=1e-10)
    errors.append(np.max(np.abs(v - np.sin(np.pi * x))))
    print(f"PASS: sine example n={n}, {cycle + 1} cycles, residual={relative:.2e}, error={errors[-1]:.2e}")
ratios = np.array(errors[:-1]) / errors[1:]
np.testing.assert_allclose(ratios, 4, rtol=0.01)
print("PASS: second-order discretization error; refinement ratios", ratios)
