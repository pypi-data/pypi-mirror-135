# -*- coding: utf-8 -*-
# distutils: language=c++
# cython: language_level=3, boundscheck=False
# cython: c_string_type=unicode, c_string_encoding=utf8


import numpy as np
cimport numpy as np

from libcpp.vector cimport vector
from libcpp.string cimport string


cdef extern from "CellExpWriter.h":
    ctypedef char byte
    ctypedef struct CellExpData:
        unsigned short geneID
        unsigned short count

    cdef cppclass CellExpWriter:
        CellExpWriter(const string& outPath) except +

        void add_cell_bin(unsigned int * bin_index, unsigned int size)
        void storeCell(unsigned int * x, unsigned int * y, unsigned short * area, unsigned int size)
        void storeCellExp()
        void storeCellBorder(byte* borderPath, unsigned int size);
        void storeGeneList()
        void storeVersion()
        void setGeneExpMap(const string & inPath)


cdef class CellExpW:
    cdef CellExpWriter* c_cell_w  # Hold a C++ instance which we're wrapping

    def __init__(self, filepath):
        self.c_cell_w = new CellExpWriter(filepath)

    def storeCell(self, np.ndarray[np.uint32_t, ndim=1] x, np.ndarray[np.uint32_t, ndim=1] y,
                  np.ndarray[np.uint16_t, ndim=1] area, unsigned int size):
        self.c_cell_w.storeCell(<unsigned int *>x.data, <unsigned int *>y.data, <unsigned short *>area.data, size)

    def storeCellExp(self):
        self.c_cell_w.storeCellExp()

    def storeCellBorder(self, np.ndarray[np.int8_t, ndim=3] border_path, unsigned int size):
        self.c_cell_w.storeCellBorder(<char*> border_path.data, size)

    def storeGeneList(self):
        self.c_cell_w.storeGeneList()

    def add_cell_bin(self, np.ndarray[np.uint32_t, ndim=2] cell_exp_index, unsigned int size):
        self.c_cell_w.add_cell_bin(<unsigned int *>cell_exp_index.data, size)

    def setGeneExpMap(self, const string & inPath):
        self.c_cell_w.setGeneExpMap(inPath)

    def __dealloc__(self):
        del self.c_cell_w