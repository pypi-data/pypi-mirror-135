import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "Plate01/RFP_Well_A3.fcs",
                             conditions = {'Dox' : 10.0}),
                   flow.Tube(file = "Plate01/CFP_Well_A4.fcs",
                             conditions = {'Dox' : 1.0})]
import_op.conditions = {'Dox' : 'float'}
ex = import_op.apply()


gm_op = flow.GaussianMixtureOp(name = 'Gauss',
                               channels = ['V2-A', 'Y2-A'],
                               scale = {'V2-A' : 'log',
                                        'Y2-A' : 'log'},
                               num_components = 2)
gm_op.estimate(ex)
ex2 = gm_op.apply(ex)
gm_op.default_view().plot(ex2)