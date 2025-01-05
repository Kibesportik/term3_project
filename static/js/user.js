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
            user_btn.href = '/profile/'+String(response.user_id);
            $('#Login_Window').modal('hide');
        },
        'statusCode': {
        418: function(response) {
            document.getElementById('login_error').innerHTML = '';
            document.getElementById('login_error').innerHTML = response.responseJSON.error;}
        }
    });
});

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
            user_btn.href = '/profile/'+String(response.user_id);
            $('#Register_Window').modal('hide');
        },
        'statusCode': {
        418: function(response) {
            document.getElementById('register_error').innerHTML = '';
            document.getElementById('register_error').innerHTML = response.responseJSON.error;}
        }
    });
});

document.getElementById("changePasswordForm").addEventListener("submit", function(event) {
    event.preventDefault();
    $.ajax('/change_password', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'current_psw': $('#current_psw').val(),
            'new_psw': $('#new_psw').val(),
        },
        'success': function (response){
            $('#current_psw').val('');
            $('#new_psw').val('');
            document.getElementById('change_password_error').innerHTML = '';
            $('#Change_Password_Window').modal('hide');
        },
        'statusCode': {
        418: function(response) {
            document.getElementById('change_password_error').innerHTML = '';
            document.getElementById('change_password_error').innerHTML = response.responseJSON.error;
            }
        }
    });
});

document.getElementById("changeUsernameForm").addEventListener("submit", function(event) {
    event.preventDefault();
    $.ajax('/change_username', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'new_username': $('#new_username').val(),
        },
        'success': function (response){
            $('#new_username').val('');
            document.getElementById('change_username_error').innerHTML = '';
            $('#Change_Username_Window').modal('hide');
        },
        'statusCode': {
        418: function(response) {
            document.getElementById('change_username_error').innerHTML = '';
            document.getElementById('change_username_error').innerHTML = response.responseJSON.error;
            }
        }
    });
});

document.getElementById("deleteUserForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const delete_user = $('#delete_user').val();
    $.ajax('/delete_user', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'delete_username': delete_user,
        },
        'success': function (response){
            $('#delete_user').val('');
            document.getElementById('delete_user_error').innerHTML = '';
            $('#Delete_User_Window').modal('hide');
        },
        'statusCode': {
        418: function(response) {
            document.getElementById('delete_user_error').innerHTML = '';
            document.getElementById('delete_user_error').innerHTML = response.responseJSON.error;
            }
        }
    });
});

document.getElementById("addAdminForm").addEventListener("submit", function(event) {
    event.preventDefault();
    $.ajax('/add_admin', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'username': $('#admin_name').val(),
            'email': $('#admin_email').val(),
            'password': $('#admin_psw').val(),
            'confirm_psw': $('#admin_confirm_psw').val()
        },
        'success': function (response){
            $('#admin_name').val('');
            $('#admin_email').val('');
            $('#admin_psw').val('');
            $('#admin_confirm_psw').val('');
            document.getElementById('add_admin_error').innerHTML = '';
            $('#Add_Admin_Window').modal('hide');
        },
        'statusCode': {
        418: function(response) {
            document.getElementById('add_admin_error').innerHTML = '';
            document.getElementById('add_admin_error').innerHTML = response.responseJSON.error;}
        }
    });
});

