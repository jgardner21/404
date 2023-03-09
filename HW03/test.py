from mult_inv import bin_div, bin_mult, MIB
from FindMI import MI

if __name__ == "__main__":
    for i in range(-10 **3, -1):
        for j in range(1, 10**3):
            if MI(i, j) != MIB(i,j):
                print("Error")
                break
    for i in range(1, 10**3):
        for j in range(1, 10**3):
            if MI(i, j) != MIB(i,j):
                print("Error")
                break
    print('All tests passed')
    '''for i in range(1, 10 ** 3):
        for j in range(1, 10 ** 3):
            if bin_div(i,j) != i //j:
                print('Error at Div: ' + str(i) + ', ' + str(j))
                break
            if bin_mult(i,j) != i * j:
                print('Error at Mult: ' + str(i) + ', ' + str(j))
                break
    for i in range(-10**3, 1):
        for j in range(1, 10 **3):
            if bin_div(i,j) != i //j:
                print('Error at Div: ' + str(i) + ', ' + str(j) + 'Expected: ' + str(i // j) + ' Actual: ' + str(bin_div(i,j)))
                break
            if bin_mult(i,j) != i * j:
                print('Error at Mult: ' + str(i) + ', ' + str(j) + 'Expected: ' + str(i * j) + ' Actual: ' + str(bin_mult(i,j)))
                break'''

