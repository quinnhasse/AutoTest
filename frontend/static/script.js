// static/script.js

document.addEventListener('DOMContentLoaded', function() {
    function closeForm() {
        document.getElementById('form').classList.remove('open');
    }

    document.getElementById('heading').addEventListener('click', function() {
        document.getElementById('form').classList.add('open');
    });

    document.querySelector('.form-close-button').addEventListener('click', closeForm);
});