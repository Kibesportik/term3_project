document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    $.ajax('/login', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'email': $('#login_email').val(),
            'password': $('#login_psw').val(),
        },
        'success': function (response){
            $('#login_email').val('');
            $('#login_psw').val('');
            document.getElementById('login_error').innerHTML = '';
            const user_btn = document.getElementById('user_btn');
            user_btn.classList.remove('d-none');
            user_btn.textContent = response.current_user;
            $('#Login_Window').modal('hide');
        },
        'statusCode': {
        418: function(response) {
            console.log(response)
            document.getElementById('login_error').innerHTML = '';
            document.getElementById('login_error').innerHTML = response.responseJSON.error;}
        }
    });
});