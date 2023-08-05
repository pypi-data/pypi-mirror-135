import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "Plate01/RFP_Well_A3.fcs",
                             conditions = {'Dox' : 10.0}),
                   flow.Tube(file = "Plate01/CFP_Well_A4.fcs",
                             conditions = {'Dox' : 1.0})]
import_op.conditions = {'Dox' : 'float'}
ex = import_op.apply()

ch_op = flow.ChannelStatisticOp(name = 'MeanByDox',
                    channel = 'Y2-A',
                    function = flow.geom_mean,
                    by = ['Dox'])
ex2 = ch_op.apply(ex)
ch_op_2 = flow.ChannelStatisticOp(name = 'SdByDox',
                      channel = 'Y2-A',
                      function = flow.geom_sd,
                      by = ['Dox'])
ex3 = ch_op_2.apply(ex2)

flow.Stats2DView(variable = 'Dox',
                 xstatistic = ('MeanByDox', 'geom_mean'),
                 xscale = 'log',
                 ystatistic = ('SdByDox', 'geom_sd'),
                 yscale = 'log').plot(ex3)