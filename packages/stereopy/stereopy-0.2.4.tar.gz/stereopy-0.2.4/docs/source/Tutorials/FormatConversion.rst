Format Conversion
==================
This section contains the introduction of format conversion.

StereoExpData to Anndata
-------------------------
The io module provides the function :mod:`stereo.io.stereo_to_anndata` to convert the StereoExpData into anndata format and output the
corresponding h5ad file(.h5ad).

parameters
~~~~~~~~~~~~~~~

:param data: StereoExpData object
:param flavor: 'scanpy' or 'seurat'. If you want to convert the output_h5ad into the rds file, set flavor='seurat'.
:param sample_id: name of sample. This will be set as 'orig.ident' in adata.obs.
:param reindex: whether to reindex the cell. The new index looks like "{sample_id}:{position_x}_{position_y}" format.
:param output: Default is None. If None, it will not generate a h5ad file.
:return: Anndata object

If you want to use sctransform to get the normalizetion result and convert the output_h5ad into the rds file,
you need to save raw data before you use sctransform. Otherwise, it may raise errors during conversion.
Example like this:

.. code:: python

    import warnings
    warnings.filterwarnings('ignore')
    import stereo as st

    # read the gef file
    mouse_data_path = './stereomics.h5'
    data = st.io.read_gef(file_path=mouse_data_path, bin_size=50)
    data.tl.cal_qc()

    # Must save raw data before sctransform.
    data.tl.raw_checkpoint()

    # Be carefule with sctransform before the conversion.
    data.tl.sctransform(res_key='sctransform', inplace=True)

    # You can use other functions as you want, like pca and so on.
    data.tl.pca(use_highly_genes=False, n_pcs=30, res_key='pca')

    # conversion
    adata = st.io.stereo_to_anndata(data,flavor='seurat',output='out.h5ad')

h5ad to rds file
----------------------------------
The output h5ad could be converted into rds file by `annh5ad2rds.R <https://github.com/BGIResearch/stereopy/blob/dev/docs/source/_static/annh5ad2rds.R>`_.

It will generate a h5seurat file at first and then generate a rds file.

You can run this script in your own R environment:

.. code:: bash

    Rscript annh5ad2rds.R --infile <h5ad file> --outfile <rds file>
