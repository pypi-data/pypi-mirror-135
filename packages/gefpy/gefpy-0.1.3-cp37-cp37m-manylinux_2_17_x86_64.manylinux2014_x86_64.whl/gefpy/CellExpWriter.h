
#pragma once

#include "hdf5.h"
#include "GeneExp.h"

typedef struct
{
    unsigned int x;
    unsigned int y;
    unsigned short area;
    unsigned short expCount;
    unsigned short dnbCount;
    unsigned short geneCount;
    unsigned int geneOffset;
//    hdset_reg_ref_t geneExp;
} CellData;

typedef struct
{
    unsigned short geneID;
    unsigned short count;
} CellExpData;

struct GeneName
{
    GeneName(const char* g)
    {
        int i = 0;
        while (g[i] != '\0')
        {
            name[i] = g[i];
            ++i;
        }
    }
    char name[32] = {0};
};

class CellExpWriter
{
public:
    CellExpWriter(const string& outPath);
    ~CellExpWriter();

    unsigned int gene_num{};

    void storeCell(unsigned int * x, unsigned int * y, unsigned short * area, unsigned int size);

    void storeCellExp();

    void storeCellBorder(char* borderPath, unsigned int size);

    void storeGeneList(vector<string>& geneList);

    void storeGeneList();

    void storeVersion();

    static bool copyFile(const string& inPath, const string& outPath);

    void add_cell_bin(unsigned int * bin_index, unsigned int size);

    void setGeneExpMap(const string &inPath);

private:
    hid_t m_file_id;
    herr_t m_status;
    hid_t m_group_id;
    map<unsigned long long , vector<CellExpData>> gene_exp_map;
    vector<CellExpData> cell_exp_list;
    vector<unsigned short> cell_dnb_count_list;
    vector<unsigned short> cell_gene_count_list;
    vector<unsigned short> cell_exp_count_list;  //offset
    vector<unsigned int> cell_gene_exp_list;  //offset
    GenePos* gene_pos;

    double mean(unsigned short* resultSet, unsigned int size);

    double mean(vector<unsigned short> resultSet);

    double mean(vector<unsigned int> resultSet);
};