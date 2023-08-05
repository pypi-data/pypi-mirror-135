import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "Plate01/RFP_Well_A3.fcs",
                             conditions = {'Dox' : 10.0}),
                   flow.Tube(file = "Plate01/CFP_Well_A4.fcs",
                             conditions = {'Dox' : 1.0})]
import_op.conditions = {'Dox' : 'float'}
ex = import_op.apply()

r = flow.Range2DOp(name = "Range2D",
                   xchannel = "V2-A",
                   xlow = 10,
                   xhigh = 1000,
                   ychannel = "Y2-A",
                   ylow = 1000,
                   yhigh = 20000)

r.default_view(huefacet = "Dox",
               xscale = 'log',
               yscale = 'log').plot(ex)