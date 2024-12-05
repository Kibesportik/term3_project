const userButton = document.getElementById("user_btn")
console.log(userButton.dataset.is_login)
if (userButton.dataset.is_login){
    userButton.classList.remove('d-none');
}
