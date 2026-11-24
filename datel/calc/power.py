"""NIC-Datel: the tool's power, and what the microphones' voltage changes in it — rough.

Sources: PCMD3180 SBASA14A (8-channel PDM recording: IAVDD 11.9 mA at 3.3 V, 11.3 mA at 1.8 V with
AREG shorted to AVDD; IIOVDD 0.7 mA at 3.3 V — at 48 kHz, more at 192 kHz, not given);
SPH0641LU4H-1 Rev B (ultrasonic mode 845 uA typ at 1.8 V, more at 3.3 V by 0.5 * VDD * C * f);
UM3300 (the DK with its camera fails on a 550 mA USB supply: "very close to the consumption").
"""
CONV, MICS, MIC_I18 = 4, 32, 0.845e-3
MIC_C, F_PDM = 10e-12, 3.072e6         # a few pF of trace and input per microphone, assumed


def shield(avdd):
    i_conv = CONV * (11.9e-3 if avdd > 2.5 else 11.3e-3)
    i_mic = MICS * (MIC_I18 + 0.5 * (avdd - 1.8) * MIC_C * F_PDM)
    p_analog = (i_conv + i_mic) * avdd
    p_rest = (CONV * 0.7e-3 + 20e-3) * 3.3        # IOVDD and the clocks at 3.3 V
    return p_analog + p_rest


if __name__ == "__main__":
    dk = 0.55 * 5.0                                  # at least what a 550 mA USB port gives
    for v in (3.3, 1.8):
        p = shield(v)
        print(f"microphones and converters' AVDD at {v} V: shield ~{p:.2f} W; with the DK (>= {dk:.2f} W) ~{p+dk:.2f} W")
    p = shield(3.3) + dk
    for wh, lab in ((11.1, "one 18650, 3000 mAh"), (22.2, "two 18650 in parallel"), (37.0, "a 10 000 mAh power bank")):
        print(f"  {lab:28s} {wh:5.1f} Wh, through a 90 % 5 V converter: ~{wh*0.9/p:.1f} h")

    # --- 1S2P with a boost, or 2S with a buck? (the owner, 23 Nov 2026) --------------------
    # Converter efficiencies assumed typical at ~0.6 A out: boost from one cell 88-92 %, buck from
    # two in series 92-95 %; the DK's own VIN path is an LDO to 5 V (UM3300 §7.4.4), so from
    # 7.4 V it burns (7.4 - 5) / 7.4 of the power.
    print("\nthe same two 18650 (22.2 Wh), ~3.1 W load")
    for lab, eff in (("1S2P + boost to 5 V (88-92 %)", 0.90), ("2S + buck to 5 V (92-95 %)", 0.935),
                     ("2S into the DK's VIN, its LDO", 5.0 / 7.4)):
        print(f"  {lab:34s} ~{22.2*eff/p:.1f} h")

    # --- The N6's core at a lower voltage (DS14791 Rev 2: VOS low 0.81 V up to 600 MHz, VOS high
    # 0.89 V for 800 MHz "with overdrive"); the core's dynamic power ~ V^2 f.
    r = (0.81 / 0.89) ** 2 * (600 / 800)
    print(f"\nthe N6's core at VOS low, 600 MHz, against 800 MHz: {r:.2f} of its dynamic power ({(1-r)*100:.0f} % less)")

    # --- The DK's VIN regulator is a 1117 (the owner read it off the schematic, 23 Nov 2026).
    # UM3417 Table 6 gives its limits: 800 mA at 7 V, 450 mA at 7-9 V, 250 mA at 9-12 V — i.e. a
    # heat limit of about (VIN - 5) x I:
    print("\nthe 1117 on VIN: the heat its own limits allow (UM3417 Table 6)")
    for vin, i in ((7.0, 0.8), (9.0, 0.45), (12.0, 0.25)):
        print(f"  {vin:4.1f} V x {i*1000:3.0f} mA -> {(vin-5)*i:.2f} W")
    print("two cells on it at ~0.6 A:")
    for vin in (8.4, 7.4, 6.4):
        print(f"  {vin:3.1f} V -> {(vin-5)*0.6:.2f} W in the 1117, {(vin-5)/vin*100:.0f} % of the battery burnt")

    # --- The N6 itself (DS14791 Rev 2, Tables 27-29, code from ITCM, HSE, typical at 25 °C and
    # the max at TJ 85 °C): IDDCORE at VDDCORE; IDD (VDD) ~0.3 mA; 1V8 2-5 mA. The NPU is not in them.
    print("\nthe N6's core (VDDCORE), typical 25 C / max at TJ 85 C:")
    for lab, v, i25, i85 in (("800 MHz, VOS high, peripherals off", 0.89, 87.6e-3, 110.8e-3),
                             ("800 MHz, VOS high, all peripherals on", 0.89, 176.0e-3, 203.4e-3),
                             ("600 MHz, VOS low, all peripherals on", 0.81, 142.9e-3, 167.4e-3)):
        p25, p85 = v * i25, v * i85
        # from the cell: TMI3113 to 1.8 V, then the N6's own SMPS to the core, ~85 % each
        print(f"  {lab:38s} {i25*1e3:4.0f} / {i85*1e3:4.0f} mA -> {p25:.2f} / {p85:.2f} W; "
              f"from the cell ~{p25/0.72:.2f} / {p85/0.72:.2f} W, ~{p25/0.72/3.7*1e3:.0f} / {p85/0.72/3.7*1e3:.0f} mA at 3.7 V")

    # --- The whole tool from the cell, on the CNN647B (24 Nov 2026). Each line marked: [sheet]
    # from a datasheet, [est] estimated. "eff" the chain from the cell to that load, rough.
    rows = [
        ("N6 core, 800 MHz, all peripherals [sheet DS14791 T28]", 0.89 * 0.176, 0.72),
        ("N6 VDD, 1V8 analog [sheet T27, T29]", 1.8 * 0.005, 0.85),
        ("HyperRAM 32 MB + octal NOR, working [est]", 0.10, 0.85),
        ("display 4.3\" 800x480, full backlight [sheet MRG4311: 165 mA at 5 V]", 5.0 * 0.165, 0.90),
        ("camera MB1854: 5 Mpx sensor, ToF, IMU [est]", 0.40, 0.85),
        ("4 x PCMD3180 + 32 mics at 1.8 V [sheet: 11.3 mA each, 0.85 mA each]", 1.8 * (4 * 11.3e-3 + 32 * 0.85e-3), 0.72),
        ("clocks: oscillator, 2 buffers, 16 outputs at 24.576 MHz [est]", 0.07, 0.85),
        ("converters' IOVDD, PMIC, the rest [est]", 0.03, 0.85),
    ]
    print("\nthe whole tool, from the cell (CNN647B, a 4.3\" display):")
    tot = 0.0
    for lab, p, eff in rows:
        tot += p / eff
        print(f"  {lab:72s} {p:5.2f} W at the load, {p/eff:5.2f} W from the cell")
    print(f"  {'in all':72s}            {tot:5.2f} W, ~{tot/3.7*1e3:.0f} mA at 3.7 V")
    seven = (0.085 * 3.3 + 0.060 * 16.0) / 0.85   # a bare 7" (NHD sheet): logic + string, through drivers
    print(f"  with a 7\" instead (NHD sheet: 85 mA at 3.3 V + 60 mA at 16 V): +{seven - 5.0*0.165/0.90:.2f} W")
    for wh, lab in ((11.1, "one 18650 / Li-Pol 3000 mAh"), (18.5, "Li-Pol 5000 mAh")):
        print(f"  {lab:28s} {wh:5.1f} Wh -> ~{wh/tot:.1f} h")
