const admin_settings_dtn = document.getElementById("home_btn")
const admin_settings = document.getElementById("admin_settings")
if (admin_settings_dtn.dataset.is_admin == 'True'){
    admin_settings.classList.remove('d-none');
};