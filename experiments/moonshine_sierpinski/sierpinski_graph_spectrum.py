"""Finite-stage Sierpinski gasket graph and combinatorial Laplacian audit."""
from math import copysign, sqrt

def edge(a, b):
    return (a, b) if a < b else (b, a)

def sierpinski_graph(stage):
    if not isinstance(stage, int) or stage < 0:
        raise ValueError("stage must be a non-negative integer")
    vertices = {(0, 0), (1, 0), (0, 1)}
    edges = {edge((0, 0), (1, 0)), edge((0, 0), (0, 1)), edge((1, 0), (0, 1))}
    for level in range(stage):
        side = 2**level
        transforms = (
            lambda x, y: (x, y),
            lambda x, y: (side + x, y),
            lambda x, y: (x, side + y),
        )
        next_vertices, next_edges = set(), set()
        for transform in transforms:
            for x, y in vertices:
                next_vertices.add(transform(x, y))
            for a, b in edges:
                next_edges.add(edge(transform(*a), transform(*b)))
        vertices, edges = next_vertices, next_edges
    return vertices, edges

def jacobi_eigenvalues(matrix, tolerance=1e-12):
    """Eigenvalues of a real symmetric matrix using cyclic Jacobi sweeps."""
    n = len(matrix)
    a = [row[:] for row in matrix]
    for _ in range(50):
        largest = max((abs(a[p][q]) for p in range(n) for q in range(p + 1, n)), default=0.0)
        if largest <= tolerance:
            break
        for p in range(n):
            for q in range(p + 1, n):
                apq = a[p][q]
                if abs(apq) <= tolerance:
                    continue
                tau = (a[q][q] - a[p][p]) / (2.0 * apq)
                t = copysign(1.0, tau) / (abs(tau) + sqrt(1.0 + tau*tau)) if tau else 1.0
                c = 1.0 / sqrt(1.0 + t*t)
                s = t*c
                app, aqq = a[p][p], a[q][q]
                a[p][p] = app - t*apq
                a[q][q] = aqq + t*apq
                a[p][q] = a[q][p] = 0.0
                for r in range(n):
                    if r == p or r == q:
                        continue
                    arp, arq = a[r][p], a[r][q]
                    a[r][p] = a[p][r] = c*arp - s*arq
                    a[r][q] = a[q][r] = s*arp + c*arq
    else:
        residual = max((abs(a[p][q]) for p in range(n) for q in range(p + 1, n)), default=0.0)
        if residual > tolerance:
            raise RuntimeError("Jacobi diagonalization did not converge within 50 sweeps")
    return sorted(a[i][i] for i in range(n))

def audit_sierpinski_stage(stage, max_spectral_vertices=64):
    vertices, edges = sierpinski_graph(stage)
    ordered = sorted(vertices)
    index = {point: i for i, point in enumerate(ordered)}
    adjacency = [set() for _ in ordered]
    for a, b in edges:
        i, j = index[a], index[b]
        adjacency[i].add(j)
        adjacency[j].add(i)
    degrees = [len(row) for row in adjacency]
    n = len(vertices)
    result = {
        "stage": stage, "vertices": n, "edges": len(edges),
        "expected_vertices": (3**(stage+1) + 3)//2,
        "expected_edges": 3**(stage+1),
        "degree_histogram": {str(d): degrees.count(d) for d in sorted(set(degrees))},
        "laplacian_trace": sum(degrees),
        "laplacian_trace_squared": sum(d*d + d for d in degrees),
        "spectral_status": "not_computed", "laplacian_eigenvalues": None,
    }
    if n != result["expected_vertices"] or len(edges) != result["expected_edges"]:
        raise AssertionError("Sierpinski graph count recurrence failed")
    if n <= max_spectral_vertices:
        laplacian = [[0.0] * n for _ in range(n)]
        for i, neighbors in enumerate(adjacency):
            laplacian[i][i] = float(degrees[i])
            for j in neighbors:
                laplacian[i][j] = -1.0
        eigenvalues = jacobi_eigenvalues(laplacian)
        if abs(sum(eigenvalues) - result["laplacian_trace"]) > 1e-7:
            raise AssertionError("spectral trace does not match degree sum")
        if abs(eigenvalues[0]) > 1e-8:
            raise AssertionError("connected gasket graph must have one zero eigenvalue")
        result["spectral_status"] = "computed_jacobi_float"
        result["laplacian_eigenvalues"] = [round(x, 12) for x in eigenvalues]
    return result

def run_stages(max_stage=3):
    if not isinstance(max_stage, int) or max_stage < 0:
        raise ValueError("max_stage must be a non-negative integer")
    return [audit_sierpinski_stage(stage) for stage in range(max_stage + 1)]

if __name__ == "__main__":
    import json
    print(json.dumps(run_stages(), indent=2, sort_keys=True))
