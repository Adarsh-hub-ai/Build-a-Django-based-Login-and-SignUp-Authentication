const signupForm = document.getElementById('signup-form');
const signupMessage = document.getElementById('signup-message');
const submitButton = signupForm.querySelector('button[type="submit"]');

signupForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    signupMessage.textContent = '';
    submitButton.disabled = true;

    try {
        const response = await fetch(signupForm.dataset.sendCodeUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': cookie('csrftoken'),
            },
            body: JSON.stringify({
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
            }),

        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || 'Unable to start signup.');
        }
        window.location.href = signupForm.dataset.codePageUrl;
    } catch (error) {
        signupMessage.textContent = error.message || 'A network error occurred. Please try again.';
        submitButton.disabled = false;
    }
});


function cookie(name) {
    const value = document.cookie
        .split('; ')
        .find((row) => row.startsWith(`${name}=`));
    return value ? decodeURIComponent(value.split('=').slice(1).join('=')) : '';
}
