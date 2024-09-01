export class NanocalcViewModel {
    private files: Record<string, File> = {};
    private mode: string = '';

    handleFileChange = (fileIdentifier: string, event: React.ChangeEvent<HTMLInputElement>) => {
        const newFileList = event.target.files;

        if (newFileList) {
            for (const file of Array.from(newFileList)) {
                this.files = {
                    ...this.files,
                    [fileIdentifier]: file
                }
            }
        }

        // console.log(`Files added for ${fileIdentifier}:`);
        // Array.from(newFileList ?? []).forEach((file, index) => {
        //     console.log(`  File ${index + 1}: ${file.name}`);
        // });
    }

    setMode(newMode: string) {
        this.mode = newMode;
    }

    async uploadFiles(appId: string) {
        const API_ENDPOINT = `http://127.0.0.1:8080/upload/${appId}`;
        const FILES_FORM_FIELD = 'NANOCALC_USER_UPLOADED_FILES';
        const MODE_FORM_FIELD = 'NANOCALC_USER_MODE';
        const formData = new FormData();

        if (this.mode) {
            formData.append(MODE_FORM_FIELD, this.mode);
        }

        for (const identifier in this.files) {
            formData.append(FILES_FORM_FIELD, this.files[identifier], identifier);
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
        }
    }
}
