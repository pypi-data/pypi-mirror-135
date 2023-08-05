bl_op = flow.BleedthroughLinearOp()
bl_op.controls = {'Pacific Blue-A' : 'tasbe/ebfp.fcs',
                  'FITC-A' : 'tasbe/eyfp.fcs',
                  'PE-Tx-Red-YG-A' : 'tasbe/mkate.fcs'}

bl_op.estimate(ex2)
bl_op.default_view().plot(ex2)

ex3 = bl_op.apply(ex2)