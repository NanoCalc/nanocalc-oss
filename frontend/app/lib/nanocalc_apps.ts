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
                text: "Click to calculate",
                isCalculate: true
            }
        ]
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
                text: "Click to calculate optical constants",
                isCalculate: true
            },
            {
                text: "Click to calculate n",
                isCalculate: true
            }
        ]
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
                text: "Click to calculate Donor Excitation",
                isCalculate: true
            },
            {
                text: "Click to calculate Acceptor Excitation",
                isCalculate: true
            }
        ]
    },
    "TMM-Sim": {
        appLogoPath: `${logosPath}tmmsim_logo.svg`,
        appName: "TMM-Sim",
        buttons: []
    }
};

export default nanocalcApps;
