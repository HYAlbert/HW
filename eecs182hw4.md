# EECS 182 HW4

## ECE 182 Homework Assignment

Design a MIC single stage amplifier using SMC. Follow the steps below to do your design.

1. Check amplifier stability at the input and output; if the device is not unconditionally stable, draw the stability circles at the input and output.
2. If the device is conditionally stable, add loss at the output to make it unconditionally stable.
3. Compute the new scattering parameters for the device with the resistor added for stability.
4. Calculate maximum stable gain of the new device (original plus resistor).
5. Compute $\Gamma_{ML}$ and $\Gamma_{MS}$ and select the corresponding passive loads.
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
*All numerical values are from [problem_calc.py](problem_calc.py).*

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
- $\Delta = S_{11}S_{22} - S_{12}S_{21} = 0.0276 - j0.564$
- $|\Delta| = 0.565$
- $K = 0.569$

**Stability criterion (unconditional stability):** $K > 1$ and $|\Delta| < 1$.

Here $K = 0.569 < 1$, so the device is **conditionally stable**. The input and output stability circles must be drawn to identify safe source and load terminations.

### 1.3 Input Stability Circle (Load Plane, $\Gamma_L$)

Locus of $\Gamma_L$ for which $|\Gamma_{\text{in}}| = 1$.

**Center:**

$$
C_L = \frac{(S_{22} - \Delta S_{11}^{\ast})^{\ast}}{|S_{22}|^{2} - |\Delta|^{2}}
$$

**Radius:**

$$
r_L = \frac{|S_{12}S_{21}|}{\left| |S_{22}|^2 - |\Delta|^2 \right|}
$$

**Numerical results:**
- $C_L = 1.09 + j1.44$ (or $|C_L| \approx 1.81$, angle $\approx 53°$)
- $r_L = 1.04$

### 1.4 Output Stability Circle (Source Plane, $\Gamma_S$)

Locus of $\Gamma_S$ for which $|\Gamma_{\text{out}}| = 1$.

**Center:**

$$
C_S = \frac{\overline{S_{11} - \Delta \overline{S_{22}}}}{|S_{11}|^2 - |\Delta|^2}
$$

**Radius:**

$$
r_S = \frac{|S_{12}S_{21}|}{\left| |S_{11}|^2 - |\Delta|^2 \right|}
$$

**Numerical results:**
- $C_S = 0.463 + j2.06$ (or $|C_S| \approx 2.11$, angle $\approx 77°$)
- $r_S = 2.51$

![Stability circles (input and output)](stability_circles.png)

---

## Problem 2: Output Loss and New S-Parameters

Add loss at the output so the composite two-port is unconditionally stable, then compute its scattering parameters. The loss is modeled as a **shunt resistor** $R$ at the device output (reference $Z_0 = 50\,\Omega$). The composite two-port is: [Device] → [Shunt R] → load.

### 2.1 Output Loss (Shunt Resistor)

With $Z_0 = 50\,\Omega$ and shunt resistance $R$, the two-port S-parameters of the resistor block are:

$$
S_{11}^{(R)} = S_{22}^{(R)} = \frac{-Z_0}{2R + Z_0}, \qquad S_{12}^{(R)} = S_{21}^{(R)} = \frac{2R}{2R + Z_0}.
$$

**Choice:** $R = 50\,\Omega$ (equal to $Z_0$).

**Numerical values:**
- $S_{11}^{(R)} = S_{22}^{(R)} = -\frac{1}{3} \approx -0.333$
- $S_{12}^{(R)} = S_{21}^{(R)} = \frac{2}{3} \approx 0.667$

### 2.2 Cascade via T-Parameters

Device output is connected to resistor input. The cascade is computed using T-parameters: $\mathbf{T}_{\text{cascade}} = \mathbf{T}_{\text{device}} \cdot \mathbf{T}_{\text{resistor}}$, then convert back to S.

**S → T** (for each two-port):

$$
T_{11} = \frac{-\det(\mathbf{S})}{S_{21}}, \quad T_{12} = \frac{S_{11}}{S_{21}}, \quad T_{21} = \frac{-S_{22}}{S_{21}}, \quad T_{22} = \frac{1}{S_{21}}.
$$

**T → S** (for composite):

$$
{S'}_{11} = \frac{T_{12}}{T_{22}}, \quad {S'}_{21} = \frac{1}{T_{22}}, \quad {S'}_{12} = \frac{\det(\mathbf{T})}{T_{22}}, \quad {S'}_{22} = \frac{-T_{21}}{T_{22}}, \quad \det(\mathbf{T}) = T_{11}T_{22} - T_{12}T_{21}.
$$

### 2.3 New S-Parameters (Composite: Device + Resistor)

| Parameter | Rectangular form $a + jb$   |
| --------- | -------------------------- |
| ${S'}_{11}$ | $0.328 + j0.047$           |
| ${S'}_{21}$ | $1.07 + j0.473$            |
| ${S'}_{12}$ | $0.060 + j0.100$            |
| ${S'}_{22}$ | $-0.137 - j0.261$          |

### 2.4 Stability Verification

$$
\Delta' = {S'}_{11}{S'}_{22} - {S'}_{12}{S'}_{21}, \qquad K' = \frac{1 - |{S'}_{11}|^2 - |{S'}_{22}|^2 + |\Delta'|^2}{2\,|{S'}_{12}{S'}_{21}|}.
$$

**Numerical values:**
- $\Delta' = -0.050 - j0.227$
- $|\Delta'| = 0.233$
- $K' = 3.15$

**Conclusion:** ${K'} > 1$ and $|{\Delta'}| < 1$, so the composite (device with shunt resistor at the output) is **unconditionally stable**.
