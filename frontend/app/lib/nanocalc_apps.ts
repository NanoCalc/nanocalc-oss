import { NanocalcAppConfig } from "./model/NanocalcAppConfig";

const logosPath = "/nanocalc_apps_logos/";

// Hash table - O(1) lookup
const nanocalcApps: NanocalcAppConfig = {
    "FRET-Calc": {
        appLogoPath: `${logosPath}fretcalc_logo.svg`,
        appName: "FRET-Calc",
        buttons: [
            {
                text: "Input file (.xlsx)",
                expectedExtension: "xlsx",
            },
            {
                text: "Extinction coefficient file (.dat)",
                expectedExtension: "dat",
            },
            {
                text: "Emission file (.dat)",
                expectedExtension: "dat",
            },
            {
                text: "Refractive Index file (.dat)",
                expectedExtension: "dat",
            },
            {
                text: "Calculate",
                isCalculate: true
            }
        ],
        articleBanner: {
            title: "FRET-Calc: A free software and web server for Förster Resonance Energy Transfer Calculation",
            doi: "https://doi.org/10.1016/j.cpc.2023.108715",
            sampleData: "https://github.com/NanoCalc/FRETCalc/releases/download/FRETCalc-1.0-alpha/data-sample.zip",
            spectralData: "https://github.com/NanoCalc/FRETCalc/releases/download/FRETCalc-1.0-alpha/spectral-data.zip",
            binaries: "https://github.com/NanoCalc/FRETCalc/releases"
        }
    },
    "RI-Calc": {
        appLogoPath: `${logosPath}ricalc_logo.svg`,
        appName: "RI-Calc",
        buttons: [
            {
                text: "Input file (.xlsx)",
                expectedExtension: "xlsx"
            },
            {
                text: "Decadic Abs. Coefficient file (.dat)",
                expectedExtension: "dat"
            },
            {
                text: " K file (.dat)",
                expectedExtension: "dat"
            },
            {
                text: "Calculate optical constants",
                isCalculate: true
            },
            {
                text: "Calculate n",
                isCalculate: true
            }
        ],
        articleBanner: {
            title: "RI-Calc: A user friendly software and web server for refractive index calculation",
            doi: "https://doi.org/10.1016/j.cpc.2024.109100",
            sampleData: "https://github.com/NanoCalc/RICalc/releases/download/3.0-beta/data_sample.zip",
            spectralData: "https://github.com/NanoCalc/RICalc/releases/download/3.0-beta/spectral-data.zip",
            binaries: "https://github.com/NanoCalc/RICalc/releases"
        }
    },
    "PLQ-Sim": {
        appLogoPath: `${logosPath}plqsim_logo.svg`,
        appName: "PLQ-Sim",
        buttons: [
            {
                text: "Input file (.xlsx)",
                expectedExtension: "xlsx"
            },
            {
                text: "Calculate Donor Excitation",
                isCalculate: true
            },
            {
                text: "Calculate Acceptor Excitation",
                isCalculate: true
            }
        ],
        articleBanner: {
            title: "PLQ-sim: A computational tool for simulating photoluminescence quenching dynamics in organic donor/acceptor blends",
            doi: "https://doi.org/10.1016/j.cpc.2023.109015",
            sampleData: "https://github.com/NanoCalc/PLQ-Sim/releases/download/1.0-beta/data-sample.zip",
            binaries: "https://github.com/NanoCalc/PLQ-Sim/releases"
        }
    },
    "TMM-Sim": {
        appLogoPath: `${logosPath}tmmsim_logo.svg`,
        appName: "TMM-Sim",
        buttons: [
            {
                text: "Input file (.xlsx)",
                expectedExtension: "xlsx",
            },
            {
                text: "up to 10 layer files (.csv)",
                expectedExtension: "csv",
                allowMultiple: true
            },
            {
                text: "Calculate",
                isCalculate: true
            }
        ],
        articleBanner: {
            title: "TMM-Sim: A versatile tool for optical simulation of thin-film solar cells",
            doi: "https://doi.org/10.1016/j.cpc.2024.109206",
            sampleData: "https://github.com/NanoCalc/TMM-Sim/releases/download/v1.0/spectral-data.zip",
            binaries: "https://github.com/NanoCalc/TMM-Sim/releases"
        }
    }
};

export default nanocalcApps;
