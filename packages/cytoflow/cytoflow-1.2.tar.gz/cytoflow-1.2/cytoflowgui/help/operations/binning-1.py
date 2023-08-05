import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "tasbe/rby.fcs")]
ex = import_op.apply()

bin_op = flow.BinningOp()
bin_op.name = "Bin"
bin_op.channel = "FITC-A"
bin_op.scale = "log"
bin_op.bin_width = 0.2

ex2 = bin_op.apply(ex)

bin_op.default_view().plot(ex2)