import numpy as np 
import scanpy as sc

########## DATA PREPROCESS ##########
#this part is same as preprocessing step in iMAP, we refer from https://github.com/Svvord/iMAP
def sub_data_preprocess(adata: sc.AnnData, n_top_genes: int=2000, batch_key: str=None, flavor: str='seurat_v3', min_genes: int=200, min_cells: int=3) -> sc.AnnData:
    sc.pp.filter_cells(adata, min_genes=min_genes)
    sc.pp.filter_genes(adata, min_cells=min_cells)
    if flavor == 'seurat_v3':
        # count data is expected when flavor=='seurat_v3'
        sc.pp.highly_variable_genes(adata, n_top_genes=n_top_genes, flavor=flavor, batch_key=batch_key)
    sc.pp.normalize_per_cell(adata, counts_per_cell_after=1e4)
    sc.pp.log1p(adata)
    if flavor != 'seurat_v3':
        # log-format data is expected when flavor!='seurat_v3'
        sc.pp.highly_variable_genes(adata, n_top_genes=n_top_genes, flavor=flavor, batch_key=batch_key)
    return adata

def data_preprocess(adata: sc.AnnData, key: str='batch', n_top_genes: int=2000, flavor: str='seurat_v3', min_genes: int=200, min_cells: int=3, n_batch: int=2) -> sc.AnnData:
    print('Establishing Adata for Next Step...')
    hv_adata = sub_data_preprocess(adata, n_top_genes=n_top_genes, batch_key = key, flavor=flavor, min_genes=min_genes, min_cells=min_cells)
    hv_adata = hv_adata[:, hv_adata.var['highly_variable']]
    print('PreProcess Done.')
    return hv_adata