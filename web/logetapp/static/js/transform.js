

// DOMを全て読み込んでから処理する
$(function(){
    $('.ttl_h1').on('click', function(){
        $(this).toggleClass('active');
 
        if($(this).hasClass('active')){
            $(this).attr('data-name', '−');
        } else {
            $(this).attr('data-name', '+');
        }
    });
});
