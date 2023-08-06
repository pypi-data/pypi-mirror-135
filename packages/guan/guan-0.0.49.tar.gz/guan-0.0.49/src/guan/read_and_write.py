# Guan is an open-source python package developed and maintained by https://www.guanjihuan.com/about. The primary location of this package is on website https://py.guanjihuan.com.

# read and write

import numpy as np

def read_one_dimensional_data(filename='a', format='txt'): 
    f = open(filename+'.'+format, 'r')
    text = f.read()
    f.close()
    row_list = np.array(text.split('\n')) 
    dim_column = np.array(row_list[0].split()).shape[0] 
    x_array = np.array([])
    y_array = np.array([])
    for row in row_list:
        column = np.array(row.split()) 
        if column.shape[0] != 0:  
            x_array = np.append(x_array, [float(column[0])], axis=0)  
            y_row = np.zeros(dim_column-1)
            for dim0 in range(dim_column-1):
                y_row[dim0] = float(column[dim0+1])
            if np.array(y_array).shape[0] == 0:
                y_array = [y_row]
            else:
                y_array = np.append(y_array, [y_row], axis=0)
    return x_array, y_array

def read_two_dimensional_data(filename='a', format='txt'): 
    f = open(filename+'.'+format, 'r')
    text = f.read()
    f.close()
    row_list = np.array(text.split('\n')) 
    dim_column = np.array(row_list[0].split()).shape[0] 
    x_array = np.array([])
    y_array = np.array([])
    matrix = np.array([])
    for i0 in range(row_list.shape[0]):
        column = np.array(row_list[i0].split()) 
        if i0 == 0:
            x_str = column[1::] 
            x_array = np.zeros(x_str.shape[0])
            for i00 in range(x_str.shape[0]):
                x_array[i00] = float(x_str[i00]) 
        elif column.shape[0] != 0: 
            y_array = np.append(y_array, [float(column[0])], axis=0)  
            matrix_row = np.zeros(dim_column-1)
            for dim0 in range(dim_column-1):
                matrix_row[dim0] = float(column[dim0+1])
            if np.array(matrix).shape[0] == 0:
                matrix = [matrix_row]
            else:
                matrix = np.append(matrix, [matrix_row], axis=0)
    return x_array, y_array, matrix

def write_one_dimensional_data(x_array, y_array, filename='a', format='txt'): 
    x_array = np.array(x_array)
    y_array = np.array(y_array)
    with open(filename+'.'+format, 'w') as f:
        i0 = 0
        for x0 in x_array:
            f.write(str(x0)+'   ')
            if len(y_array.shape) == 1:
                f.write(str(y_array[i0])+'\n')
            elif len(y_array.shape) == 2:
                for j0 in range(y_array.shape[1]):
                    f.write(str(y_array[i0, j0])+'   ')
                f.write('\n')
            i0 += 1

def write_two_dimensional_data(x_array, y_array, matrix, filename='a', format='txt'): 
    x_array = np.array(x_array)
    y_array = np.array(y_array)
    matrix = np.array(matrix)
    with open(filename+'.'+format, 'w') as f:
        f.write('0   ')
        for x0 in x_array:
            f.write(str(x0)+'   ')
        f.write('\n')
        i0 = 0
        for y0 in y_array:
            f.write(str(y0))
            j0 = 0
            for x0 in x_array:
                f.write('   '+str(matrix[i0, j0])+'   ')
                j0 += 1
            f.write('\n')
            i0 += 1