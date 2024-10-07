function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

let formdata;
function showConfirmationCard(datasetName) {
    document.getElementById('dataset-name').innerText = datasetName;
    document.getElementById('confirmation-card').style.display = 'block';
}

function hideConfirmationCard() {
    document.getElementById('confirmation-card').style.display = 'none';
}

let formData;
window.onload = function() {
    const forms = document.getElementsByClassName('upload');
    Array.from(forms).forEach(form => {
        form.onsubmit = async function(event) {
            showLoading();
            event.preventDefault();

            try {
                formData = new FormData(form)
                const response = await fetch(form.action, {
                    method: form.method,
                    body: formData
                });

                hideLoading()
                if (response.status == 400) {
                    showConfirmationCard(form.name.value)
                } else if (!response.ok) {
                    const result = await response.json();
                    throw new Error(result.detail)
                }
            } catch (error) {
                console.error('Error when uploading the dataset: ', error.message)
                alert(error.message)
            }
        }
    });

    document.getElementById('confirm-btn').onclick = async function() {
        hideConfirmationCard();
        showLoading();

        try {
            const response = await fetch('/upload/dataset/force', {
                method: 'POST',
                body: formData
            });

            hideLoading()
            if (!response.ok) {
                const result = await response.json();
                throw new Error(result.detail)
            }
        } catch (error) {
            console.error('Error when uploading the dataset: ', error.message)
            alert(error.message)
        }
    };

    document.getElementById('cancel-btn').onclick = function() {
        hideConfirmationCard();
        hideLoading();
    };
}