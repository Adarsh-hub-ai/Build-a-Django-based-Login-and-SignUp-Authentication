const loginFlow = document.getElementById('login-flow');
const loginForm = document.getElementById('login-form');
const verifyForm = document.getElementById('verify-login-form');
const errorMessage = document.getElementById('error');

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    errorMessage.textContent = '';

    try {
        const response = await fetch(loginFlow.dataset.requestUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': cookie('csrftoken'),
            },
            body: JSON.stringify({ email: document.getElementById('email').value }),
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Unable to send login code.');

        errorMessage.textContent = result.message;
        loginForm.hidden = true;
        verifyForm.hidden = false;
        document.getElementById('code').focus();
    } catch (error) {
        errorMessage.textContent = error.message || 'A network error occurred. Please try again.';
    }
});

verifyForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    errorMessage.textContent = '';

    try {
        const response = await fetch(loginFlow.dataset.verifyUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': cookie('csrftoken'),
            },
            body: JSON.stringify({ code: document.getElementById('code').value }),
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Unable to verify login code.');

        errorMessage.textContent = result.message;
        verifyForm.hidden = true;
    } catch (error) {
        errorMessage.textContent = error.message || 'A network error occurred. Please try again.';
    }
});

function cookie(name) {
    const value = document.cookie
        .split(';')
        .find((row) => row.trim().startsWith(`${name}=`));

    return value ? decodeURIComponent(value.split('=')[1]) : null;
}
