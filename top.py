from amaranth import *
from amaranth.build import *

from amaranth_boards.resources import *
from tim import Timer
from icesugar_pro import ICESugarProPlatform

class top(Elaboratable):
    def elaborate(self):
        m = Module()

        # freq = int(platform.default_clk_frequency / 10000)
        # counter = Signal(range(freq + 1))
        counter = Signal(16)

        rgb_led = platform.request("rgb_led")

        m.submodules.r_pwm = r_pwm = Timer(rgb_led.r.o)
        m.submodules.g_pwm = g_pwm = Timer(rgb_led.g.o)
        m.submodules.b_pwm = b_pwm = Timer(rgb_led.b.o)

        brightness = Signal(16, reset=0x1FF)
        direction = Signal(1)

        m.d.comb += [
            r_pwm.arr.eq(0xFFF),
            r_pwm.alignment.eq(0),
            r_pwm.en.eq(1),
            g_pwm.arr.eq(0xFFF),
            g_pwm.alignment.eq(0),
            g_pwm.arr.eq(1),
            b_pwm.arr.eq(0xFFF),
            b_pwm.alignment.eq(0),
            b_pwm.arr.eq(1)
        ]

        m.d.sync += [
            r_pwm.ccr.eq(brightness),
            g_pwm.ccr.eq(brightness),
            b_pwm.ccr.eq(brightness)
        ]

        with m.If(counter == 2500):
            m.d.sync += counter.eq(0)

            with m.If(direction == 0):
                with m.If(brightness == 0xFFF):
                    m.d.sync += [
                        direction.eq(~direction),
                        brightness.eq(brightness - 1)
                    ]

                with m.Else():
                    m.d.sync += brightness.eq(brightness + 1)

            with m.Else():
                with m.If(brightness == 0):
                    m.d.sync += [
                        direction.eq(~direction),
                        brightness.eq(brightness + 1)
                    ]

                with m.Else():
                    m.d.sync += brightness.eq(brightness - 1)

        with m.Else():
            m.d.sync += counter.eq(counter + 1)

        return m 

if __name__ == "__main__":
    platform = ICESugarProPlatform()
    platform.build(top, do_program=True)