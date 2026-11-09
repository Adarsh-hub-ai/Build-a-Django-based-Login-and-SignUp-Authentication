console.log('the file is running')

const btn = document.getElementById('btn');
const input_name = document.getElementById('name');
const input_email = document.getElementById('email');

btn.addEventListener('click', function() {
    getemail()
    window.location.href = '/myapp/sendcode/'
})


function getemail() {
    let name = input_name.value;
    let email = input_email.value;

    

    fetch('/myapp/signin/', {
        'method' : 'POST',
        'headers' : {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : cookie('csrftoken')
        },
        body : JSON.stringify({
            name : name,
            email : email
        }) 
})

};


function cookie(name) {
    let cookie = document.cookie
    .split('; ')
    .find(row => row.startsWith(name + '='))


    return cookie ? decodeURIComponent(cookie.split('=')[1]) : null;
};
