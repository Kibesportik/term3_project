$('.order_button').click(function (){
    const order_btn = $(this)
    const price_div = $('#order_div'+String(order_btn.data('id')));
    const amount_div = $('#amount_div'+String(order_btn.data('id')));
    const order_input = $('#order_input'+String(order_btn.data('id')));
    let price = order_btn.data('price');
    let tour_city = order_btn.data('city');
    let tour_date = order_btn.data('tour_date');
    order_input.on("input", (event) => {
        let order_input_amount = order_input.val();
        let final_tour_price = order_input_amount * price;
        price_div.html(`<p> Price for all:  ${final_tour_price}</p>`);
    });
    $('.confirm_order_button').click(function (){
        const confirm_btn = $(this);
        $.ajax(confirm_btn.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'order_amount': order_input.val()
            },
            'success': function (response){
                let new_info = `
                <span class="badge bg-warning text-dark">Tour to: ${ tour_city }</span>
                <span class="badge bg-warning text-dark">Tour date: ${ tour_date }</span>
                <span class="badge bg-warning text-dark">Spaces left: ${ response.current_amount }</span>`
                price_div.html(`<p> Price for all: 0 </p>`);
                amount_div.html(`<p> Spaces left: ${ response.current_amount } </p>`);
                $('#order_input'+String(order_btn.data('id'))).val('');
                $('#tour_info'+String(order_btn.data('id'))).html(new_info)
                $(confirm_btn.data('modal-id')).modal('hide');
            },
            'statusCode': {
                418: function(response) {
                document.getElementById('tour_order_error').innerHTML = '';
                document.getElementById('tour_order_error').innerHTML = response.responseJSON.error;}
            }
        });
    });
});