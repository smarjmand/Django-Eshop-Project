function removeProductFromBasket(detailId){
    $.get('http://127.0.0.1:8000/order/remove-product-from-basket?detail_id=' + detailId).
    then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body)
        }
    })
}

// detailId : order detail id
// state : increase/decrease number of an item
function changeItemCount(detailId, state){
    $.get('http://127.0.0.1:8000/order/change-item-count?detail_id=' + detailId + '&state=' + state).
    then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body)
        }
    })
}