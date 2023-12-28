import os, shutil
import subprocess

from amaranth.build import *
from amaranth.vendor import LatticeECP5Platform
from amaranth_boards.resources import *


__all__ = ["ICESugarProPlatform"]


class ICESugarProPlatform(LatticeECP5Platform):
    device      = "LFE5U-25F"
    package     = "BG256"
    speed       = "6"
    default_clk = "clk25"
    resources   = [
        Resource(
            "clk25", 0, Pins("P6", dir="i"), Clock(25e6), 
            Attrs(IO_TYPE="LVCMOS33")),

        Resource(
            "rst", 0, PinsN("R9", dir="i"), 
            Attrs(IO_TYPE="LVCMOS33")),

        *LEDResources(
            pins="B11 A11 C11", 
            attrs=Attrs(IO_TYPE="LVCMOS33")),

        RGBLEDResource(0,
            r="B11", g="A11", b="A12", 
            invert=False, attrs=Attrs(IO_TYPE="LVCMOS33")),

        UARTResource(0,
            rx="B9", tx="A9",
            attrs=Attrs(IO_TYPE="LVTTL33", PULLUP=1)),

        *SPIFlashResources(0,
            cs_n="N8", clk="N9", copi="T8", cipo="T7", wp_n="M7", hold_n="N7",
            attrs=Attrs(IO_TYPE="LVCMOS33")),

        *SDCardResources(0,
            dat0="K12", dat1="L12", dat2="F12", dat3="G12", clk="J12", cmd="H12",
            attrs=Attrs(IO_TYPE="LVCMOS33", SLEWRATE="FAST")),

        # Resource("jtag", 1, 
        #     Subsignal("tms",    PinsN("T11", dir="o")),
        #     Subsignal("tck",    PinsN("T10", dir="o")),
        #     Subsignal("tdi",    PinsN("R11", dir="i")),
        #     Subsignal("tdo",    PinsN("M10", dir="o")),
        #     Attrs(IO_TYPE="LVSCMOS33")
        # ),

        # Resource("jtag", 2, 
        #     Subsignal("tms",    PinsN("PL17A", dir="o")),
        #     Subsignal("tck",    PinsN("PL8D", dir="o")),
        #     Subsignal("tdi",    PinsN("PL38A", dir="i")),
        #     Subsignal("tdo",    PinsN("PL17D", dir="o")),
        #     Attrs(IO_TYPE="LVSCMOS33")
        # ),

        SDRAMResource(0,
            clk="R15", cke="L16", cs_n="A14", we_n="A15", ras_n="B16", cas_n="G16",
            ba="G15 BA14",  a="H15 B13 B12 J16 J15 R12 K16 R13 T13 K15 A13 R14 T14",
            dqm="C16 T15", dq="F16 E15 F15 D14 E16 C15 D16 B15 R16 P16 P15 N16 N14 M16 M15 L15",
            attrs=Attrs(IO_TYPE="LVCMOS33", SLEWRATE="FAST")),
    ]

    connectors = [
        Connector("sodimm", 0, "A7"),
    ]

    def toolchain_program(self, products, name):
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call(["icesprog", bitstream_filename])


if __name__ == "__main__":
    from amaranth_boards.test.blinky import *
    ICESugarProPlatform().build(Blinky(), do_program=True)