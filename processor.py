def get_matrix(number):
    """ Returns a list containing a matrix of selected size and content.

    Receives a string with numerical descriptor as parameter (e.g., "first ", "second ", etc.)
    Asks user to input matrix size, returns empty list if input isn't exactly two integers that
    are greater than zero.
    Asks user to input matrix, returns empty list if input for each line isn't a number of
    floats and/or integers equal to second specified matrix dimension.
    """
    dimensions = input("Enter size of " + number + "matrix: ").split()
    if len(dimensions) != 2:
        return []
    try:
        m = int(dimensions[0])
        n = int(dimensions[1])
    except ValueError:
        return []
    matrix = []
    if m > 0 and n > 0:
        print("Enter " + number + "matrix:")
        for i in range(m):
            row_input = input().split()
            if len(row_input) != n:
                return []
            row = []
            for j in range(n):
                if "." in row_input[j]:
                    try:
                        row.append(float(row_input[j]))
                    except ValueError:
                        return []
                else:
                    try:
                        row.append(int(row_input[j]))
                    except ValueError:
                        return []
            matrix.append(row)
    return matrix


def add_matrices(mat1, mat2):
    """ Adds two matrices, returns empty list if matrices are of different size. """

    matrix = mat1[:]
    for i in range(len(matrix)):
        if len(matrix[i]) != len(mat2[i]):
            return []
        for j in range(len(matrix[i])):
            matrix[i][j] += mat2[i][j]
    return matrix


def multiply_matrix(mat, mult):
    """ Multiplies matrix by constant, returns empty list if invalid constant. """

    try:
        if "." in mult:
            mult = float(mult)
        else:
            mult = int(mult)
    except ValueError:
        return []
    matrix = mat[:]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] *= mult
    return matrix


def multiply_matrices(mat1, mat2):
    """ Multiplies two matrices, returns empty list if matrices are incompatible. """

    if len(mat1[0]) != len(mat2):
        return []
    matrix = []
    for row in range(len(mat1)):
        matrix.append([])
        for col in range(len(mat2[0])):
            matrix[row].append(calculate_cell(mat1, mat2, row, col))
    return matrix


def calculate_cell(mat1, mat2, row, col):
    """ Performs all multiplications for one matrix cell. """

    result = 0
    for i in range(len(mat1[0])):
        result += mat1[row][i] * mat2[i][col]
    return result


def transpose_main(mat):
    """ Performs matrix transposition along main diagonal. """

    matrix = get_empty_matrix(mat, True)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = mat[j][i]
    return matrix


def transpose_side(mat):
    """ Performs matrix transposition along side diagonal. """

    matrix = get_empty_matrix(mat, True)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = mat[len(mat) - j - 1][len(mat[0]) - i - 1]
    return matrix


def transpose_vertical(mat):
    """ Performs vertical matrix transposition. """

    matrix = get_empty_matrix(mat)
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            matrix[i][j] = mat[i][len(mat[0]) - 1 - j]
    return matrix


def transpose_horizontal(mat):
    """ Performs horizontal matrix transposition. """

    matrix = get_empty_matrix(mat)
    for i in range(len(mat)):
        matrix[i] = mat[len(mat) - 1 - i]
    return matrix


def get_empty_matrix(mat, diagonal=False):
    """ Returns an empty matrix to perform transposition.

    Takes source matrix and whether transposition uses diagonal as parameters.
    Returns empty matrix of identical size if diagonal is not used.
    Returns empty matrix with flipped rows and columns if diagonal is used.
    """

    matrix = []
    rows = len(mat[0]) if diagonal else len(mat)
    columns = len(mat) if diagonal else len(mat[0])
    for i in range(rows):
        matrix.append([])
        for _ in range(columns):
            matrix[i].append(0)
    return matrix


def calculate_determinant(mat):
    """ Calculates determinant for given matrix.

    Returns None if matrix is empty or not square.
    Returns single value of 1x1 matrix, returns determinant of 2x2 matrix.
    With a larger matrix recursively calls the function with a submatrix one size smaller.
    """

    if not mat or len(mat) != len(mat[0]):
        return None
    if len(mat) == 1:
        return mat[0][0]
    elif len(mat) == 2:
        return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
    determinant = 0
    for j in range(len(mat)):
        determinant += mat[0][j] * calculate_determinant(get_submatrix(mat, 0, j)) * ((-1) ** j)
    return determinant


def get_submatrix(mat, index_i, index_j):
    """ Returns submatrix of given matrix with [index_i] row and [index_j] column removed. """

    submatrix = []
    for _ in range(len(mat) - 1):
        submatrix.append([])
    for i in range(len(mat)):
        if index_i != i:
            for j in range(len(mat)):
                if index_j != j:
                    submatrix[i - 1 if index_i < i else i].append(mat[i][j])
    return submatrix


def invert_matrix(mat):
    """ Returns an inverse of given matrix.

    Calculates adjoint matrix, then multiplies it by 1 divided by given matrix's determinant.
    """
    determinant = calculate_determinant(mat)
    if determinant == 0:
        return []
    return multiply_matrix(calculate_adjoint(mat), str(1 / determinant))


def calculate_adjoint(mat):
    """ Calculates adjoint matrix of given matrix.

    For each cell of given matrix calculates minor and multiplies it by co-factor.
    """
    matrix = get_empty_matrix(mat)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = calculate_determinant(get_submatrix(mat, i, j)) * (-1) ** (i + j)
    return transpose_main(matrix)


def print_matrix(mat):
    """ Prints given matrix with values separated by spaces. """

    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == 0:
                mat[i][j] = "0"
            elif mat[i][j] == int(mat[i][j]):
                mat[i][j] = str(int(mat[i][j]))
            else:
                mat[i][j] = str(mat[i][j])

        print(" ".join(mat[i]))


def print_result(result):
    """ Prints resulting matrix or value, throws error if invalid choice or operation. """

    if result == "invalid":
        print("Invalid choice")
    elif not isinstance(result, list):
        print("The result is:\n" + str(result))
    elif result:
        print("The result is:")
        print_matrix(result)
    else:
        print("The operation cannot be performed.")
    print()


def get_option():
    """ Return main menu option selected by user. """

    print("1. Add matrices")
    print("2. Multiply matrix by a constant")
    print("3. Multiply matrices")
    print("4. Transpose matrix")
    print("5. Calculate a determinant")
    print("6. Inverse matrix")
    print("0. Exit")
    return input("Your choice: ")


def get_transposition_option():
    """ Return transposition submenu option selected by user. """

    print()
    print("1. Main diagonal")
    print("2. Side diagonal")
    print("3. Vertical line")
    print("4. Horizontal line")
    return input("Your choice: ")


while True:
    selection = get_option()
    if selection == "0":
        break
    elif selection == "1":
        result = add_matrices(get_matrix("first "), get_matrix("second "))
    elif selection == "2":
        result = multiply_matrix(get_matrix(""), input("Enter constant: "))
    elif selection == "3":
        result = multiply_matrices(get_matrix("first "), get_matrix("second "))
    elif selection == "4":
        selection = get_transposition_option()
        if selection == "1":
            result = transpose_main(get_matrix(""))
        elif selection == "2":
            result = transpose_side(get_matrix(""))
        elif selection == "3":
            result = transpose_vertical(get_matrix(""))
        elif selection == "4":
            result = transpose_horizontal(get_matrix(""))
        else:
            result = "invalid"
    elif selection == "5":
        result = calculate_determinant(get_matrix(""))
    elif selection == "6":
        result = invert_matrix(get_matrix(""))
    else:
        result = "invalid"
    print_result(result)
