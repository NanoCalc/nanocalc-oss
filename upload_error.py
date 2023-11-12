class UploadError: 
    """
    Represents an error that occurs during the user data upload. 
    
    Attributes: 
    - the type of error (wrong extension or too many files)
    - the file expected by the web app
    - its expected extension  
    - and the app to which the user should be redirected to 

    Methods:
    - to_dict(): returns a dictionary representation of the error object for frontend use
    """
    def __init__(self, error_type, file_name, expected_ext, redirect_url):
        self.error_type = error_type
        self.file_name = file_name
        self.expected_ext = expected_ext
        self.redirect_url = redirect_url

    def to_dict(self):
        """
        Returns all attributes (even if they are None) in a dictionary format
        """
        return {
            "error": self.error_type,
            "file_name": self.file_name,
            "expected_ext": self.expected_ext,
            "redirect": self.redirect_url
        }
