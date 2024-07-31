import { CommonLogoConfig } from "./model/CommonLogoConfig";

const logosPath = "/common_logos/"

// Array - O(n) lookup
const commonLogos = [
    {
        appLogoPath: `${logosPath}dine.png`,
        width: 195,
        height: 97,
        description: "DINE logo - Grupo de Dispositivos Nanoestruturados",
    },
    {
        appLogoPath: `${logosPath}namor.png`,
        width: 195,
        height: 83,
        description: "NAMOR logo - Nanoscience Modelling in Rio",
    },
    {
        appLogoPath: `${logosPath}ufrj.png`,
        width: 78,
        height: 103,
        description: "UFRJ logo - Universidade Federal do Rio de Janeiro",
    },
    {
        appLogoPath: `${logosPath}ufpr.png`,
        width: 111,
        height: 78,
        description: "UFPR logo- Universidade Federal do Paraná",
    }
]

export default commonLogos