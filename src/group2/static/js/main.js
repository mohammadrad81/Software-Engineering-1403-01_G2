document.addEventListener('DOMContentLoaded', function() {
    // Toggle File Upload Section
    const toggleBtn = document.getElementById('toggleUpload');
    const uploadArea = document.getElementById('uploadArea');

    toggleBtn.addEventListener('click', function() {
        uploadArea.classList.toggle('hidden');
    });

    // File Input Validation
    const fileInput = document.getElementById('fileInput');
    const errorMessage = document.getElementById('errorMessage');

    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            if (!file.name.endsWith('.txt')) {
                errorMessage.textContent = 'Please upload only .txt files';
                this.value = '';
            } else {
                errorMessage.textContent = '';
            }
        }
    });

    // Form Submissions with AJAX
    const sentenceForm = document.getElementById('sentenceForm');
    const fileForm = document.getElementById('fileForm');

    sentenceForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        try {
            const formData = new FormData(this);
            const response = await fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });
            const result = await response.json();
            updateResults(result);
        } catch (error) {
            console.error('Error:', error);
        }
    });

    fileForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        try {
            const formData = new FormData(this);
            const response = await fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });
            const result = await response.json();
            updateResults(result);
        } catch (error) {
            console.error('Error:', error);
        }
    });

    function updateResults(result) {
        const resultsSection = document.querySelector('.results-section');
        resultsSection.innerHTML = `
            <div class="result-box">
                <h3>Result:</h3>
                <p>${result.message}</p>
            </div>
        `;
    }
});