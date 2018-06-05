# IPKISS - Parametric Design Framework
# Copyright (C) 2002-2012  Ghent University - imec
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# i-depot BBIE 7396, 7556, 7748
#
# Contact: ipkiss@intec.ugent.be

if __name__ == "__main__":
    from technologies.si_photonics.picazzo.default import *
from ipkiss.all import *
from ipkiss.plugins.photonics.wg.basic import *  # basic waveguides
from picazzo.filters.mmi_shallow import ShallowMmi1x2Tapered  # MMI
from picazzo.io.column import *  # Standard io columns
from picazzo.io.fibcoup import IoFibcoupGeneric  # generic fibcoup adapter
from genericpdk.library.fibcoup import *

#######################################
# Demonstration on how to use different fiber couplers to a single structure
#######################################


class PicazzoExample5(Structure):
    def define_elements(self, elems):
        layout = layout = IoColumnGroup(
            y_spacing=25.0, south_east=(6000.0, 0.0), adapter=IoFibcoupGeneric
        )  # Note: default fiber coupler is changed!

        # alignment waveguide
        wg_def = WgElDefinition()
        align_wg = wg_def(shape=[(0.0, 0.0), (50.0, 0.0)])
        align = Structure(name="align", elements=[align_wg], ports=align_wg.ports)
        layout += align  # adds default fiber couplers
        layout.add(
            align, west_fibcoups=[STANDARD_GRATING_1550_TM()]
        )  # with 1550-TM fiber couplers on the left side

        # 2x2 mmi
        MMI = ShallowMmi1x2Tapered(width=3, length=5, wg_offset=0.5, taper_width=1.0)
        layout += MMI  # standard fibcoups
        layout.add(
            MMI,
            west_fibcoups=[STANDARD_GRATING_1300_TE()],
            east_fibcoups=[STANDARD_GRATING_1550_TM()],
        )  # with 1300 fiber couplers on the left side, and TM on the right side

        layout.add(
            MMI, west_fibcoups=[STANDARD_GRATING_1550_TE(), STANDARD_GRATING_1300_TE()]
        )  # on the left side, the bottom fiber coupler is 1550, the second one 1300.
        # if there are more than 2 ports on the left side, the fiber couplers are cycled. You can add more fiber couplers,
        # and the adapter will go down the list. You can add this cycle behaviour to almost all parameters of the generic fiber coupler
        # only beware of structures with ports of different process layers (e.g. multi-layer circuits). This does not yet work correctly.

        elems += layout
        return elems


if __name__ == "__main__":
    layout = PicazzoExample5(name="layout")
    # -------- export to GDS2 : instead of manually making a library, we can use this convenient shortcut-function to export a structure
    layout.write_gdsii("example5.gds")
    # -------- verify the fabrication materials with a 2D visualization
    from ipkiss.plugins.vfabrication import *

    layout.visualize_2d()
    # -------- export a GDS file with the virtual fabrication
    layout.write_gdsii_vfabrication("example5_vfab.gds")
