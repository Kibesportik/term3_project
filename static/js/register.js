$('#register_button').click(function (){
    let btn = document.getElementById('#register_button');
    $.ajax(btn.data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'username': $('#username').val(),
            'email': $('#email').val(),
            'password': $('#password').val(),
            'confirm_psw': $('#confirm_psw').val()
        },
        'success': function (response){
            $('#username').val('');
            $('#email').val()'';
            $('#password').val('');
            $('#confirm_psw').val('');
            document.getElementById('#user_btn').classList.remove('d-none');
        }
    });
});