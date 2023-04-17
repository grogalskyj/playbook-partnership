import python from '@/utils/python'
import { BokehPlot } from '@/components/viz/bokeh'
import { MetaNode } from '@/spec/metanode'
import { GeneCountMatrix } from '@/components/data/gene_count_matrix'
import { scatterplot_icon } from '@/icons'
import { GMT } from '@/components/data/gene_matrix_transpose'

export const UMAPBokehPlotFromGeneCountMatrix = MetaNode('UMAPBokehPlotFromGeneCountMatrix')
  .meta({
    label: 'UMAP Bokeh Plot From Gene Count Matrix',
    description: 'Construct UMAP bokeh plot From gene count matrix',
    icon: [scatterplot_icon],
  })
  .inputs({ matrix: GeneCountMatrix })
  .output(BokehPlot)
  .resolve(async (props) => await python(
    'components.data.umap_transformation.umap_transformation',
    { kargs: [props.inputs.matrix] },
  ))
  .story(props =>
    `The gene count matrix was then visualized as a UMAP plot${''/* [FIGURE]*/}.`
  )
  .build()



export const UMAPBokehPlotFromGMT = MetaNode('UMAPBokehPlotFromGMT')
  .meta({
    label: 'UMAP Bokeh Plot from Gene Sets',
    description: 'Construct a UMAP bokeh plot from many differnt gene sets',
    icon: [scatterplot_icon],
  })
  .inputs({ GMT: GMT })
  .output(BokehPlot)
  .resolve(async (props) => await python('components.data.umap_transformation.umap_transformation_GMT)',
    { kargs: [props.inputs.GMT.set] }))