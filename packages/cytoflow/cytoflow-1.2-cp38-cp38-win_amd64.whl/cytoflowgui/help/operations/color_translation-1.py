import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "tasbe/mkate.fcs")]
ex = import_op.apply()

color_op = flow.ColorTranslationOp()
color_op.controls = {("Pacific Blue-A", "FITC-A") : "tasbe/rby.fcs",
                     ("PE-Tx-Red-YG-A", "FITC-A") : "tasbe/rby.fcs"}
color_op.mixture_model = True

color_op.estimate(ex)
color_op.default_view().plot(ex)
ex = color_op.apply(ex)