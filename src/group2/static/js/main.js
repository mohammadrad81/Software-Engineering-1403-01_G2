// JavaScript to handle text and file processing
document.addEventListener('DOMContentLoaded', function () {
    const userGuideBtn = document.getElementById("userGuideBtn");
    const userGuidePopup = document.getElementById("userGuidePopup");
    const closeBtn = userGuidePopup.querySelector(".close");

    userGuideBtn.onclick = function() {
        userGuidePopup.style.display = "block";
    }

    closeBtn.onclick = function() {
        userGuidePopup.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == userGuidePopup) {
            userGuidePopup.style.display = "none";
        }
    }
    
    const sentenceForm = document.getElementById('sentenceForm');
    const sentenceInput = document.getElementById('sentence');

    // Handle form submission
    sentenceForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        try {
            const response = await fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
            });

            const result = await response.json();
            console.log("Server Response:", result);
            // clearPreviousResults();
            highlightCorrections(result.corrections, result.correctedText);
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Function to clear previous results
    function highlightCorrections(corrections, correctedText) {
        const resultsSection = document.querySelector('.results-section');
        const highlightedInputText = document.getElementById('highlightedInputText');
        const correctedTextContainer = document.getElementById('correctedTextContainer');
        const processedTextContainer = document.getElementById('processedText');
        const text = sentenceInput.value;

        corrections.sort((a, b) => a.start - b.start);

        let highlightedText = "";
        let lastIndex = 0;

        corrections.forEach(({ start, end, word, candidates }) => {
            highlightedText += text.slice(lastIndex, start);

            const span = `<span class="error-word" title="پیشنهادها: ${candidates.join(', ')}">${word}</span>`;
            highlightedText += span;

            lastIndex = end;
        });

        highlightedText += text.slice(lastIndex);

        if (highlightedInputText) {
            highlightedInputText.innerHTML = highlightedText;
        }

        if (processedTextContainer) {
            processedTextContainer.innerHTML = `
                <div class="result-box">
                    <h3>Processed Text:</h3>
                    <p class="highlighted-text">${highlightedText}</p>
                    <h4>Corrections:</h4>
                    <ul>
                        ${corrections.map(({ word, candidates }) => `
                            <li>
                                <strong>${word}</strong>: پیشنهادها - ${candidates.join(', ')}
                            </li>
                        `).join('')}
                    </ul>
                </div>
            `;
        }

        if (correctedTextContainer) {
            correctedTextContainer.innerHTML = `
                <div class="result-box">
                    <h3>Corrected Text:</h3>
                    <p class="corrected-text">${correctedText}</p>
                </div>
            `;
        }
    }



    // Toggle File Upload Section
    const toggleBtn = document.getElementById('toggleUpload');
    const uploadArea = document.getElementById('uploadArea');

    toggleBtn.addEventListener('click', function () {
        uploadArea.classList.toggle('hidden');
    });

    // File Input Validation
    const fileInput = document.getElementById('fileInput');
    const errorMessage = document.getElementById('errorMessage');

    fileInput.addEventListener('change', function () {
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

    // Handle File Form Submission
    const fileForm = document.getElementById('fileForm');

    fileForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        try {
            const response = await fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
            });

            const result = await response.json();
            clearPreviousResults();
            highlightCorrections(result.corrections, result.correctedText);
        } catch (error) {
            console.error('Error:', error);
        }
    });
});