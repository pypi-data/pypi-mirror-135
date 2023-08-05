import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "tasbe/rby.fcs")]
ex = import_op.apply()

af_op = flow.AutofluorescenceOp()
af_op.channels = ["Pacific Blue-A", "FITC-A", "PE-Tx-Red-YG-A"]
af_op.blank_file = "tasbe/blank.fcs"

af_op.estimate(ex)
ex2 = af_op.apply(ex)

bl_op = flow.BleedthroughLinearOp()
bl_op.controls = {'Pacific Blue-A' : 'tasbe/ebfp.fcs',
                  'FITC-A' : 'tasbe/eyfp.fcs',
                  'PE-Tx-Red-YG-A' : 'tasbe/mkate.fcs'}

bl_op.estimate(ex2)
bl_op.default_view().plot(ex2)

ex2 = bl_op.apply(ex2)