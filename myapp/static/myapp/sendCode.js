const verifyForm = document.getElementById('verify-form');
const verifyMessage = document.getElementById('verify-message');
const verifyButton = verifyForm.querySelector('button[type="submit"]');

verifyForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    verifyMessage.textContent = '';
    verifyButton.disabled = true;

    try {
        const response = await fetch(verifyForm.dataset.verifyUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': cookie('csrftoken'),
            },
            body: JSON.stringify({ code: document.getElementById('otp-code').value }),
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || 'Code verification failed.');
        }
        verifyMessage.textContent = result.message;
        window.location.href = verifyForm.dataset.loginUrl;
    } catch (error) {
        verifyMessage.textContent = error.message || 'A network error occurred. Please try again.';
        verifyButton.disabled = false;
    }
});

document.getElementById('resend-code').addEventListener('click', async (event) => {
    const button = event.currentTarget;
    button.disabled = true;
    verifyMessage.textContent = '';
    try {
        const response = await fetch(verifyForm.dataset.resendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': cookie('csrftoken'),
            },
            body: JSON.stringify({ resend: true }),
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || 'Unable to resend the code.');
        }
        verifyMessage.textContent = result.message;
    } catch (error) {
        verifyMessage.textContent = error.message || 'A network error occurred. Please try again.';
    } finally {
        button.disabled = false;
    }
});

function cookie(name) {
    const value = document.cookie
        .split('; ')
        .find((row) => row.startsWith(`${name}=`));
    return value ? decodeURIComponent(value.split('=').slice(1).join('=')) : '';
}
