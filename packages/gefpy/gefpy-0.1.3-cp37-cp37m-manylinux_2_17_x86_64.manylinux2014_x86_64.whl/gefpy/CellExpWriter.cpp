
#include "CellExpWriter.h"

#include <iostream>
#include <cstring>
#include <algorithm>
#include <fstream>
#include <string>
#include <vector>
#include <numeric>


CellExpWriter::CellExpWriter(const string &outPath) {
//    bool r = copyFile(inPath, outPath);
//    if(!r) cerr << "Error writing to file (" << outPath << ") is failed!" << endl;

    printf("create h5 file: %s\n", outPath.c_str());
    m_file_id = H5Fcreate(outPath.c_str(), H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);

    storeVersion();
    m_group_id = H5Gcreate(m_file_id, "/cellBin", H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
    m_status = H5Gclose(m_group_id);
}

CellExpWriter::~CellExpWriter()
{
    free(gene_pos);
    m_status = H5Fclose(m_file_id);
}

void CellExpWriter::storeVersion() {
    hsize_t dimsAttr[1] = {1};
    hid_t data_space = H5Screate_simple(1, dimsAttr, NULL);
    hid_t attr = H5Acreate(m_file_id, "version", H5T_STD_U32LE, data_space, H5P_DEFAULT, H5P_DEFAULT);
    H5Awrite(attr, H5T_NATIVE_UINT, &version);
    H5Sclose(data_space);
    H5Aclose(attr);
}

void CellExpWriter::storeGeneList(vector<string> & geneList) {
    hsize_t dims[1] = {geneList.size()};
    hid_t strtype = H5Tcopy(H5T_C_S1);
    H5Tset_size(strtype, 32);

    hid_t dataspace_id = H5Screate_simple(1, dims, NULL);
    hid_t dataset_id = H5Dcreate(m_file_id, "cellBin/geneList", strtype, dataspace_id, H5P_DEFAULT,
                             H5P_DEFAULT, H5P_DEFAULT);
    m_status = H5Dwrite(dataset_id, strtype, H5S_ALL, H5S_ALL, H5P_DEFAULT, &geneList[0]);
    H5Sclose(dataspace_id);
    H5Dclose(dataset_id);
}

void CellExpWriter::storeGeneList() {
    hid_t strtype;
//    hid_t memtype, filetype;

    strtype = H5Tcopy(H5T_C_S1);
    m_status = H5Tset_size(strtype, char_len);

//    memtype = H5Tcreate(H5T_COMPOUND, sizeof(GenePos));
//    m_status = H5Tinsert(memtype, "gene", HOFFSET(GenePos, gene), strtype);
//    m_status = H5Tinsert(memtype, "offset", HOFFSET(GenePos, offset), H5T_NATIVE_UINT);
//    m_status = H5Tinsert(memtype, "count", HOFFSET(GenePos, count), H5T_NATIVE_UINT);
//
//    filetype = H5Tcreate(H5T_COMPOUND, char_len);
//    m_status = H5Tinsert(filetype, "gene", 0, strtype);

    hsize_t dims[1] = {gene_num};

    GeneName * gene_name = (GeneName*)malloc(gene_num * sizeof(GeneName));
    for(int i=0; i< gene_num; i++){
        gene_name[i] = gene_pos[i].gene;
    }

    hid_t dataspace_id = H5Screate_simple(1, dims, NULL);
    hid_t dataset_id = H5Dcreate(m_file_id, "cellBin/geneList", strtype, dataspace_id, H5P_DEFAULT,
                                 H5P_DEFAULT, H5P_DEFAULT);
    m_status = H5Dwrite(dataset_id, strtype, H5S_ALL, H5S_ALL, H5P_DEFAULT, gene_name);
    free(gene_name);
    H5Sclose(dataspace_id);
    H5Dclose(dataset_id);
}

bool CellExpWriter::copyFile(const string &inPath, const string &outPath) {
    ifstream fin(inPath, ios::binary);
    ofstream fout(outPath, ios::binary);

    bool bRet = true;

    while(!fin.eof()){
        char szBuf;
        fin.read(&szBuf, sizeof(char));

        if(fin.eof()) break;

        if (fout.bad())
        {
            bRet = false;
            break;
        }
        fout.write(&szBuf, sizeof(char));
    }

    fout.close();
    fin.close();
    return bRet;
}

void CellExpWriter::storeCellBorder(char* borderPath, unsigned int size) {
    hsize_t dims[3];
    dims[0] = size;
    dims[1] = 16;
    dims[2] = 2;

    hid_t dataspace_id = H5Screate_simple(3, dims, NULL);
    hid_t dataset_id = H5Dcreate(m_file_id, "cellBin/cellBorder", H5T_STD_I8LE, dataspace_id, H5P_DEFAULT,
                                 H5P_DEFAULT, H5P_DEFAULT);
    H5Dwrite(dataset_id, H5T_STD_I8LE, H5S_ALL, H5S_ALL, H5P_DEFAULT, borderPath);
    H5Sclose(dataspace_id);
    H5Dclose(dataset_id);
}

void CellExpWriter::storeCellExp() {

    hsize_t dims[1] = {cell_exp_list.size()};

    hid_t memtype, filetype;
    memtype = H5Tcreate(H5T_COMPOUND, sizeof(CellExpData));
    H5Tinsert(memtype, "geneID", HOFFSET(CellExpData, geneID), H5T_NATIVE_USHORT);
    H5Tinsert(memtype, "count", HOFFSET(CellExpData, count), H5T_NATIVE_USHORT);

    filetype = H5Tcreate(H5T_COMPOUND, 4);
    H5Tinsert(filetype, "geneID", 0, H5T_STD_U16LE);
    H5Tinsert(filetype, "count", 2, H5T_STD_U16LE);

    hid_t dataspace_id = H5Screate_simple(1, dims, NULL);
    hid_t dataset_id = H5Dcreate(m_file_id, "cellBin/cellExp", filetype, dataspace_id, H5P_DEFAULT,
                                 H5P_DEFAULT, H5P_DEFAULT);
    H5Dwrite(dataset_id, memtype, H5S_ALL, H5S_ALL, H5P_DEFAULT, &cell_exp_list[0]);

    H5Tclose(memtype);
    H5Tclose(filetype);
    H5Sclose(dataspace_id);
    H5Dclose(dataset_id);
}

void CellExpWriter::storeCell(unsigned int * x, unsigned int * y, unsigned short * area, unsigned int size) {
    CellData * cell = (CellData*)malloc(size * sizeof(CellData));

    for(unsigned int i=0; i < size; i++){
        cell[i] = {x[i], y[i], area[i], cell_exp_count_list[i], cell_dnb_count_list[i], cell_gene_count_list[i],cell_gene_exp_list[i]};
    }

    double average_cell_area = mean(area, size);
    double average_exp_count = mean(cell_exp_count_list);
    double average_dnb_count = mean(cell_dnb_count_list);
    double average_gene_count = mean(cell_gene_count_list);

    printf("Average Cell Area : %.2f\n", average_exp_count);
    printf("Average Cell Exp Count : %.2f\n", average_exp_count);
    printf("Average Cell DNB Count : %.2f\n", average_dnb_count);
    printf("Average Cell Gene Count : %.2f\n", average_gene_count);

    hsize_t dims[1] = {(hsize_t)size};

    hid_t memtype, filetype;
    memtype = H5Tcreate(H5T_COMPOUND, sizeof(CellData));
    H5Tinsert(memtype, "x", HOFFSET(CellData, x), H5T_NATIVE_UINT);
    H5Tinsert(memtype, "y", HOFFSET(CellData, y), H5T_NATIVE_UINT);
    H5Tinsert(memtype, "area", HOFFSET(CellData, area), H5T_NATIVE_USHORT);
    H5Tinsert(memtype, "expCount", HOFFSET(CellData, expCount), H5T_NATIVE_USHORT);
    H5Tinsert(memtype, "dnbCount", HOFFSET(CellData, dnbCount), H5T_NATIVE_USHORT);
    H5Tinsert(memtype, "geneCount", HOFFSET(CellData, geneCount), H5T_NATIVE_USHORT);
    H5Tinsert(memtype, "geneOffset", HOFFSET(CellData, geneOffset), H5T_NATIVE_UINT);

    filetype = H5Tcreate(H5T_COMPOUND, 20);
    H5Tinsert(filetype, "x", 0, H5T_STD_U32LE);
    H5Tinsert(filetype, "y", 4, H5T_STD_U32LE);
    H5Tinsert(filetype, "area", 8, H5T_STD_U16LE);
    H5Tinsert(filetype, "expCount", 14, H5T_STD_U16LE);
    H5Tinsert(filetype, "dnbCount", 10, H5T_STD_U16LE);
    H5Tinsert(filetype, "geneCount", 12, H5T_STD_U16LE);
    H5Tinsert(filetype, "geneOffset", 16, H5T_STD_U32LE);

    hid_t dataspace_id = H5Screate_simple(1, dims, NULL);
    hid_t dataset_id = H5Dcreate(m_file_id, "cellBin/cell", filetype, dataspace_id, H5P_DEFAULT,
                                 H5P_DEFAULT, H5P_DEFAULT);
    H5Dwrite(dataset_id, memtype, H5S_ALL, H5S_ALL, H5P_DEFAULT, cell);

    free(cell);
    H5Tclose(memtype);
    H5Tclose(filetype);
    H5Sclose(dataspace_id);
    H5Dclose(dataset_id);
//    hdset_reg_ref_t wdata[1];
//    status = H5Sselect_elements (space, H5S_SELECT_SET, 4, coords[0]);
//    status = H5Rcreate (&wdata[0], file, DATASET2, H5R_DATASET_REGION, space);
}

void CellExpWriter::add_cell_bin(unsigned int * bin_index, unsigned int size){
    unsigned long long bin_id;
    map<unsigned short, unsigned short> gene_count_in_cell;
    unsigned short gene_count = 0;
    unsigned short exp_count = 0;

    cell_dnb_count_list.emplace_back(size);

    for (unsigned int i = 0; i < size; ++i) {
        bin_id = bin_index[2*i];
        bin_id = bin_id << 32 | bin_index[2*i+1];
        auto iter = gene_exp_map.find(bin_id);
        if(iter != gene_exp_map.end()){
            vector<CellExpData> cxp = iter->second;
            auto it = cxp.begin();
            while (it != cxp.end()) {
                exp_count += it->count;
                auto iter_gene = gene_count_in_cell.find(it->geneID);
                if(iter_gene != gene_count_in_cell.end()){
                    iter_gene->second += it->count;
                } else{
                    gene_count_in_cell.insert(map<unsigned short, unsigned short>::value_type(it->geneID, it->count));
                    gene_count++;
                }
                ++it;
            }
        }
    }

    map<unsigned short, unsigned short> ::iterator iter_m;
    iter_m = gene_count_in_cell.begin();
    while(iter_m != gene_count_in_cell.end()) {
        CellExpData cexp_tmp = {iter_m->first, iter_m->second};
        cell_exp_list.emplace_back(cexp_tmp);
        ++iter_m;
    }

    cell_exp_count_list.emplace_back(exp_count);

    if(cell_gene_exp_list.empty()){
        cell_gene_exp_list.emplace_back(0);
    }else {
        cell_gene_exp_list.emplace_back(cell_gene_exp_list.back()+cell_gene_count_list.back());
    }
    cell_gene_count_list.emplace_back(gene_count);
}

void CellExpWriter::setGeneExpMap(const string &inPath){
    GeneExp gene_exp = GeneExp(inPath, 1);
    auto * gene_index = (unsigned int *)malloc(gene_exp.getExpLen() * sizeof(unsigned int));
    vector<string> gene_names;
    gene_exp.getGeneData(gene_index, gene_names);

    gene_pos = gene_exp.getGenePos();
    gene_num = gene_exp.getGeneNum();
    Gene * expData = gene_exp.getGeneExpData();

    unsigned long long xy_bin;
    for (int i = 0; i < gene_exp.getExpLen(); ++i) {
        CellExpData cellExpData = {(unsigned short)gene_index[i], (unsigned short)expData[i].cnt};
//        xy_bin = expData[i].x - gene_exp.minX;
//        xy_bin = xy_bin << 32 | (expData[i].y - gene_exp.minY);
        xy_bin = expData[i].x;
        xy_bin = xy_bin << 32 | expData[i].y;

        auto iter = gene_exp_map.find(xy_bin);
        if(iter != gene_exp_map.end()){
            iter->second.emplace_back(cellExpData);
        }else{
            vector<CellExpData> cellExpDataList;
            cellExpDataList.emplace_back(cellExpData);
            gene_exp_map.insert(map<unsigned long long, vector<CellExpData>>::value_type (xy_bin, cellExpDataList));
        }
    }

    free(expData);
    free(gene_index);
}

double CellExpWriter::mean(unsigned short* resultSet, unsigned int size){
    double sum = 0;
    for(unsigned int i = 0; i < size; i++){
        sum += resultSet[i];
    }
    return sum / size;
}

double CellExpWriter::mean(vector<unsigned short> resultSet){
    double sum = std::accumulate(std::begin(resultSet), std::end(resultSet), 0.0);
    return sum / resultSet.size();
}

double CellExpWriter::mean(vector<unsigned int> resultSet){
    double sum = std::accumulate(std::begin(resultSet), std::end(resultSet), 0.0);
    return sum / resultSet.size();
}
