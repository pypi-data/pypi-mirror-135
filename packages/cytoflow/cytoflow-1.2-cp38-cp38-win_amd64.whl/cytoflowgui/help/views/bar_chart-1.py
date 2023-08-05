import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "Plate01/RFP_Well_A3.fcs",
                             conditions = {'Dox' : 10.0}),
                   flow.Tube(file = "Plate01/CFP_Well_A4.fcs",
                             conditions = {'Dox' : 1.0})]
import_op.conditions = {'Dox' : 'float'}
ex = import_op.apply()

ex2 = flow.ThresholdOp(name = 'Threshold',
                       channel = 'Y2-A',
                       threshold = 2000).apply(ex)

ex3 = flow.ChannelStatisticOp(name = "ByDox",
                              channel = "Y2-A",
                              by = ['Dox', 'Threshold'],
                              function = len).apply(ex2)

flow.BarChartView(statistic = ("ByDox", "len"),
                  variable = "Dox",
                  huefacet = "Threshold").plot(ex3)