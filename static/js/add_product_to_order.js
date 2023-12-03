function addProductToOrder(productId) {
    const productCount = $('#product-count').val()
    $.get('http://127.0.0.1:8000/order/add-product-to-basket?product_id=' + productId + '&count=' + productCount).
    then( res => {
        Swal.fire({
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "#3085d6",
            confirmButtonText: res.confirm_button_text
        });
    })
}


