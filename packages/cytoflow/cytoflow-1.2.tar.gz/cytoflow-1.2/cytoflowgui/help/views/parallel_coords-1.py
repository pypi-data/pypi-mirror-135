import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "Plate01/RFP_Well_A3.fcs",
                             conditions = {'Dox' : 10.0}),
                   flow.Tube(file = "Plate01/CFP_Well_A4.fcs",
                             conditions = {'Dox' : 1.0})]
import_op.conditions = {'Dox' : 'float'}
ex = import_op.apply()

flow.ParallelCoordinatesView(channels = ['B1-A', 'V2-A', 'Y2-A', 'FSC-A'],
                             scale = {'Y2-A' : 'log',
                                      'V2-A' : 'log',
                                      'B1-A' : 'log',
                                      'FSC-A' : 'log'},
                             huefacet = 'Dox').plot(ex)