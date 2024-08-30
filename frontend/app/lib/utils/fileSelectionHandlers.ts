import { RegularButton } from "../model/NanocalcAppConfig";


export const handleRegularButtonClick = function (identifier: string) {
    
    const fileInput = document.getElementById(`regularButtonInput${identifier}`) as HTMLInputElement;
    const fileNameDisplay = document.getElementById(`fileNameDisplay${identifier}`);
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

    regularButtons.forEach((button) => {
        const fileInput = document.getElementById(`regularButtonInput${button.identifier}`) as HTMLInputElement;
        console.log(`Button clicked at index: ${button.identifier}`);

        Array.from(fileInput?.files ?? []).forEach(file => {
            formData.append(FORM_FIELD, file, `${button.identifier}_${file.name}`);
            
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
        
        
        // const responseData = await response.json()
        if (response.ok) {
            
            // console.log('Server response:', responseData);
            console.log('Files successfully uploaded!');

            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = `${appId}_generated_data.zip`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(downloadUrl);
            console.log('Files successfully downloaded!');
        } else {
            // console.error('file.upload.error status code:', response.statusText);
            // console.error('file.upload.error message:', responseData.message);
        }
    } catch (error) {
        console.error('generic.network.error:', error);
    }
};