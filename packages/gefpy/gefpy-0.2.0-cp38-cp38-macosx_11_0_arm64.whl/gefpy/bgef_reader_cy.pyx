# -*- coding: utf-8 -*-
# distutils: language=c++
# cython: language_level=3, boundscheck=False
# cython: c_string_type=unicode, c_string_encoding=utf8
# Created by huangzhibo on 2022/01/01
"""
    Provides access to the bgef_reader interface.
    For reading common bin GEF.
"""

from .bgef_reader cimport *
import numpy as np
cimport numpy as np

from cython cimport view

cdef class BgefR:
    cdef BgefReader* c_bgef  # Hold a C++ instance which we're wrapping
    cdef unsigned int exp_len
    cdef unsigned int gene_num

    def __cinit__(self, filepath, bin_size):
        self.c_bgef = new BgefReader(filepath, bin_size, True)
        self.exp_len = self.c_bgef.getExpressionNum()
        self.gene_num = self.c_bgef.getGeneNum()

    def __init__(self, filepath, bin_size):
        """
        A class for reading common bin GEF.

        :param filepath: Input bin GEF filepath.
        :param bin_size: Bin size.
        """
        pass

    def __dealloc__(self):
        del self.c_bgef

    def get_expression_num(self):
        """
        Get the number of expression.
        """
        return self.c_bgef.getExpressionNum()

    def get_cell_num(self):
        """
        Get the number of cell.
        """
        return self.c_bgef.getCellNum()

    def get_gene_num(self):
        """
        Get the number of gene.
        """
        return self.c_bgef.getGeneNum()

    def get_gene_names(self):
        """
        Get an array of gene names.
        """
        # cdef view.array gene_names = view.array((self.c_bgef.getGeneNum(),),
        #                                         itemsize=32 * sizeof(char), format='32s', allocate_buffer=True)
        cdef vector[string] gene_names
        gene_names.reserve(self.gene_num)
        self.c_bgef.getGeneNameList(gene_names)
        return np.asarray(gene_names)

    def get_cell_ids(self):
        """
        Get an array of cell ids.
        """
        cdef unsigned long long int[::1] cell_ids = np.empty(self.get_cell_num(), dtype=np.uint64)
        self.c_bgef.getCellPosList(&cell_ids[0])
        return np.asarray(cell_ids)

    # def get_gene_data(self):
    #     cdef unsigned int[::1] gene_index = np.empty(self.exp_len, dtype=np.uint32)
    #     cdef vector[string] uniq_genes = self.c_bgef.getSparseMatrixIndexesOfGene(&gene_index[0])
    #     return np.asarray(gene_index), np.asarray(uniq_genes)

    def get_sparse_matrix_indices(self):
        """
        Gets indices for building csr_matrix.

        Examples:
        from scipy import sparse
        sparse.csr_matrix((count, indices, indptr), shape=(cell_num, gene_num))

        :param indices:  CSR format index array of the matrix. Cell id array, the column indices, is the same size as count.
        :param indptr:   CSR format index pointer array of the matrix. indptr length = gene_num_ + 1 .
        :param count:    CSR format data array of the matrix. Expression count.
        :return: (indices, indptr, count)
        """
        cdef unsigned int[::1] indices = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] indptr = np.empty(self.gene_num + 1, dtype=np.uint32)
        cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
        self.c_bgef.getSparseMatrixIndices(&indices[0], &indptr[0], &count[0])
        return np.asarray(indices), np.asarray(indptr), np.asarray(count)

    def get_sparse_matrix_indices2(self):
        """
        Gets indices for building csr_matrix.

        Examples:
        from scipy import sparse
        sparse.csr_matrix((count, cell_ind, gene_ind), shape=(cell_num, gene_num))

        :param cell_ind:  CSR format index array of the matrix. same size as count.
        :param gene_ind:  CSR format index array of the matrix. same size as count.
        :param count:     CSR format data array of the matrix. Expression count.
        :return: (cell_ind, gene_ind, count)
        """
        cdef unsigned int[::1] cell_ind = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] gene_ind = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
        self.c_bgef.getSparseMatrixIndices2(&cell_ind[0], &gene_ind[0], &count[0])
        return np.asarray(cell_ind), np.asarray(gene_ind), np.asarray(count)


    def get_sparse_matrix_indices_of_exp(self):
        """
        Get sparse matrix indexes of expression data.

        :return: (uniq_cell, cell_index, count)
        """
        cdef unsigned int[::1] cell_index = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
        cdef vector[unsigned long long] uniq_cell = self.c_bgef.getSparseMatrixIndicesOfExp(&cell_index[0], &count[0])
        return np.asarray(uniq_cell), np.asarray(cell_index), np.asarray(count)

    def get_sparse_matrix_indices_of_gene(self):
        """
        Get gene data.
        :return: (gene_index, gene_names)
        """
        cdef unsigned int[::1] gene_index = np.empty(self.c_bgef.getGeneNum()+1, dtype=np.uint32)
        cdef view.array gene_names = view.array((self.c_bgef.getGeneNum(),),
                                           itemsize=32*sizeof(char), format='32s', allocate_buffer=True)

        self.c_bgef.getSparseMatrixIndicesOfGene(&gene_index[0], gene_names.data)
        return np.asarray(gene_index), np.asarray(gene_names)


    def read_whole_exp_matrix(self,
                              unsigned int offset_x,
                              unsigned int offset_y,
                              unsigned int rows,
                              unsigned int cols,
                              string & key,
                              np.ndarray[np.uint8_t, ndim=1] matrix):
        """
        Get wholeExp matrix.

        :param offset_x: The starting position on the x-axis to be read.
        :param offset_y: The starting position on the y-axis to be read.
        :param rows:     Number of rows to read.
        :param cols:     Number of cols to read.
        :param key: MIDcount or genecount.
        :param matrix: When the value is greater than 255, it will be set to 255.
        :return:
        """
        self.c_bgef.readWholeExpMatrix(offset_x, offset_y, rows, cols, key, <unsigned char*>matrix.data)


    def read_whole_exp_matrix_all(self, str key):
        """
        Get wholeExp matrix.

        :param key: MIDcount or genecount.
        :return: 2D Matrix: When the value is greater than 255, it will be set to 255.
        """
        cdef np.ndarray[np.uint8_t, ndim = 2] matrix = np.empty(self.get_whole_exp_matrix_shape(), dtype=np.uint8)
        self.c_bgef.readWholeExpMatrix(key, <unsigned char*>matrix.data)
        return matrix

    def get_whole_exp_matrix_shape(self) -> np.ndarray:
        """
        Get the shape of wholeExp matrix.
        :return: [rows, cols]
        """
        cdef view.array shape = view.array((2,), itemsize=sizeof(unsigned int), format="I", allocate_buffer=False)
        shape.data = <char *>self.c_bgef.getWholeExpMatrixShape()
        return np.asarray(shape)

#@Depracted
cdef class GEF:
    cdef BgefReader* c_bgef  # Hold a C++ instance which we're wrapping
    cdef unsigned int exp_len
    cdef unsigned int gene_num

    def __cinit__(self, filepath, bin_size):
        self.c_bgef = new BgefReader(filepath, bin_size, True)
        self.exp_len = self.c_bgef.getExpressionNum()
        self.gene_num = self.c_bgef.getGeneNum()

    def __init__(self, filepath, bin_size):
        """
        A class for reading common bin GEF.

        :param filepath: Input bin GEF filepath.
        :param bin_size: Bin size.
        """
        pass

    def __dealloc__(self):
        del self.c_bgef

    def get_expression_num(self):
        """
        Get the number of expression.
        """
        return self.c_bgef.getExpressionNum()

    def get_cell_num(self):
        """
        Get the number of cell.
        """
        return self.c_bgef.getCellNum()

    def get_gene_num(self):
        """
        Get the number of gene.
        """
        return self.c_bgef.getGeneNum()

    def get_exp_data(self):
        """
        Get sparse matrix indexes of expression data.

        :return: (uniq_cell, cell_index, count)
        """
        cdef unsigned int[::1] cell_index = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
        cdef vector[unsigned long long] uniq_cell = self.c_bgef.getSparseMatrixIndicesOfExp(&cell_index[0], &count[0])
        return np.asarray(uniq_cell), np.asarray(cell_index), np.asarray(count)

    def get_gene_data(self):
        """
        Get gene data.
        :return: (gene_index, gene_names)
        """
        cdef unsigned int[::1] gene_index = np.empty(self.c_bgef.getGeneNum()+1, dtype=np.uint32)
        cdef view.array gene_names = view.array((self.c_bgef.getGeneNum(),),
                                           itemsize=32*sizeof(char), format='32s', allocate_buffer=True)

        self.c_bgef.getSparseMatrixIndicesOfGene(&gene_index[0], gene_names.data)
        return np.asarray(gene_index), np.asarray(gene_names)

