import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "Plate01/RFP_Well_A3.fcs",
                             conditions = {'Dox' : 10.0}),
                   flow.Tube(file = "Plate01/CFP_Well_A4.fcs",
                             conditions = {'Dox' : 1.0})]
import_op.conditions = {'Dox' : 'float'}
ex = import_op.apply()

quad = flow.QuadOp(name = "Quad",
                   xchannel = "V2-A",
                   xthreshold = 100,
                   ychannel = "Y2-A",
                   ythreshold = 1000)

qv = quad.default_view(xscale = 'log', yscale = 'log')
qv.plot(ex)