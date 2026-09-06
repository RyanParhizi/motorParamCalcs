"""
Class: ECEN 2270
File Purpose: Calculating motor parameters
DC Motor Parameter Extraction:  R_M, k, B, T_INT, J
"""

import numpy as np
import math

# =========================================================
# CONSTANTS
# =========================================================
R_eq = 1 / 6            # [ohm]  current-sense resistor network (R1..R6 || combo)
GEAR_PULSES = 960       # encoder counts per wheel revolution (8 pulses/rev x 120:1 gearbox)

# =========================================================
# Auxiliary Functions
# =========================================================
def omega_from_fenc(fenc):
    """Convert encoder frequency [Hz] to angular WHEEL speed [rad/s]."""
    return (2 * np.pi / GEAR_PULSES) * fenc

# =========================================================
# R_M
# =========================================================
def calc_R_M(Vdc_stall, VI_stall):
    I_DC_stall    = VI_stall / R_eq                 # [A]
    V_MOTOR_stall = Vdc_stall - VI_stall             # [V]  V_MOTOR = V_DC+ - V_I

    p1 = np.polyfit(I_DC_stall, V_MOTOR_stall, 1)
    R_M, b1 = p1[0], p1[1]
    p_fit = np.polyval(p1, I_DC_stall)

    return R_M, I_DC_stall, V_MOTOR_stall, p_fit
# =========================================================
# k
# =========================================================
def calc_k(Vdc_free, VI_free, fenc, R_M):

    I_DC_free    = VI_free / R_eq
    V_MOTOR_free = Vdc_free - VI_free
    omega        = omega_from_fenc(fenc)

    V_EMF = V_MOTOR_free - R_M * I_DC_free
    k_i = V_EMF / omega

    k_mean   = np.mean(k_i)
    k_median = np.median(k_i)
    k = k_mean  

    return k, k_i, omega

# =========================================================
# B, T_INT
# =========================================================
def calc_B_T_INT(Vdc_free, VI_free, fenc, k):

    I_DC_free    = VI_free / R_eq
    V_MOTOR_free = Vdc_free - VI_free
    omega        = omega_from_fenc(fenc)

    T = k * I_DC_free
    p2 = np.polyfit(omega, T, 1)
    B, T_INT = p2[0], p2[1]
    T_fit = np.polyval(p2, omega)

    return B, T_INT, T_fit, T, omega

# =========================================================
# J
# =========================================================
def calc_J(B, tau, T_INT, f): 
    w = omega_from_fenc(f)
    J = - (B * tau) / math.log((T_INT)/(B*w + T_INT)) 

    return J