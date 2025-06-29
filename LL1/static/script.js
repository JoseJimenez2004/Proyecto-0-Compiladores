document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const resultContainer = document.getElementById('resultContainer');
    const validationResult = document.getElementById('validationResult');
    const fileContent = document.getElementById('fileContent');
    
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('grammarFile');
        const file = fileInput.files[0];
        
        if (!file) {
            alert('Por favor selecciona un archivo');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', file);
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                validationResult.textContent = data.error;
                validationResult.className = 'invalid';
            } else {
                validationResult.textContent = data.message;
                validationResult.className = data.success ? 'valid' : 'invalid';
                fileContent.textContent = data.content;
            }
            
            resultContainer.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            validationResult.textContent = 'Error al procesar el archivo';
            validationResult.className = 'invalid';
            resultContainer.classList.remove('hidden');
        });
    });
});