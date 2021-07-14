import numpy as np 
from scipy import sparse

matrix = np.array([[0,0],[0,1],[3,0]])
print(matrix)

matrix_sparse = sparse.csr_matrix(matrix) #remove zeros to reduce computation time
print(matrix_sparse)