document.addEventListener('DOMContentLoaded', (event) => {
    // Function to handle form submissions without page refresh
    function handleSubmit(event, formId, action) {
        event.preventDefault();
        const form = document.getElementById(formId);
        const formData = new FormData(form);
        fetch(action, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            if (data === 'Username already exists' || data === 'Invalid username or password') {
                alert(data);
            } else {
                window.location.href = data;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }

    // Register form
    if (document.getElementById('registerForm')) {
        document.getElementById('registerForm').addEventListener('submit', function(event) {
            handleSubmit(event, 'registerForm', '/register');
        });
    }

    // Login form
    if (document.getElementById('loginForm')) {
        document.getElementById('loginForm').addEventListener('submit', function(event) {
            handleSubmit(event, 'loginForm', '/login');
        });
    }

    // Post creation form
    if (document.getElementById('postForm')) {
        document.getElementById('postForm').addEventListener('submit', function(event) {
            handleSubmit(event, 'postForm', '/post');
        });
    }
});