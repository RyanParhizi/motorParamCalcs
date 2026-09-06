import numpy as np
import matplotlib.pyplot as plt
from main import calc_R_M, calc_k, calc_B_T_INT, calc_J

Vdc_stall = np.array([0.57, 1.50, 2.12, 3.06, 4.12, 4.92, 6.43])   # [V]  V_DC+
VI_stall  = np.array([0.040, 0.101, 0.136, 0.195, 0.250, 0.289, 0.344])  # [V]

Vdc_free = np.array([1.55, 1.98, 2.36, 2.68, 3.36, 3.80,
                      3.97, 4.49, 4.94, 5.26, 5.67, 6.14])          # [V]
VI_free  = np.array([0.043, 0.049, 0.047, 0.052, 0.052, 0.055,
                      0.058, 0.059, 0.064, 0.067, 0.070, 0.071])    # [V]
fenc     = np.array([198, 305, 386, 526, 667, 806,
                      917, 1025, 1150, 1310, 1380, 1490])           # [Hz]


R_M, I_DC_stall, V_MOTOR_stall, p_fit = calc_R_M(Vdc_stall, VI_stall)
k, k_i, omega = calc_k(Vdc_free, VI_free, fenc, R_M)
B, T_INT, T_fit, T, omega = calc_B_T_INT(Vdc_free, VI_free, fenc, k)
j = calc_J(B, 3.3, T_INT, 1490)


print(f"R_M = {R_M:.4f} ohm")
print(f"k = {k:.6f} Nm/A")
print(f"B = {B:.6f} Nms/rad")
print(f"T_INT = {T_INT:.6f} Nm")
print(f"J = {j:.6f} kgm^2")


fig, axs = plt.subplots(1, 3, figsize=(15, 4.5))

axs[0].scatter(I_DC_stall, V_MOTOR_stall, label="Measured")
axs[0].plot(I_DC_stall, p_fit, "r--", label=f"Fit: R_M={R_M:.3f} ohm")
axs[0].set_xlabel("I_DC [A]")
axs[0].set_ylabel("V_MOTOR [V]")
axs[0].set_title("R_M")
axs[0].legend()
axs[0].grid(True)

axs[1].scatter(omega, k_i, label="k_i")
axs[1].axhline(k, color="r", linestyle="--", label=f"k={k:.3f} Nm/A")
axs[1].set_xlabel("omega [rad/s]")
axs[1].set_ylabel("k_i [Nm/A]")
axs[1].set_title("k")
axs[1].legend()
axs[1].grid(True)

axs[2].scatter(omega, T, label="T = k*I_DC")
axs[2].plot(omega, T_fit, "r--", label=f"Fit: B={B:.4f}, T_INT={T_INT:.3f}")
axs[2].set_xlabel("omega [rad/s]")
axs[2].set_ylabel("T [Nm]")
axs[2].set_title("B and T_INT")
axs[2].legend()
axs[2].grid(True)

plt.tight_layout()
plt.show()