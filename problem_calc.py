"""
EECS 182 HW4 — All problem calculations in one file.
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
R = 50

# Shunt resistor two-port S-parameters (uses S11, S21, S12, S22 from Problem 1)
S11_R = -Z0 / (2 * R + Z0)
S22_R = S11_R
S12_R = 2 * R / (2 * R + Z0)
S21_R = S12_R

# Cascade: T_cascade = T_device * T_resistor (device output -> resistor input)
T_d = s_to_t(S11, S12, S21, S22)
T_r = s_to_t(S11_R, S12_R, S21_R, S22_R)
T_c = (
    T_d[0] * T_r[0] + T_d[1] * T_r[2],
    T_d[0] * T_r[1] + T_d[1] * T_r[3],
    T_d[2] * T_r[0] + T_d[3] * T_r[2],
    T_d[2] * T_r[1] + T_d[3] * T_r[3],
)

# Composite S-parameters (S'): device + resistor
Sp11, Sp21, Sp12, Sp22 = t_to_s(*T_c)
Delta_p = Sp11 * Sp22 - Sp12 * Sp21
K_p = (1 - abs(Sp11) ** 2 - abs(Sp22) ** 2 + abs(Delta_p) ** 2) / (
    2 * abs(Sp12 * Sp21)
)


# =============================================================================
# Print all results (for copying into eecs182hw4.md or verification)
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
    print(f"\nR = {R} Ohm, Z0 = {Z0} Ohm")
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
