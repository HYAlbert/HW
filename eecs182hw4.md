# EECS 182 HW4

## ECE 182 Homework Assignment

Design a MIC single stage amplifier using SMC. Follow the steps below to do your design.

1. Check amplifier stability at the input and output; if the device is not unconditionally stable, draw the stability circles at the input and output.
2. If the device is conditionally stable, add loss at the output to make it unconditionally stable.
3. Compute the new scattering parameters for the device with the resistor added for stability.
4. Calculate maximum stable gain of the new device (original plus resistor).
5. Compute \Gamma_{ML} and \Gamma_{MS} and select the correspondent passive loads.
6. Use the Smith chart to design the input and output matching networks using discrete L, C networks.
7. Design the bias network for the device including the decoupling capacitors.
8. Provide a good draw to scale of the circuit layout.

---

## Device Parameters and Dimensions

*Note: Angles are in degrees and magnitude in linear scale.*

### S-Parameter Table (5.0 GHz)


| freq | magS11 | angS11 | magS21 | angS21 | magS12 | angS12 | magS22 | angS22 |
| ---- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| 5.0  | 0.4    | 23     | 2.0    | 11     | 0.2    | 46     | 0.839  | -66    |


---

### 77 Package

- **Pin configuration (top-down):**
  - **Pin 4:** SOURCE (top)
  - **Pin 1:** GATE (left)
  - **Pin 3:** DRAIN (right)
  - **Pin 2:** SOURCE (bottom)
---

### 402 Passive Device Dimensions (inches)


| Parameter | Value        |
| --------- | ------------ |
| L         | 0.04 ± 0.004 |
| W         | 0.02 ± 0.004 |
| T         | 0.02 ± 0.004 |
| EB        | 0.01 ± 0.006 |

![HW4 assignment](HW4.JPG)

---

## Problem 1: Stability and Stability Circles

### 1.1 Complex S-Parameters

Convert from magnitude and angle (linear scale, degrees) using $S_{ij} = |S_{ij}|\, e^{j\theta_{ij}}$ with angles in radians. At 5.0 GHz:

| Parameter | Rectangular form $a + jb$ |
| --------- | ------------------------- |
| $S_{11}$  | $0.368 + j0.156$          |
| $S_{21}$  | $1.963 + j0.382$          |
| $S_{12}$  | $0.139 + j0.144$          |
| $S_{22}$  | $0.341 - j0.766$          |

### 1.2 Stability Factor $K$

**Definitions** (Rollett):

$$
\Delta = S_{11}S_{22} - S_{12}S_{21}
$$

$$
K = \frac{1 - |S_{11}|^2 - |S_{22}|^2 + |\Delta|^2}{2\,|S_{12}S_{21}|}
$$

**Numerical values:**
- $\Delta = -0.322 - j0.564$
- $|\Delta| = 0.650$
- $K = 0.698$

**Stability criterion (unconditional stability):** $K > 1$ and $|\Delta| < 1$.

Here $K = 0.698 < 1$, so the device is **conditionally stable**. The input and output stability circles must be drawn to identify safe source and load terminations.

### 1.3 Input Stability Circle (Load Plane, $\Gamma_L$)

Locus of $\Gamma_L$ for which $|\Gamma_{\text{in}}| = 1$.

**Center:**
$$
C_L = \frac{(S_{22} - \Delta S_{11}^*)^*}{|S_{22}|^2 - |\Delta|^2}
$$

**Radius:**
$$
r_L = \frac{|S_{12}S_{21}|}{\left| |S_{22}|^2 - |\Delta|^2 \right|}
$$

**Numerical results:**
- $C_L = 1.94 + j2.16$ (or $|C_L| \approx 2.91$, angle $\approx 48°$)
- $r_L = 1.42$

### 1.4 Output Stability Circle (Source Plane, $\Gamma_S$)

Locus of $\Gamma_S$ for which $|\Gamma_{\text{out}}| = 1$.

**Center:**
$$
C_S = \frac{(S_{11} - \Delta S_{22}^*)^*}{|S_{11}|^2 - |\Delta|^2}
$$

**Radius:**
$$
r_S = \frac{|S_{12}S_{21}|}{\left| |S_{11}|^2 - |\Delta|^2 \right|}
$$

**Numerical results:**
- $C_S = -0.175 + j2.27$ (or $|C_S| \approx 2.28$, angle $\approx 94°$)
- $r_S = 1.53$
