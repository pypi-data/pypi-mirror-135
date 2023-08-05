# -*- coding: utf-8 -*-
# distutils: language=c++
# cython: language_level=3, boundscheck=False
# cython: c_string_type=unicode, c_string_encoding=utf8
# Created by huangzhibo on 2022/01/01

from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp cimport bool


cdef extern from "bgef_reader.h":
    cdef cppclass BgefReader:
        BgefReader(const string& filename, int bin_size, bool verbose) except +
        unsigned int getGeneNum() const
        unsigned int getCellNum()
        unsigned int getExpressionNum() const

        void getGeneNameList(vector[string] & gene_list)
        void getCellPosList(unsigned long long int * cell_pos_list)

        vector[unsigned long long] getSparseMatrixIndicesOfExp(unsigned int * cell_index, unsigned int * count)
        vector[string] getSparseMatrixIndicesOfGene(unsigned int * gene_index)
        void getSparseMatrixIndicesOfGene(unsigned int * gene_index, char * gene_names)

        int getSparseMatrixIndices(unsigned int *indices, unsigned int *indptr, unsigned int *count)
        int getSparseMatrixIndices2(unsigned int *cell_ind, unsigned int *gene_ind, unsigned int *count)

        const unsigned int *getWholeExpMatrixShape() const

        void readWholeExpMatrix(unsigned int offset_x,
                                unsigned int offset_y,
                                unsigned int rows,
                                unsigned int cols,
                                string & key,
                                unsigned char *matrix) const

        void readWholeExpMatrix(string & key,
                                unsigned char *matrix) const
