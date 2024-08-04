// Planck constant (h) in eV.s times the speed of light (c) in m/s times 10^9 for conversion from m to nm
const PHOTON_ENERGY_WAVELENGTH = 1239.84193  // eV.nm

export type EnergyUnits = 'Hartree' | 'eV' | 'kJ/mol' | 'kcal/mol' |'cm^-1' | 'nm'


export const conversion_factors_to_eV: Record<EnergyUnits, number | ((nm: number) => number)> = {
    'Hartree': 27.2114,
    'eV': 1,
    'kJ/mol': 0.010364,
    'kcal/mol': 0.0433641,
    'cm^-1': 0.000123986,
    'nm': (nm: number) => PHOTON_ENERGY_WAVELENGTH / nm
}

export const conversion_factors_from_eV: Record<EnergyUnits, number | ((nm: number) => number)> = {
    'Hartree': 1 / 27.2114,
    'eV': 1,
    'kJ/mol': 96.4853,
    'kcal/mol': 23.0605,
    'cm^-1': 8065.54,
    'nm': (eV: number) => PHOTON_ENERGY_WAVELENGTH / eV
}

