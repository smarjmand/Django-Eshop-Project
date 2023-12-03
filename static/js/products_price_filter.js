// to filter price range

function filterProducts(){
    const filterPrice = $('#sl2').val();
    const startPrice = filterPrice.split(',')[0];
    const endPrice = filterPrice.split(',')[1];
    $('#start_price_input').val(startPrice);
    $('#end_price_input').val(endPrice);
    $('#price_filter_form').submit();
}

function fillPage(page){
    $('#page_number_input').val(page);
    $('#price_filter_form').submit();
}