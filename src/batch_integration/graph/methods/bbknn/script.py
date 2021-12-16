## VIASH START
par = {
    'adata': './src/batch_integration/resources/datasets_pancreas.h5ad',
    'output': './src/batch_integration/resources/pancreas_bbknn.h5ad',
    'hvg': True,
    'scaling': True,
    'debug': True
}
## VIASH END

print('Importing libraries')
from pprint import pprint
import scanpy as sc
from scib.integration import bbknn

if par['debug']:
    pprint(par)

adata_file = par['adata']
output = par['output']
hvg = par['hvg']
scaling = par['scaling']

print('Read adata')
adata = sc.read(adata_file)

if hvg:
    print('Select HVGs')
    # TODO: check that hvg value makes sense on dataset
    #hvgs_list = hvg_batch(adata, batch_key='batch', target_genes=hvg, adataOut=False)
    adata = adata[:, adata.var['hvg']]


if scaling:
    print('Scale')
    adata.X = adata.layers['logcounts_scaled']
else:
    adata.X = adata.layers['logcounts']

print('Integrate')
adata = bbknn(adata, batch='batch')

print('Save HDF5')
adata.uns['hvg'] = hvg
adata.uns['scaled'] = scaling

adata.write(output, compression='gzip')
