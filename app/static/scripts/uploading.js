function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

window.onload = function() {
    const forms = document.getElementsByClassName('upload');
    Array.from(forms).forEach(form => {
        form.onsubmit = function() {
            showLoading();
        }
    });
}