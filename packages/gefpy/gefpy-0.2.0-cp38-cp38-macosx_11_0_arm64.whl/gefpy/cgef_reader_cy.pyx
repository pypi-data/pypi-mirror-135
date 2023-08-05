# distutils: language=c++
# cython: language_level=3
"""
    Provides access to the cgef_reader interface.
"""

from .cgef_reader cimport *


cdef class CgefR:
    cdef CgefReader* c_cgef  # Hold a C++ instance which we're wrapping
    cdef unsigned int exp_len
    cdef unsigned int gene_num

    def __cinit__(self, filepath, bin_size):
        self.c_cgef = new CgefReader(filepath, bin_size)
        self.exp_len = self.c_cgef.getExpressionNum()
        self.gene_num = self.c_cgef.getGeneNum()

    def __init__(self, filepath, bin_size):
        """
        A class for reading common bin GEF.

        :param filepath: Input bin GEF filepath.
        :param bin_size: Bin size.
        """
        pass

    def __dealloc__(self):
        del self.c_cgef

    def get_expression_num(self):
        """
        Get the number of expression.
        """
        return self.c_cgef.getExpressionNum()

    def get_cell_num(self):
        """
        Get the number of cell.
        """
        return self.c_cgef.getCellNum()

    def get_gene_num(self):
        """
        Get the number of gene.
        """
        return self.c_cgef.getGeneNum()

    def get_gene_names(self):
        """
        Get an array of gene names.
        """
        # cdef view.array gene_names = view.array((self.c_bgef.getGeneNum(),),
        #                                         itemsize=32 * sizeof(char), format='32s', allocate_buffer=True)
        cdef vector[string] gene_names
        gene_names.reserve(self.gene_num)
        self.c_cgef.getGeneNameList(gene_names)
        return np.asarray(gene_names)

    def get_cell_ids(self):
        """
        Get an array of cell ids.
        """
        cdef unsigned long long int[::1] cell_ids = np.empty(self.get_cell_num(), dtype=np.uint64)
        self.c_cgef.getCellPosList(&cell_ids[0])
        return np.asarray(cell_ids)

    def get_sparse_matrix_indices(self, str order = 'gene'):
        """
        Gets indices for building csr_matrix.

        Examples:
        from scipy import sparse
        sparse.csr_matrix((count, indices, indptr), shape=(cell_num, gene_num))

        :param indices:  CSR format index array of the matrix. Cell id array, the column indices, is the same size as count.
        :param indptr:   CSR format index pointer array of the matrix. indptr length = gene_num_ + 1 .
        :param count:    CSR format data array of the matrix. Expression count.
        :param order:    Order of count, "gene" or "cell".
        :return: (indices, indptr, count, order)
        """
        cdef unsigned int[::1] indices = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] indptr = np.empty(self.gene_num + 1, dtype=np.uint32)
        cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
        self.c_cgef.getSparseMatrixIndices(&indices[0], &indptr[0], &count[0], order)
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
        self.c_cgef.getSparseMatrixIndices2(&cell_ind[0], &gene_ind[0], &count[0])
        return np.asarray(cell_ind), np.asarray(gene_ind), np.asarray(count)

    def use_region(self, min_x, max_x, min_y, max_y):
        self.c_cgef.useRegion(min_x, max_x, min_y, max_y)

    def get_cellid_and_count(self):
        """
        Gets cellId and count from the geneExp dataset.

        :return:  (cell_id, count)
        """
        cdef unsigned int[::1] cell_id = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
        self.c_cgef.getCellIdAndCount(&cell_id[0], &count[0])
        return np.asarray(cell_id), np.asarray(count)

    def get_geneid_and_count(self):
        """
        Gets geneId and count from the cellExp dataset.
        
        :return:  (gene_id, count)
        """
        cdef unsigned int[::1] gene_id = np.empty(self.exp_len, dtype=np.uint32)
        cdef unsigned int[::1] count = np.empty(self.exp_len, dtype=np.uint32)
        self.c_cgef.getGeneIdAndCount(&gene_id[0], &count[0])
        return np.asarray(gene_id), np.asarray(count)





