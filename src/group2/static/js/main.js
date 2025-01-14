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
            highlightCorrections(result.input_text, result.corrections, result.correctedText);
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Function to clear previous results
    function highlightCorrections(input_text, corrections, correctedText) {
        const processedTextContainer = document.getElementById('processedText');
        const correctedTextContainer = document.getElementById('correctedTextContainer');
        const text = input_text;

        corrections.sort((a, b) => a.start - b.start);

        let highlightedText = "";
        let lastIndex = 0;

        corrections.forEach(({ start, end, word, candidates }, index) => {
            highlightedText += text.slice(lastIndex, start);

            const suggestions = candidates.map((candidate, i) =>
                `<span class="suggestion" data-index="${index}" data-candidate="${candidate}">${candidate}</span>`).join(', ');

            highlightedText += `<span class="error-word">${word} (${suggestions})</span>`;
            lastIndex = end;
        });

        highlightedText += text.slice(lastIndex);

        if (processedTextContainer) {
            processedTextContainer.innerHTML = `
                <div class="result-box">
                    <h3>غلط های املایی:</h3>
                    <p class="highlighted-text">${highlightedText}</p>
                </div>
            `;
        }

        if (correctedTextContainer) {
            correctedTextContainer.innerHTML = `
                <div class="result-box">
                    <h3>متن پیشنهادی اصلاح شده:</h3>
                    <p id="correctedText" class="corrected-text">${correctedText}</p>
                </div>
            `;
        }

        document.querySelectorAll('.suggestion').forEach(suggestion => {
            suggestion.addEventListener('click', function () {
                const index = parseInt(this.dataset.index, 10);
                const candidate = this.dataset.candidate;

                corrections[index].replacement = candidate;
                const updatedText = applyCorrections(input_text, corrections);
                document.getElementById('correctedText').innerText = updatedText;
            });
        });
    }

    function applyCorrections(text, corrections) {
        let resultText = text;
        let offset = 0;

        corrections.forEach(({ start, end, replacement }) => {
            if (replacement) {
                resultText = resultText.slice(0, start + offset) + replacement + resultText.slice(end + offset);
                offset += replacement.length - (end - start);
            }
        });

        return resultText;
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
            console.log("Server Response:", result);

            highlightCorrections(result.input_text, result.corrections, result.correctedText);
        } catch (error) {
            console.error('Error:', error);
        }
    });
});