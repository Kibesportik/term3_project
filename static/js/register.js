document.getElementById("registerForm").addEventListener("submit", function(event) {
    event.preventDefault();
    $.ajax('/register', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'username': $('#register_username').val(),
            'email': $('#register_email').val(),
            'password': $('#register_psw').val(),
            'confirm_psw': $('#register_confirm_psw').val()
        },
        'success': function (response){
            $('#register_username').val('');
            $('#register_email').val('');
            $('#register_psw').val('');
            $('#register_confirm_psw').val('');
            document.getElementById('register_error').innerHTML = '';
            const user_btn = document.getElementById('user_btn');
            user_btn.classList.remove('d-none');
            user_btn.textContent= response.current_user;
            $('#Register_Window').modal('hide');
        },
        'statusCode': {
        418: function(response) {
            document.getElementById('register_error').innerHTML = '';
            document.getElementById('register_error').innerHTML = response.responseJSON.error;}
        }
    });
});