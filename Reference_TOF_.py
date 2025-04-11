import math
import numpy as np

def calculate_air_density(t_C: float, RH: float, p: float = 101325.0, Z: float = 1.0) -> float:

    T = t_C + 273.15

    M_a = 0.02896546   # kg/mol (dry air)
    M_v = 0.01801528   # kg/mol (water vapor)
    R_u = 8.314462618  # J/(mol·K)

    e_sat = 610.78 * math.exp((17.27 * t_C) / (t_C + 237.3))

    e = RH / 100.0 * e_sat

    x_v = e / p

    molar_mass_mix = (1 - x_v) * M_a + x_v * M_v
    rho = (p * molar_mass_mix) / (R_u * T * Z)

    return rho

def estimate_z(temperature: float) -> float:
    temperatures = np.array([-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30, 35])
    z_moist = np.array([449.1, 444.6, 440.3, 436.1, 432.1, 428.0, 424.3, 420.5, 416.9, 413.3, 409.4, 406.5, 403.2])
    
    return float(np.interp(temperature, temperatures, z_moist))


def main():
    # Inputs
    distance_cm = 15.4 # Distance in cm
    t_C = 15.9  # °C
    RH = 48.1    # % Relative Humidity
    p = 101325.0 # Pa
    Z = 1.0      # Compressibility factor (ideal)

    rho = calculate_air_density(t_C, RH, p, Z)

    print(f"Temperature: {t_C} °C")
    print(f"Relative Humidity: {RH}%")
    print(f"Atmospheric Pressure: {p} Pa")
    print(f"Air Density: {rho:.4f} kg/m³")


    temperature = t_C
    
    z_estimated = estimate_z(temperature)
    
    print(f"Estimated z (moist) value at {temperature:.1f} °C is: {z_estimated:.2f}")

    speed_of_sound = z_estimated / rho
    print(f"Speed of sound in moist air: {speed_of_sound:.2f} m/s")

    duration = distance_cm / speed_of_sound * 1e4  # Convert to microseconds
    print(f"Duration of sound wave to travel {distance_cm} cm: {duration:.4f} μs")

    sampling_rate = (125/128)*1e6  # samples per second

    # Convert duration in µs to seconds
    duration_s = duration * 1e-6

    # Number of samples
    num_samples = int(round(sampling_rate * duration_s))
    print(f"Number of samples ≈ {num_samples}")
    print(f"Number of samples = {sampling_rate * 291.88e-6}")

if __name__ == "__main__":
    main()
