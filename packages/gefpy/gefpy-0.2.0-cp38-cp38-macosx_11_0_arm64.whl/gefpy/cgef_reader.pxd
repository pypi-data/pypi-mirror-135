# distutils: language=c++
# cython: language_level=3
import numpy as np
cimport numpy as np

from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp cimport bool

cdef extern from "cgef_reader.h" nogil:
    cdef cppclass CgefReader:
        CgefReader(const string &filename, bool verbose)
        unsigned short getGeneNum() const;
        unsigned int getCellNum() const;
        unsigned int getExpressionNum() const;

        void getGeneNameList(vector[string] & gene_list)
        void getCellPosList(unsigned long long int * cell_pos_list)

        int getSparseMatrixIndices(unsigned int * indices,
                                   unsigned int * indptr,
                                   unsigned int * count,
                                   const char * order)

        int getSparseMatrixIndices2(unsigned int * cell_ind, unsigned int * gene_ind, unsigned int * count)

        void useRegion(unsigned int min_x, unsigned int max_x, unsigned int min_y, unsigned int max_y)

        void getCellIdAndCount(unsigned int * cell_id, unsigned int * count) const

        void getGeneIdAndCount(unsigned int * gene_id, unsigned int * count) const

