$('.order_button').click(function (){
    let order_btn = $(this)
    const price_div = $('#order_div'+String(order_btn.data('id')));
    const order_input = $('#order_input'+String(order_btn.data('id')));
    let price = order_btn.data('price');
    order_input.on("input", (event) => {
        let order_input_amount = order_input.val();
        let final_tour_price = order_input_amount * price;
        price_div.html(`<p> Price for all:  ${final_tour_price}</p>`);
    });
    $('.confirm_order_button').click(function (){
        let btn = $(this);
        $.ajax(btn.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'order_amount': $('#order_input'+String(btn.data('id'))).val()
            },
            'success': function (response){
                price_div.html(`<p> Price for all: 0 </p>`);
                $('#order_input'+String(btn.data('id'))).val('');
                $(btn.data('modal-id')).modal('hide');
            },
        })
    });
});