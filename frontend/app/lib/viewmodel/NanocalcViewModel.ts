import { RegularButton } from "../model/NanocalcAppConfig";
import nanocalcApps from "../nanocalc_apps";

interface SelectedFiles {
    [key: string]: File[]
}
const MAX_FILE_SIZE_MB = 1;

export class NanocalcViewModel {
    private mode: string = '';
    private nanocalcAppConfig = nanocalcApps

    setMode(newMode: string) {
        this.mode = newMode;
    }

    getAppIdentifiers(appId: string): string[] | null {
        const appConfig = Object.values(this.nanocalcAppConfig).find(app => app.appId === appId);

        if (!appConfig) {
            return null;
        }

        const appIdentifiers: string[] = appConfig.buttons
            .filter((button): button is RegularButton => !button.isCalculate)
            .map(button => button.identifier);

        return appIdentifiers;
    }


    validateFiles(selectedFiles: SelectedFiles, appId: string): string | null {
        if (Object.keys(selectedFiles).length === 0) {
            return `Please fill in all necessary files.`
        }
        const appConfig = Object.values(nanocalcApps).find(app => app.appId === appId);
        const actualIds = Object.keys(selectedFiles);
        if (!appConfig) return 'Invalid application ID.';

        const requiredIdentifiers = appConfig.buttons
            .filter(button => !button.isCalculate)
            .map(button => button.identifier);
        
        if (!actualIds.includes(requiredIdentifiers[0])) {
            return `Please enter an input file.`;
        }

        for (const button of appConfig.buttons) {
            if (!button.isCalculate) {
                const files = selectedFiles[button.identifier];
                if (files) {
                    for (const file of files) {
                        const fileExtension = file.name.split('.').pop()?.toLowerCase();
                        if (fileExtension !== button.expectedExtension) {
                            return `File ${file.name} must have the .${button.expectedExtension} extension.`;
                        }
                    }
                }
            }
        }
        
        switch (appId) {
            case 'fretcalc':
                if (Object.keys(selectedFiles).length !== requiredIdentifiers.length) {
                    return 'All files are required for FRET-Calc.';
                }
                break;
            case 'ricalc':
                const datFiles = ['decadicCoefficient', 'constantK'];
                const foundOptions = datFiles.filter(option => actualIds.includes(option));
                if (foundOptions.length !== 1) {
                    return 'You must provide either the Decadic Abs or K file for RI-Calc.';
                }
                break;
            case 'plqsim':
                if (Object.keys(selectedFiles).length !== 1) {
                    return 'PLQ-Sim requires exactly one file.';
                }
                break;
            case 'tmmsim':
                if (selectedFiles['layerFiles'] && selectedFiles['layerFiles'].length > 10) {
                    return 'You can upload up to 10 layer files for TMM-Sim.';
                }
                break;
            default:
                return 'Invalid application ID.';
        }


        // Validate file size
        for (const key in selectedFiles) {
            const files = selectedFiles[key];
            for (const file of files) {
                if (file.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
                    return `File ${file.name} exceeds the maximum size of ${MAX_FILE_SIZE_MB} MB.`;
                }
            }
        }

        return null;
    }

    async uploadFiles(appId: string, selectedFiles: SelectedFiles) {
        const validationError = this.validateFiles(selectedFiles, appId);
        if (validationError) {
            return validationError;
        }

        const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
        if (!API_BASE_URL) {
            return `Unable to connect to the server. Please try again later.`
        }
        const API_ENDPOINT = `${API_BASE_URL}/upload/${appId}`;

        const FILE_ID_FORM_FIELD = 'NANOCALC_FILE_ID_FORM_FIELD'
        const FILES_FORM_FIELD = 'NANOCALC_USER_UPLOADED_FILES';
        const MODE_FORM_FIELD = 'NANOCALC_USER_MODE';

        const formData = new FormData();

        if (this.mode) {
            formData.append(MODE_FORM_FIELD, this.mode);
        }

        for (const key in selectedFiles) {
            if (selectedFiles.hasOwnProperty(key)) {
                const filesArray = selectedFiles[key];

                filesArray.forEach(file => {
                    formData.append(FILE_ID_FORM_FIELD, key);
                    formData.append(FILES_FORM_FIELD, file);
                });
            }
        }
        
        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = `${appId}_generated_data.zip`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(downloadUrl);

                return null;
            } else {
                return `Error while processing data. Please double check your data and be sure it complies with the expected formatting.`;
            }
        } catch (error) {
            return `Unknown error during file upload. Please try again later.`
        }
    }
}
