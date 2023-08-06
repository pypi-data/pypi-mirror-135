# distutils: language = c++

cdef extern from "stdlib.h":
    ctypedef void const_void "const void"
    void qsort(void *base, int nmemb, int size,
            int(*compar)(const void *, const void *)) nogil

from libcpp cimport bool
from libc.stdlib cimport malloc, free
import cython

from libc.math cimport exp
from libc.math cimport pow as cpow

from tqdm import tqdm

import numpy as np
cimport numpy as np

from cpython cimport array
import array      

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef void count_diff_desc(int[:,:] A,
               int[:,:] out):
    cdef Py_ssize_t j, i_asc, i
    
    cdef int n = A.shape[0]
    cdef int d = A.shape[1]
    
    for i_asc in range(n - 1):
        i = n - 2 - i_asc
        for j in range(d):
            if A[i,j] == A[i+1, j]:
                if j == 0:
                    out[i,j] = out[i+1,j] + 1
                elif out[i,j-1] > 1:
                    out[i,j] = out[i+1,j] + 1  

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef void count_diff_asc(int[:,:] A,
                          int[:,:] out):
    cdef Py_ssize_t j, i
    
    cdef int n = A.shape[0]
    cdef int d = A.shape[1]
    
    for i in range(1, n):
        for j in range(d):
            if A[i,j] == A[i-1, j]:
                if j == 0:
                    out[i,j] = out[i-1,j] + 1
                elif out[i,j-1] > 1:
                    out[i,j] = out[i-1,j] + 1


@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
cdef int *** sparse(int[:,:] U,
                    int[:,:] U_diff_desc,
                    int[:,:] U_diff_one_side,
                    int *S_shape):
    cdef Py_ssize_t i_U, i_S, j, j_asc
    
    cdef int n = U.shape[0]
    cdef int d = U.shape[1]
        
    cdef int ***S = <int ***> malloc(d *sizeof(int **))
    
    for j in range(d):
        S[j] = <int **> malloc(S_shape[j] * sizeof(int *))
    
    for i_U in range(n):
        S[d-1][i_U] = <int *> malloc(2 * sizeof(int))
        S[d-1][i_U][0] = U[i_U, d-1]
        S[d-1][i_U][1] = i_U
    
    for j in range(d-1):
        S[j][0] = <int *> malloc(2 * sizeof(int))
        S[j][0][0] = U[0, j]
        S[j][0][1] = 0
    
    for j in range(d-1):
        i_U = 0
        for i_S in range(1, S_shape[j]):
            S[j][i_S] = <int *> malloc(2 * sizeof(int))
            
            S[j][i_S][1] = S[j][i_S - 1][1] + U_diff_one_side[i_U, j]
            
            i_U = i_U + U_diff_desc[i_U, j]
            
            S[j][i_S][0] = U[i_U, j]                
    
    return(S)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
cdef int [:,:] count_one_side(int[:,:] U_diff_desc):
    cdef Py_ssize_t i, j, i_asc
    
    cdef int n = U_diff_desc.shape[0]
    cdef int d = U_diff_desc.shape[1]
    cdef int [:,:] U_diff_one_side = np.zeros((n, d-1), dtype=np.intc)
    
    cdef int cnt
    
    for j in range(d-1):
        cnt = 0
        for i_asc in range(n):
            i = n - 1 - i_asc
            if U_diff_desc[i, j] == 1:
                cnt = 0
                
            if U_diff_desc[i, j+1] == 1:
                cnt = cnt + 1
            
            U_diff_one_side[i, j] = cnt
    
    return(U_diff_one_side)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
cdef bool search_first_U(int ***S, 
                         int *S_shape,
                         int[:,:] U_diff_asc,
                         int * s,
                         int d,
                         int *target,
                         int j_start):
    cdef Py_ssize_t j
    
    cdef int a
    cdef int b
    
    for j in range(j_start, d):
        if j == 0:
            a = 0
            b = S_shape[0]
        
        else:
            a = S[j-1][s[j-1]][1]
            if s[j-1] + 1 < S_shape[j-1]:
                b = S[j-1][s[j-1] + 1][1]
            else:
                b = S_shape[j]
            
        s[j] = binary_search(L = S[j],
                             x = target[j],
                             a = a,
                             b = b)
        
        if s[j] == -1:
            return(next_s(S = S, 
                          S_shape=S_shape,
                          U_diff_asc=U_diff_asc,
                          d = d,
                          s = s,
                          j_max = j-1))
    
    # for j in range(d):
    #     if S[j][s[j]][0] < target[j]:
    #         return(next_s(S = S, 
    #                       S_shape=S_shape,
    #                       U_diff_asc=U_diff_asc,
    #                       d = d,
    #                       s = s,
    #                       j_max = j-1))
    
    return(True)
    

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
cdef int binary_search(int **L,
                       int x,
                       int a,
                       int b):
    cdef int m
    
    if x < L[a][0]:
        return(a)
    
    if x > L[b-1][0]:
        return(-1)
    
    while a < b:
        m = <int> (a + b) / 2
        
        if L[m][0] < x:
            a = m + 1
        else:
            b = m
    
    return(a)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
cdef bool next_s(int ***S, 
                 int *S_shape,
                 int [:,:] U_diff_asc,
                 int d,
                 int *s,
                 int j_max):
    cdef Py_ssize_t j    
    cdef int i_U = s[j_max] + 1
    
    if j_max < 0:
        return(False)
    
    if i_U >= S_shape[j_max]:
        s[j_max] = -1
        return(False)
        
    for j in range(j_max, d):
        i_U = S[j][i_U][1]
    
    
    for j in range(j_max + 1):
        if U_diff_asc[i_U, j] == 1:
            s[j] = s[j] + 1
    
    for j in range(j_max + 1, d):
        s[j] = S[j-1][s[j-1]][1]
    
    return(True)
        
@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
cdef int * get_S_shape(int[:,:] U_diff_desc, 
                       int n_U,
                       int d):
    cdef Py_ssize_t j
    
    cdef int *S_shape = <int *> malloc(d * sizeof(int))
    
    for j in range(d):
        S_shape[j] = 0
        
        for i_U in range(n_U):
            if U_diff_desc[i_U, j] == 1:
                S_shape[j] = S_shape[j] + 1
    return(S_shape)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef double [:] set_estimation(int[:,:] Z_diff_asc,
                                int[:] Z_indices,
                                double[:] g):
    cdef Py_ssize_t i_Z, i_g
    cdef int n_Z = Z_diff_asc.shape[0]
    cdef int d = Z_diff_asc.shape[1]
    
    cdef double [:] f = np.zeros(n_Z, dtype=np.double)
    
    i_g = 0
    for i_Z in range(n_Z):
        if Z_diff_asc[i_Z, d-1] == 1:
            f[Z_indices[i_Z]] = g[i_g]
            i_g = i_g + 1
        else:
            f[Z_indices[i_Z]] = g[i_g]
    
    return(f)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)  # non check division 
@cython.cdivision(True) # modulo operator (%)
cpdef double [:] merge(int[:, :] U, 
                       int[:, :] U_diff_asc,
                       int[:, :] U_diff_desc,
                       double[:] nu, 
                       int[:, :] Z,
                       int q,
                       double h,
                       int kernel_id,
                       double dx,
                       int verbose=0):
    cdef Py_ssize_t i_U, i_Z, j, k
    
    cdef int n_U = U.shape[0]
    cdef int d = U.shape[1]
    cdef int n_Z = Z.shape[0]
    
    cdef int margin = (q - 1) / 2
    
    cdef double [:] f = np.zeros(n_Z, dtype=np.double)
                
    cdef int *S_shape = get_S_shape(U_diff_desc,
                                    n_U,
                                    d)
    
    cdef int [:,:] U_diff_one_side = count_one_side(U_diff_desc=U_diff_desc)
    
    cdef int ***S = sparse(U=U,
                           U_diff_desc=U_diff_desc,
                           U_diff_one_side = U_diff_one_side,
                           S_shape=S_shape)
    
    if verbose > 0:
        pbar = tqdm(total=n_Z)
        
    
    f[0] = estimate(S=S, 
                    S_shape=S_shape, 
                    U_diff_asc=U_diff_asc, 
                    nu=nu,
                    Z=Z, 
                    i_Z=0, 
                    margin=margin,
                    d=d,
                    h=h,
                    dx=dx,
                    kernel_id=kernel_id)
    
    for i_Z in range(0, n_Z):
        if verbose > 0:
            if i_Z % (n_Z / 100) == 0:
                pbar.update(<int> n_Z / 100)
                
        f[i_Z] = estimate(S=S, 
                          S_shape=S_shape, 
                          U_diff_asc=U_diff_asc, 
                          nu=nu,
                          Z=Z, 
                          i_Z=i_Z, 
                          margin=margin,
                          d=d,
                          h=h,
                          dx=dx,
                          kernel_id=kernel_id)
    
    for j in range(d):
        for i_U in range(S_shape[j]):
            free(S[j][i_U])
        free(S[j])
    free(S)
    
    free(S_shape)
    
    if verbose > 0:
        pbar.close()
    
    return(f)

@cython.boundscheck(False)  # Deactivate bounds checking.
@cython.wraparound(False)   # Deactivate negative indexing.
@cython.cdivision(True)  # non check division 
cdef double estimate(int ***S, 
              int *S_shape, 
              int[:,:] U_diff_asc, 
              double[:] nu,
              int[:,:] Z, 
              int i_Z, 
              int margin,
              int d,
              double h,
              double dx,
              int kernel_id):
    cdef Py_ssize_t j
    cdef double dist_sq, est, contrib
    
    cdef bool trigger_search_U
    cdef int *target = <int *> malloc(d * sizeof(int))
    cdef int *s = <int *> malloc(d * sizeof(int))
    
    est = 0.0
    
    for j in range(d):
        target[j] = Z[i_Z, j] - margin
    
    trigger_search_U =  search_first_U(S = S,
                                       S_shape = S_shape,
                                       U_diff_asc = U_diff_asc,
                                       s = s,
                                       d = d,
                                       target = target,
                                       j_start=0)
    
    while trigger_search_U:
        for j in range(d):
            if S[j][s[j]][0] - margin > Z[i_Z, j]:
                # U is too high
                # the column before is incremented
                trigger_search_U = next_s(S = S, 
                                          S_shape=S_shape,
                                          U_diff_asc=U_diff_asc,
                                          d = d,
                                          s = s,
                                          j_max = j-1)
                break
            
            elif S[j][s[j]][0] + margin < Z[i_Z, j]:
                # U is too low
                # let's search above
                # if nothing is found, the column before is incremented
                trigger_search_U = search_first_U(S = S,
                                                   S_shape = S_shape,
                                                   U_diff_asc = U_diff_asc,
                                                   s = s,
                                                   d = d,
                                                   target = target,
                                                   j_start=j)
                break
        else:
            # U is good for Z !
            # here it is possible to set another type of kernel
            contrib = nu[S[d-1][s[d-1]][1]]
            
            if kernel_id == 0:
                pass
                
            elif kernel_id == 1:
                
                dist_sq = 0
                for j in range(d):
                    dist_sq = dist_sq + cpow(Z[i_Z, j] - S[j][s[j]][0], 2.0)
                dist_sq = dist_sq * cpow(dx, 2.0)
                
                contrib = contrib * exp(-dist_sq / cpow(h,2.0) / 2)
            
            est = est + contrib
                            
            # then, next U
            trigger_search_U = next_s(S = S, 
                                      S_shape=S_shape,
                                      U_diff_asc=U_diff_asc,
                                      d = d,
                                      s = s,
                                      j_max = d-1)
    
    free(s)
    free(target)
    return(est)