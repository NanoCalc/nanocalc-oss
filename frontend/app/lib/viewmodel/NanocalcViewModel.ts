interface SelectedFiles {
    [key: string]: File[]
}

export class NanocalcViewModel {
    private mode: string = '';

    setMode(newMode: string) {
        this.mode = newMode;
    }

    async uploadFiles(appId: string, selectedFiles: SelectedFiles) {
        const API_ENDPOINT = `http://127.0.0.1:8080/upload/${appId}`;
        
        const FILE_ID_FORM_FIELD  = 'NANOCALC_FILE_ID_FORM_FIELD'
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
                    formData.append(FILE_ID_FORM_FIELD , key);
                    formData.append(FILES_FORM_FIELD, file);
                });
            }
        }

        // console.group('FormData Contents');
        // for (let [key, value] of formData.entries()) {
        //     console.log(`${key}:`, value);
        // }
        // console.groupEnd();


        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            body: formData,
        });

        // const parsedResponse = await response.json()
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
        } else {
            console.error('Error uploading files:', response.statusText);
            // console.error('Server message:', parsedResponse.message);
        }
    }
}
