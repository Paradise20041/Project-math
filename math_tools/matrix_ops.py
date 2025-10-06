import numpy as np

def parse_matrix(matrix_str):
    try:
        return np.array(eval(matrix_str))
    except:
        raise ValueError("Формат: [[1,2],[3,4]]")

def matrix_add(A_str, B_str):
    A = parse_matrix(A_str)
    B = parse_matrix(B_str)
    return np.add(A, B).tolist()

def matrix_mult(A_str, B_str):
    A = parse_matrix(A_str)
    B = parse_matrix(B_str)
    return np.dot(A, B).tolist()

def matrix_det(A_str):
    A = parse_matrix(A_str)
    if A.shape[0] != A.shape[1]:
        raise ValueError("Только для квадратных матриц")
    return float(np.linalg.det(A))

def matrix_inv(A_str):
    A = parse_matrix(A_str)
    return np.linalg.inv(A).tolist()