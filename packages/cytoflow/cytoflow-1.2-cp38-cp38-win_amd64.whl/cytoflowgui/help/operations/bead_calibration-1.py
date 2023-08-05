import cytoflow as flow
import_op = flow.ImportOp()
import_op.tubes = [flow.Tube(file = "tasbe/rby.fcs")]
ex = import_op.apply()

bead_op = flow.BeadCalibrationOp()
beads = 'RCP-30-5A Lot AA01, AA02, AA03, AA04, AB01, AB02, AC01 & GAA01-R'
bead_op.beads = flow.BeadCalibrationOp.BEADS[beads]
bead_op.units = {"Pacific Blue-A" : "MEBFP",
                 "FITC-A" : "MEFL",
                 "PE-Tx-Red-YG-A" : "MEPTR"}

bead_op.beads_file = "tasbe/beads.fcs"

bead_op.estimate(ex)

bead_op.default_view().plot(ex)

ex = bead_op.apply(ex)