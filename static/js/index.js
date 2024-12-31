const userButton = document.getElementById("user_btn")
const search_input = $('#search')
if (userButton.dataset.is_login == 'True'){
    userButton.classList.remove('d-none');
    userButton.href = '/profile/'+String(userButton.dataset.user_id);
};

search_input.on("input", (event) => {
    $.ajax('/search', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'search_word': search_input.val()
        },
        'success': function (response){
            const tour_id_list = response.tour_id_list;
            for (let tour in tour_id_list){
                let tour_example = document.getElementById(tour_id_list[tour]);
                tour_example.classList.add('d-none');
            }
        },
        'statusCode': {
        418: function(response) {
            const tour_id_list = response.responseJSON.tour_id_list;
            for (let tour in tour_id_list){
                let tour_example = document.getElementById(tour_id_list[tour]);
                tour_example.classList.remove('d-none');
            }
            }
        }
    });
});

