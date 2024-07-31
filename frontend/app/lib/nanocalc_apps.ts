const logosPath = "/nanocalc_apps_logos/";

// Hash table - O(1) lookup
const nanocalcApps = {
    "FRET-Calc": {
        appLogoPath: `${logosPath}fretcalc_logo.svg`,
        appName: "FRET-Calc"
    },
    "RI-Calc": {
        appLogoPath: `${logosPath}ricalc_logo.svg`,
        appName: "RI-Calc"
    },
    "PLQ-Sim": {
        appLogoPath: `${logosPath}plqsim_logo.svg`,
        appName: "PLQ-Sim"
    },
    "TMM-Sim": {
        appLogoPath: `${logosPath}tmmsim_logo.svg`,
        appName: "TMM-Sim"
    }
};

export default nanocalcApps;
