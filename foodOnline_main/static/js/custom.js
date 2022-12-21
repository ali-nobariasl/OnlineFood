

$(document).ready(function() {
    // add to cart
    $('.add_to_cart').on('click', function(e) {
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type : 'GET',
            url : url,
            success : function(response) {
                console.log(response)
                if (response.status =='login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login/';
                    })
                
                }else if (response.status =='Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                }
            }
        })
    })

    // place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
        console.log(qty)
    })

    //decrease cart
    $('.decrease_cart').on('click', function(e) {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type : 'GET',
            url : url,
            success : function(response) {
                console.log(response)
                if (response.status =='login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login/';
                    })
                
                }else if (response.status =='Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                }
            }
        })
    })
        //decrease cart
    $('.decrease_cart').on('click', function(e) {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type : 'GET',
            url : url,
            success : function(response) {
                console.log(response)
                if (response.status =='login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login/';
                    })
                
                }else if (response.status =='Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                }
            }
        })
    })

    //delete cart
    $('.delete_cart').on('click', function(e) {
        e.preventDefault();

        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type : 'GET',
            url : url,
            success : function(response) {
                console.log(response)
                if (response.status =='Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status,'response.message','success')
                    removeCartItem(0,cart_id);
                    checkEmptyCart();
                }
            }
        })
    })

    //delete the cart element if the qty is 0
    function removeCartItem(cartItemQuantity, cart_id){
        if (cartItemQuantity <= 0){
            // remove the cart item elemnt 
            document.getElementById("cart-item-"+ cart_id).remove()
        }
    }

    //check if the cart is empty
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter==0){
            document.getElementById("empty-cart").style.display = "block";
        }
    }
});