import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "Plate01/RFP_Well_A3.fcs",
                             conditions = {'Dox' : 10.0}),
                   flow.Tube(file = "Plate01/CFP_Well_A4.fcs",
                             conditions = {'Dox' : 1.0})]
import_op.conditions = {'Dox' : 'float'}
ex = import_op.apply()

p = flow.PolygonOp(name = "Polygon",
                   xchannel = "V2-A",
                   ychannel = "Y2-A")
p.vertices = [(23.411982294776319, 5158.7027015021222),
              (102.22182270573683, 23124.058843387455),
              (510.94519955277201, 23124.058843387455),
              (1089.5215641232173, 3800.3424832180476),
              (340.56382570202402, 801.98947404942271),
              (65.42597937575897, 1119.3133482602157)]

p.default_view(huefacet = "Dox",
               xscale = 'log',
               yscale = 'log').plot(ex)