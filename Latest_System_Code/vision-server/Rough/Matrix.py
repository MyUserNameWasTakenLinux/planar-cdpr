import math

class Mat:
    # Row major order
    elems = None
    n_rows = 0
    n_columns = 0
    # elems is a list of lists with each list within the list being a single row
    def __init__(self, elems):
        self.elems = elems
        self.n_rows = len(elems)
        self.n_columns = len(elems[0])
    # prints out the matrix in a pretty format
    def display(self):
        for i in range(self.n_rows):
            for j in range(self.n_columns):
                print(self.elems[i][j], end=' ')
            print("")
    # matrix addition
    def __add__(self, other):
        m_data = []
        for i in range(self.n_rows):
            row = []
            for j in range(self.n_columns):
                row.append(self.elems[i][j] + other.elems[i][j])
            m_data.append(row)
        result = Mat(m_data)
        return result
    # matrix addition
    def __radd__(self, other):
        m_data = []
        for i in range(self.n_rows):
            row = []
            for j in range(self.n_columns):
                row.append(self.elems[i][j] + other.elems[i][j])
            m_data.append(row)
        result = Mat(m_data)
        return result
    # matrix subtraction
    def __sub__(self, other):
        m_data = []
        for i in range(self.n_rows):
            row = []
            for j in range(self.n_columns):
                row.append(self.elems[i][j] - other.elems[i][j])
            m_data.append(row)
        result = Mat(m_data)
        return result
    # matrix subtraction
    def __rsub__(self, other):
        m_data = []
        for i in range(self.n_rows):
            row = []
            for j in range(self.n_columns):
                row.append(-self.elems[i][j] + other.elems[i][j])
            m_data.append(row)
        result = Mat(m_data)
        return result
    # matrix multiplication
    def __mul__(self, other):
        m_data = []
        for i in range(self.n_rows):
            row = []
            for j in range(other.n_columns):
                el_result = 0
                for k in range(self.n_columns):
                    el_result += self.elems[i][k] * other.elems[k][j]
                row.append(el_result)
            m_data.append(row)
        return Mat(m_data)
    # matrix multiplication
    def __rmul__(self, other):
        m_data = []
        for i in range(self.n_rows):
            row = []
            for j in range(self.n_columns):
                el_result = 0
                for k in range(self.n_columns):
                    el_result += self.elems[i][k] * other.elems[k][j]
                row.append(el_result)
            m_data.append(row)
        return Mat(m_data)
    def transpose(self):
        m_data = []
        for j in range(self.n_columns):
            row = []
            for i in range(self.n_rows):
                row.append(self.elems[i][j])
            m_data.append(row)
        return Mat(m_data)
    # Only works for vectors
    def norm(self):
        t = 0
        for i in range(self.n_rows):
            t += (self.elems[i][0])**2
        return math.sqrt(t)


# The arugments are two column vectors
# Returns the dot product as a float
def dot_product(v, w):
    result = v.transpose() * w
    return result.elems[0][0]

# Converts v to homogenous
def to_homogenous(v):
    w_data = v.elems.copy()
    new_row = [1]
    w_data.append(new_row)
    return Mat(w_data)

# Converts from Homogenous
def from_homogenous(v):
    w_data = v.elems.copy()
    w_data.pop()
    return Mat(w_data)

# Create an nxm matrix with values f
def initalize_from(n, m, f):
    m_data = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(f)
        m_data.append(row)
    
    return Mat(m_data)

def identity_mat(n):
    I = initalize_from(n, n, 0)
    for i in range(n):
        I.elems[i][i] = 1
    return I

# Returns the acute angle (in degrees) between the two vectors v and w
def get_angle(v, w):
    t = (dot_product(v, w) / (v.norm() * w.norm()))
    return math.degrees(math.acos(t))


# Returns the LU decomposition of B
def LU_decomposition(B):
    A = Mat(B.elems.copy())
    n = A.n_columns
    M = initalize_from(n, n, 0.0)
    
    for k in range(n - 1):
        if(A.elems[k][k] == 0):
            return (initalize_from(n, n, 0), initalize_from(n, n, 0));
        for i in range(k + 1, n):
            M.elems[i][k] = A.elems[i][k] / A.elems[k][k]
        for j in range(k + 1, n):
            for  i in range(k + 1, n):
                A.elems[i][j] = A.elems[i][j] - (M.elems[i][k] * A.elems[k][j])
    
    L = identity_mat(n)
    for j in range(n):
        for i in range(j + 1, n):
            L.elems[i][j] = M.elems[i][j]
    
    U = initalize_from(n, n, 0)
    for j in range(n):
        for i in reversed(range(0, j + 1)):
            U.elems[i][j] = A.elems[i][j]
    
    return (L, U)

# Forward substitution
def forward_sub(L : Mat, b : Mat):
    n = b.n_rows
    x = initalize_from(n, 1, 0)
    b_copy = Mat(b.elems.copy())

    for j in range(n):
        if(L.elems[j][j] == 0):
            print("ERROR")
            break
        x.elems[j][0] = b_copy.elems[j][0] / L.elems[j][j]
        for i in range(j + 1, n):
            b_copy.elems[i][0] = b_copy.elems[i][0] - L.elems[i][j] * x.elems[j][0]
    
    return x

# Backward substitution
def backward_sub(U : Mat, b : Mat):
    n = b.n_rows
    x = initalize_from(n, 1, 0)
    b_copy = Mat(b.elems.copy())

    for j in reversed(range(0, n)):
        if(U.elems[j][j] == 0):
            print("ERROR")
            break
        x.elems[j][0] = b_copy.elems[j][0] / U.elems[j][j]
        for i in range(j):
            b_copy.elems[i][0] = b_copy.elems[i][0] - U.elems[i][j] * x.elems[j][0]
    
    return x