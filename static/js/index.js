const userButton = document.getElementById("user_btn")
if (userButton.dataset.is_login == 'True'){
    userButton.classList.remove('d-none');
    userButton.href = '/profile/'+String(userButton.dataset.user_id);
};

