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
