"""
EECS 182 HW4 — All problem calculations.
Variables from earlier problems are reused in later ones.
"""
import cmath


def mag_ang_to_complex(mag, deg):
    """Convert magnitude and angle (degrees) to complex number."""
    return cmath.rect(mag, cmath.pi * deg / 180)


def s_to_t(s11, s12, s21, s22):
    """Convert S-parameters to T-parameters (chain/scattering)."""
    det_s = s11 * s22 - s12 * s21
    return (-det_s / s21, s11 / s21, -s22 / s21, 1 / s21)


def t_to_s(t11, t12, t21, t22):
    """Convert T-parameters to S-parameters."""
    det_t = t11 * t22 - t12 * t21
    return (t12 / t22, 1 / t22, det_t / t22, -t21 / t22)


# =============================================================================
# PROBLEM 1: Stability and stability circles
# =============================================================================

# Raw S-parameter data from table (5.0 GHz; magnitude linear, angle degrees)
magS11, angS11 = 0.4, 23
magS21, angS21 = 2.0, 11
magS12, angS12 = 0.2, 46
magS22, angS22 = 0.839, -66

# Complex S-parameters (used in Problem 2 and later)
S11 = mag_ang_to_complex(magS11, angS11)
S21 = mag_ang_to_complex(magS21, angS21)
S12 = mag_ang_to_complex(magS12, angS12)
S22 = mag_ang_to_complex(magS22, angS22)

# Delta = S11*S22 - S12*S21 (determinant of S-matrix)
Delta = S11 * S22 - S12 * S21

# Rollett stability factor K
K = (1 - abs(S11) ** 2 - abs(S22) ** 2 + abs(Delta) ** 2) / (2 * abs(S12 * S21))

# Input stability circle (load plane): center C_L, radius r_L
den_L = abs(S22) ** 2 - abs(Delta) ** 2
C_L = (S22 - Delta * S11.conjugate()).conjugate() / den_L
r_L = abs(S12 * S21) / abs(den_L)

# Output stability circle (source plane): center C_S, radius r_S
den_S = abs(S11) ** 2 - abs(Delta) ** 2
C_S = (S11 - Delta * S22.conjugate()).conjugate() / den_S
r_S = abs(S12 * S21) / abs(den_S)


# =============================================================================
# PROBLEM 2: Output loss and new S-parameters (device + shunt resistor)
# =============================================================================

Z0 = 50
R_INITIAL = 50.0


def shunt_s_params(R_value: float):
    """Return S-parameters of the shunt resistor two-port for a given R."""
    s11_r = -Z0 / (2 * R_value + Z0)
    s22_r = s11_r
    s12_r = 2 * R_value / (2 * R_value + Z0)
    s21_r = s12_r
    return s11_r, s12_r, s21_r, s22_r


def composite_for_R(R_value: float):
    """Compute composite S-params, Delta', K', and stability circles for a given R."""
    s11_r, s12_r, s21_r, s22_r = shunt_s_params(R_value)

    # Cascade: T_cascade = T_device * T_resistor (device output -> resistor input)
    T_d = s_to_t(S11, S12, S21, S22)
    T_r = s_to_t(s11_r, s12_r, s21_r, s22_r)
    T_c = (
        T_d[0] * T_r[0] + T_d[1] * T_r[2],
        T_d[0] * T_r[1] + T_d[1] * T_r[3],
        T_d[2] * T_r[0] + T_d[3] * T_r[2],
        T_d[2] * T_r[1] + T_d[3] * T_r[3],
    )

    # Composite S-parameters (S'): device + resistor
    sp11, sp21, sp12, sp22 = t_to_s(*T_c)
    delta_p = sp11 * sp22 - sp12 * sp21
    K_p_val = (1 - abs(sp11) ** 2 - abs(sp22) ** 2 + abs(delta_p) ** 2) / (
        2 * abs(sp12 * sp21)
    )

    # Composite stability circles (same formulas as Problem 1)
    den_L_p = abs(sp22) ** 2 - abs(delta_p) ** 2
    C_L_p_val = (sp22 - delta_p * sp11.conjugate()).conjugate() / den_L_p
    r_L_p_val = abs(sp12 * sp21) / abs(den_L_p)

    den_S_p = abs(sp11) ** 2 - abs(delta_p) ** 2
    C_S_p_val = (sp11 - delta_p * sp22.conjugate()).conjugate() / den_S_p
    r_S_p_val = abs(sp12 * sp21) / abs(den_S_p)

    return {
        "R": R_value,
        "S11_R": s11_r,
        "S12_R": s12_r,
        "S21_R": s21_r,
        "S22_R": s22_r,
        "Sp11": sp11,
        "Sp21": sp21,
        "Sp12": sp12,
        "Sp22": sp22,
        "Delta_p": delta_p,
        "K_p": K_p_val,
        "C_L_p": C_L_p_val,
        "r_L_p": r_L_p_val,
        "C_S_p": C_S_p_val,
        "r_S_p": r_S_p_val,
    }


def find_minimum_loss_R():
    """Find largest R (minimum loss) such that K' >= 1 and |Delta'| < 1."""
    # Start from initial R known to be stable
    res_low = composite_for_R(R_INITIAL)
    R_low = R_INITIAL

    # Find an upper bound where K' < 1 (device becomes conditionally stable again)
    R_high = R_low
    res_high = res_low
    # Avoid infinite loop by capping R_high
    while res_high["K_p"] >= 1.0 and R_high < 1e4:
        R_high *= 2.0
        res_high = composite_for_R(R_high)

    # If even very large R still gives K' >= 1, just use that as minimum-loss R
    if res_high["K_p"] >= 1.0:
        return res_high

    # Binary search between R_low and R_high for K' ~= 1
    for _ in range(40):
        R_mid = 0.5 * (R_low + R_high)
        res_mid = composite_for_R(R_mid)
        if res_mid["K_p"] >= 1.0 and abs(res_mid["Delta_p"]) < 1.0:
            R_low = R_mid
            res_low = res_mid
        else:
            R_high = R_mid

    return res_low


# Boundary: largest R (minimum loss) for which K' >= 1 (marginally stable at that R)
_min_loss_result = find_minimum_loss_R()
R_boundary = _min_loss_result["R"]  # ~299.3 Ohm

# Chosen R = 50 Ohm for design (unconditionally stable, K' > 1)
R_CHOSEN = 50
_result = composite_for_R(R_CHOSEN)

R = R_CHOSEN
S11_R = _result["S11_R"]
S12_R = _result["S12_R"]
S21_R = _result["S21_R"]
S22_R = _result["S22_R"]

Sp11 = _result["Sp11"]
Sp21 = _result["Sp21"]
Sp12 = _result["Sp12"]
Sp22 = _result["Sp22"]
Delta_p = _result["Delta_p"]
K_p = _result["K_p"]

# Composite stability circles (for loss_circle.png)
C_L_p = _result["C_L_p"]
r_L_p = _result["r_L_p"]
C_S_p = _result["C_S_p"]
r_S_p = _result["r_S_p"]


# =============================================================================
# PROBLEM 3: Maximum stable gain of composite device
# =============================================================================

G_MSG = abs(Sp21 / Sp12)


# =============================================================================
# PROBLEM 4: Gamma_ML and Gamma_MS (simultaneous conjugate match)
# =============================================================================
# For composite S' (Sp11, Sp12, Sp21, Sp22), Delta' = Sp11*Sp22 - Sp12*Sp21.
# B1, C1 for source match (Gamma_MS); B2, C2 for load match (Gamma_ML).
# Choose root so |Gamma| < 1 (passive termination).

B1 = 1 + abs(Sp11) ** 2 - abs(Sp22) ** 2 - abs(Delta_p) ** 2
C1 = Sp11 - Delta_p * Sp22.conjugate()
disc1 = B1**2 - 4 * abs(C1) ** 2
# Minus sign gives |Gamma_MS| < 1
Gamma_MS = (B1 - cmath.sqrt(disc1)) / (2 * C1) if abs(C1) > 1e-12 else 0

B2 = 1 + abs(Sp22) ** 2 - abs(Sp11) ** 2 - abs(Delta_p) ** 2
C2 = Sp22 - Delta_p * Sp11.conjugate()
disc2 = B2**2 - 4 * abs(C2) ** 2
# Minus sign gives |Gamma_ML| < 1
Gamma_ML = (B2 - cmath.sqrt(disc2)) / (2 * C2) if abs(C2) > 1e-12 else 0


# =============================================================================
# Print all results
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PROBLEM 1: Stability and stability circles")
    print("=" * 60)
    print("\nComplex S-parameters (rectangular):")
    print(f"  S11 = {S11.real:.4f} + j{S11.imag:.4f}")
    print(f"  S21 = {S21.real:.4f} + j{S21.imag:.4f}")
    print(f"  S12 = {S12.real:.4f} + j{S12.imag:.4f}")
    s22_str = f"{S22.real:.4f} - j{abs(S22.imag):.4f}" if S22.imag < 0 else f"{S22.real:.4f} + j{S22.imag:.4f}"
    print(f"  S22 = {s22_str}")
    print("\nDelta = S11*S22 - S12*S21:")
    d_str = f"{Delta.real:.4f} - j{abs(Delta.imag):.4f}" if Delta.imag < 0 else f"{Delta.real:.4f} + j{Delta.imag:.4f}"
    print(f"  Delta = {d_str}")
    print(f"  |Delta| = {abs(Delta):.4f}")
    print(f"\nK = {K:.4f}")
    print("\nInput stability circle (load plane):")
    print(f"  C_L = {C_L.real:.4f} + j{C_L.imag:.4f}")
    print(f"  |C_L| = {abs(C_L):.4f}, angle = {cmath.phase(C_L)*180/cmath.pi:.2f} deg")
    print(f"  r_L = {r_L:.4f}")
    print("\nOutput stability circle (source plane):")
    print(f"  C_S = {C_S.real:.4f} + j{C_S.imag:.4f}")
    print(f"  |C_S| = {abs(C_S):.4f}, angle = {cmath.phase(C_S)*180/cmath.pi:.2f} deg")
    print(f"  r_S = {r_S:.4f}")

    print("\n" + "=" * 60)
    print("PROBLEM 2: Output loss and new S-parameters")
    print("=" * 60)
    print(f"\nR_boundary (K'=1) = {R_boundary:.2f} Ohm")
    print(f"R chosen for design = {R} Ohm, Z0 = {Z0} Ohm")
    print(f"S^(R): S11=S22 = {S11_R:.4f}, S12=S21 = {S12_R:.4f}")
    print("\nComposite S' (device + resistor):")
    print(f"  S'11 = {Sp11.real:.4f} + j{Sp11.imag:.4f}")
    print(f"  S'21 = {Sp21.real:.4f} + j{Sp21.imag:.4f}")
    print(f"  S'12 = {Sp12.real:.4f} + j{Sp12.imag:.4f}")
    sp22_str = f"{Sp22.real:.4f} - j{abs(Sp22.imag):.4f}" if Sp22.imag < 0 else f"{Sp22.real:.4f} + j{Sp22.imag:.4f}"
    print(f"  S'22 = {sp22_str}")
    print("\nStability of composite:")
    dp_str = f"{Delta_p.real:.4f} - j{abs(Delta_p.imag):.4f}" if Delta_p.imag < 0 else f"{Delta_p.real:.4f} + j{Delta_p.imag:.4f}"
    print(f"  Delta' = {dp_str}")
    print(f"  |Delta'| = {abs(Delta_p):.4f}")
    print(f"  K' = {K_p:.4f}")

    print("\n" + "=" * 60)
    print("PROBLEM 3: Maximum stable gain of composite device")
    print("=" * 60)
    print(f"\nG_MSG (linear) = {G_MSG:.4f}")
    G_MSG_dB = 20 * cmath.log10(G_MSG).real
    print(f"G_MSG (dB)     = {G_MSG_dB:.2f} dB")

    print("\n" + "=" * 60)
    print("PROBLEM 4: Gamma_ML and Gamma_MS (conjugate match)")
    print("=" * 60)
    def fmt(z):
        s = f"{z.real:.4f}"
        if z.imag >= 0:
            s += f" + j{z.imag:.4f}"
        else:
            s += f" - j{abs(z.imag):.4f}"
        return s
    print(f"\nGamma_MS = {fmt(Gamma_MS)}")
    print(f"  |Gamma_MS| = {abs(Gamma_MS):.4f}")
    print(f"Gamma_ML = {fmt(Gamma_ML)}")
    print(f"  |Gamma_ML| = {abs(Gamma_ML):.4f}")
