color_op = flow.ColorTranslationOp()
color_op.controls = {("Pacific Blue-A", "FITC-A") : "tasbe/rby.fcs",
                     ("PE-Tx-Red-YG-A", "FITC-A") : "tasbe/rby.fcs"}
color_op.mixture_model = True

color_op.estimate(ex3)
color_op.default_view().plot(ex3)
ex4 = color_op.apply(ex3)