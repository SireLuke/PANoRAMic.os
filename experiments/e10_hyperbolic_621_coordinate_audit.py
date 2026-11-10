#!/usr/bin/env python3
"""Exact Lorentzian coordinate realization of the E10 Coxeter simplex."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations
import json

def gram_from_arms(arms=(6, 2, 1)):
    n=1+sum(arms); a=[[0]*n for _ in range(n)]; cursor=1
    for length in arms:
        prev=0
        for _ in range(length):
            a[prev][cursor]=a[cursor][prev]=1; prev,cursor=cursor,cursor+1
    return [[Q(int(i==j))-Q(a[i][j],2) for j in range(n)] for i in range(n)]

def determinant(matrix):
    w=[list(map(Q,row)) for row in matrix]; n=len(w); out=Q(1)
    for c in range(n):
        p=next((r for r in range(c,n) if w[r][c]),None)
        if p is None:return Q(0)
        if p!=c:w[c],w[p]=w[p],w[c];out=-out
        x=w[c][c];out*=x
        for r in range(c+1,n):
            f=w[r][c]/x
            for j in range(c+1,n):w[r][j]-=f*w[c][j]
    return out

def inverse(matrix):
    n=len(matrix); w=[list(map(Q,row))+[Q(int(i==j)) for j in range(n)] for i,row in enumerate(matrix)]
    for c in range(n):
        p=next(r for r in range(c,n) if w[r][c]);w[c],w[p]=w[p],w[c]
        x=w[c][c];w[c]=[v/x for v in w[c]]
        for r in range(n):
            if r!=c:
                x=w[r][c];w[r]=[a-x*b for a,b in zip(w[r],w[c])]
    return [r[n:] for r in w]

def transpose(a):return [list(x) for x in zip(*a)]
def matmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def identity(n):return [[Q(int(i==j)) for j in range(n)] for i in range(n)]
def diagonal_matrix(v):return [[v[i] if i==j else Q(0) for j in range(len(v))] for i in range(len(v))]

def ldl(matrix):
    n=len(matrix); lower=identity(n); diagonal=[]
    for k in range(n):
        pivot=matrix[k][k]-sum(lower[k][j]**2*diagonal[j] for j in range(k))
        if pivot==0:raise ArithmeticError("zero LDL pivot")
        diagonal.append(pivot)
        for i in range(k+1,n):
            numerator=matrix[i][k]-sum(lower[i][j]*lower[k][j]*diagonal[j] for j in range(k))
            lower[i][k]=numerator/pivot
    return lower,diagonal

def principal_minor_counts(matrix):
    counts=Counter()
    for size in range(1,len(matrix)+1):
        for ids in combinations(range(len(matrix)),size):
            value=determinant([[matrix[i][j] for j in ids] for i in ids])
            counts["zero" if value==0 else "positive" if value>0 else "negative"]+=1
    return counts

def run_audit():
    g=gram_from_arms();n=len(g);lower,d=ldl(g);metric=diagonal_matrix(d)
    assert matmul(matmul(lower,metric),transpose(lower))==g
    signature=(sum(x>0 for x in d),sum(x<0 for x in d),sum(x==0 for x in d))
    assert signature==(9,1,0) and determinant(g)==Q(-1,1024)
    dual=matmul(diagonal_matrix([1/x for x in d]),inverse(lower))
    assert matmul(matmul(lower,metric),dual)==identity(n)
    dual_gram=matmul(matmul(transpose(dual),metric),dual)
    ginv=inverse(g);assert dual_gram==ginv
    norms=[dual_gram[i][i] for i in range(n)];ideal=6
    assert [i for i,x in enumerate(norms) if x==0]==[ideal]
    assert all(x<0 for i,x in enumerate(norms) if i!=ideal)
    time_coords=[dual[-1][i] for i in range(n)]
    assert all(x<0 for x in time_coords)
    assert all(ginv[i][j]<0 for i in range(n) for j in range(n) if i!=j)

    reflections=[]
    for i in range(n):
        root=lower[i]
        r=[[Q(int(a==b))-2*root[a]*root[b]*d[b] for b in range(n)] for a in range(n)]
        reflections.append(r)
        assert matmul(r,r)==identity(n)
        assert matmul(matmul(transpose(r),metric),r)==metric
    adjacent=commuting=0
    for i,j in combinations(range(n),2):
        rij=matmul(reflections[i],reflections[j])
        if g[i][j]==Q(-1,2):
            assert matmul(matmul(rij,rij),rij)==identity(n);adjacent+=1
        else:
            assert rij==matmul(reflections[j],reflections[i]);commuting+=1
    assert (adjacent,commuting)==(9,36)

    keep=[i for i in range(n) if i!=ideal]
    affine=[[g[i][j] for j in keep] for i in keep]
    minors=principal_minor_counts(affine)
    assert minors==Counter({"positive":510,"zero":1})
    marks=[Q(6),Q(5),Q(4),Q(3),Q(2),Q(1),Q(4),Q(2),Q(3)]
    assert [sum(affine[i][j]*marks[j] for j in range(9)) for i in range(9)]==[Q(0)]*9
    return {
        "status":"PASS","lorentzian_metric_diagonal":[str(x) for x in d],
        "gram_signature":signature,"gram_determinant":str(determinant(g)),
        "dual_vertex_norms":[str(x) for x in norms],"finite_vertex_count":9,
        "ideal_vertex_count":1,"ideal_vertex_node":ideal,
        "all_vertex_rays_same_time_cone":True,"lorentz_reflections":10,
        "reflection_metric_preservation_checks":10,
        "coxeter_relations":{"involutions":10,"adjacent_order_three":adjacent,"nonadjacent_commutations":commuting,"total":55},
        "ideal_link":{"type":"affine E8 (also called E9 in the E10 vertex-link ladder)",
                      "principal_minor_counts":dict(minors),
                      "primitive_null_root_marks":[str(x) for x in marks]},
        "scope":"Exact Lorentzian coordinate realization of the E10 Coxeter simplex and its ideal affine-E8 link. This does not yet construct the full hyperbolic 6_21 honeycomb or its Wythoffian cells."
    }

if __name__=="__main__":print(json.dumps(run_audit(),indent=2,sort_keys=True))
