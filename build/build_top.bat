@rem Automatically generated by Amaranth 0.4.dev233+g1802f7f. Do not edit.
@echo off
if defined AMARANTH_ENV_Trellis call %AMARANTH_ENV_Trellis%
if defined AMARANTH_ENV_TRELLIS call %AMARANTH_ENV_TRELLIS%
if [%YOSYS%] equ [""] set YOSYS=
if [%YOSYS%] equ [] set YOSYS=yosys
if [%NEXTPNR_ECP5%] equ [""] set NEXTPNR_ECP5=
if [%NEXTPNR_ECP5%] equ [] set NEXTPNR_ECP5=nextpnr-ecp5
if [%ECPPACK%] equ [""] set ECPPACK=
if [%ECPPACK%] equ [] set ECPPACK=ecppack
%YOSYS% -q -l top.rpt top.ys || exit /b
%NEXTPNR_ECP5% --quiet --log top.tim --25k --package CABGA256 --speed 6 --json top.json --lpf top.lpf --textcfg top.config || exit /b
%ECPPACK% --input top.config --bit top.bit --svf top.svf || exit /b