const btn = document.getElementById('btn')
const input_email = document.getElementById('email')



btn.addEventListener('click', function() {
    login()
})


function login(){
    let email = input_email.value

    fetch('/myapp/login/', {
        'method' : 'POST',
        'headers' : {
            'Content-Type' : 'application/json',
            'X-CsrfToken' : cookie('csrftoken')
        },

        body : JSON.stringify({
            email : email
        })
    })

    .then(response => {
        return response.json()

    })

    .then(data => {
        if (data.error){
            document.getElementById('error').textContent = data.error
        }
    })
}


function cookie(name){
    let cookie = document.cookie
    .split(';')
    .find(row => row.startsWith(name + '='))


    return cookie ? decodeURIComponent(cookie.split('=')[1]) : null
}