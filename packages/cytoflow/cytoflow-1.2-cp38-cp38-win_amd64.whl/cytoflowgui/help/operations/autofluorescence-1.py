import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "tasbe/rby.fcs")]
ex = import_op.apply()

af_op = flow.AutofluorescenceOp()
af_op.channels = ["Pacific Blue-A", "FITC-A", "PE-Tx-Red-YG-A"]
af_op.blank_file = "tasbe/blank.fcs"

af_op.estimate(ex)
af_op.default_view().plot(ex)