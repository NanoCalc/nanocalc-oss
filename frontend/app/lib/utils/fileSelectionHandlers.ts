import { RegularButton } from "../model/NanocalcAppConfig";

const VPS_API_ENDPOINT = ""

export const handleRegularButtonClick = function (index: number) {
    document.getElementById(`regularButtonInput${index}`)?.click()
}

export const handleCalculateButtonClick = async (regularButtons: RegularButton[]) => {
    const formField = 'NANOCALC_USER_UPLOADED_FILES'
    const formData = new FormData();

    regularButtons.forEach((_, index: number) => {
        const fileInput = document.getElementById(`regularButtonInput${index}`) as HTMLInputElement;

        Array.from(fileInput?.files ?? []).forEach(file => {
            formData.append(formField, file, file.name);
        });

    });

    console.group('FormData Contents');
    for (let [key, value] of formData.entries()) {
        console.log(`${key}:`, value);
    }
    console.groupEnd();

    // try {
    //     const response = await fetch(VPS_API_ENDPOINT, {
    //         method: 'POST',
    //         body: formData,
    //     });

    //     if (response.ok) {
    //         console.log('Files successfully uploaded');
    //     } else {
    //         console.error('Error uploading files:', response.statusText);
    //     }
    // } catch (error) {
    //     console.error('Network error:', error);
    // }
};