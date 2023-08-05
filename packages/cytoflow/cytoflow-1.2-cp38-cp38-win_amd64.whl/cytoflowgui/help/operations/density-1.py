import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "Plate01/RFP_Well_A3.fcs",
                             conditions = {'Dox' : 10.0}),
                   flow.Tube(file = "Plate01/CFP_Well_A4.fcs",
                             conditions = {'Dox' : 1.0})]
import_op.conditions = {'Dox' : 'float'}
ex = import_op.apply()


density_op = flow.DensityGateOp(name = 'Density',
                                xchannel = 'FSC-A',
                                xscale = 'log',
                                ychannel = 'SSC-A',
                                yscale = 'log',
                                keep = 0.5)
density_op.estimate(ex)
density_op.default_view().plot(ex)
ex2 = density_op.apply(ex)