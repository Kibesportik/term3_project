document.getElementById("tourForm").addEventListener("submit", function(event) {
    event.preventDefault();
    $.ajax('/add_tour', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'city': $('#city').val(),
            'tour_date': $('#tour_date').val(),
            'tour_quant': $('#tour_quant').val(),
            'price': $('#price').val(),
            'description': $('#description').val(),
            'tour_name': $('#tour_name').val()
        },
        'success': function (response){
            document.getElementById('tour_error').innerHTML = '';
            $('#Add_Tour_Window').modal('hide');
        },
        'statusCode': {
        418: function(response) {
            document.getElementById('tour_error').innerHTML = '';
            document.getElementById('tour_error').innerHTML = response.responseJSON.error;}
        }
    });
});