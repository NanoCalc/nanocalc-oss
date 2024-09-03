import { RegularButton } from "../model/NanocalcAppConfig";
import nanocalcApps from "../nanocalc_apps";

interface SelectedFiles {
    [key: string]: File[]
}
const MAX_FILE_SIZE_MB = 1;
const ALLOWED_EXTENSIONS = ['xlsx', 'dat', 'csv'];

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

    validateAppFiles(appId: string, selectedFiles: SelectedFiles): boolean {
        const expectedIds = this.getAppIdentifiers(appId);
        if (!expectedIds) {
            return false;
        }
        const actualIds = Object.keys(selectedFiles);

        // Every web app needs an input file (first expectedId)
        if (!actualIds.includes(expectedIds[0])) {
            return false;
        }

        switch (appId) {
            case "fretcalc":
                for (const id of expectedIds) {
                    if (!actualIds.includes(id)) {
                        return false;
                    }
                }
                return true;
            case "ricalc":
                const datFiles = ['decadicCoefficient', 'constantK'];
                const foundOptions = datFiles.filter(option => actualIds.includes(option));
                if (foundOptions.length !== 1) {
                    return false;
                }
                return true;
            case "plqsim":
                return true;
            case "tmmsim":
                return true;
            default:
                return false;
        }
    }



    validateFiles(selectedFiles: SelectedFiles, appId: string): string | null {
        // specific app files validation: which keys are required
        if (!this.validateAppFiles(appId, selectedFiles)) {
            return `Please select all required files.`;
        }

        // general app files validation: size, extension and quantity
        for (const key in selectedFiles) {
            if (selectedFiles.hasOwnProperty(key)) {
                const filesArray = selectedFiles[key];


                if (key === 'layerFiles') {
                    if (filesArray.length > 10) {
                        return `Too many files selected. Max limit is 10 files.`;
                    }
                } else if (filesArray.length > 1) {
                    return `Too many files selected. Only one file is allowed.`;
                }

                for (const file of filesArray) {
                    const fileSizeMB = file.size / 1024 / 1024;
                    const fileExtension = file.name.split('.').pop()?.toLowerCase();

                    if (fileSizeMB > MAX_FILE_SIZE_MB) {
                        return `${file.name} is too large. Max size is ${MAX_FILE_SIZE_MB} MB.`;
                    }

                    if (!ALLOWED_EXTENSIONS.includes(fileExtension || '')) {
                        return `${file.name} has an invalid file extension. Allowed extensions are: ${ALLOWED_EXTENSIONS.join(', ')}.`;
                    }
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

        const API_ENDPOINT = `http://127.0.0.1:8080/upload/${appId}`;

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

        // for devtime - prints the detailed upload object
        // const formDataObject = {};
        // for (let [key, value] of formData.entries()) {
        //     let displayValue = value;

        //     if (value instanceof File) {
        //         displayValue = {
        //             name: value.name,
        //             size: value.size,
        //             type: value.type,
        //         };
        //     }

        //     if (formDataObject.hasOwnProperty(key)) {
        //         if (Array.isArray(formDataObject[key])) {
        //             formDataObject[key].push(displayValue);
        //         } else {
        //             formDataObject[key] = [formDataObject[key], displayValue];
        //         }
        //     } else {
        //         formDataObject[key] = displayValue;
        //     }
        // }
        // console.group('Structured FormData Contents');
        // console.log(JSON.stringify(formDataObject, null, 2));
        // console.groupEnd();


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
                // const parsedResponse = await response.json();
                // console.error(`Error uploading files: ${response.statusText}. Server message: ${parsedResponse.message}`)
                return `Error while processing data. Please double check your data and be sure it complies with the expected formatting.`;
            }
        } catch (error) {
            // console.error(`Unknown error during file upload: ${error}`);
            return `Unknown error during file upload. Please try again later.`
        }
    }
}
