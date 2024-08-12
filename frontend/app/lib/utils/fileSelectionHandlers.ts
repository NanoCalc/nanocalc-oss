import { RegularButton } from "../model/NanocalcAppConfig";


export const handleRegularButtonClick = function (index: number) {
    const fileInput = document.getElementById(`regularButtonInput${index}`) as HTMLInputElement;
    const fileNameDisplay = document.getElementById(`fileNameDisplay${index}`);
    if (!fileInput || !fileNameDisplay) {
        return;
    }; 

    fileInput.click();

    fileInput.onchange = () => {
        if (fileInput?.files && fileInput.files.length > 0) {
            const fileName = fileInput.files[0].name;
            fileNameDisplay.textContent = fileName;
        }
    };
}

export const handleCalculateButtonClick = async (regularButtons: RegularButton[], appId: string) => {
    const API_ENDPOINT = `http://127.0.0.1:8080/upload/${appId}`
    const FORM_FIELD = 'NANOCALC_USER_UPLOADED_FILES'
    const formData = new FormData();

    regularButtons.forEach((_, index: number) => {
        const fileInput = document.getElementById(`regularButtonInput${index}`) as HTMLInputElement;

        Array.from(fileInput?.files ?? []).forEach(file => {
            formData.append(FORM_FIELD, file, file.name);
        });

    });

    // console.group('FormData Contents');
    // for (let [key, value] of formData.entries()) {
    //     console.log(`${key}:`, value);
    // }
    // console.groupEnd();

    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            body: formData,
        });
        
        
        const responseData = await response.json()
        if (response.ok) {
            
            console.log('Server response:', responseData);
            console.log('Files successfully uploaded!');
        } else {
            console.error('file.upload.error status code:', response.statusText);
            console.error('file.upload.error message:', responseData.message);
        }
    } catch (error) {
        console.error('generic.network.error:', error);
    }
};