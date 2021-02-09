<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
<script>
$(function(){
    var $setElem = $('.switch'),
    pcName = '_pc',
    spName = '_sp',
    replaceWidth = 641;
 
    $setElem.each(function(){
        var $this = $(this);
        function imgSize(){
            if(window.innerWidth > replaceWidth) {
                $this.attr('src',$this.attr('src').replace(spName,pcName)).css({visibility:'visible'});
            } else {
                $this.attr('src',$this.attr('src').replace(pcName,spName)).css({visibility:'visible'});
            }
        }
        $(window).resize(function(){imgSize();});
        imgSize();
    });
});
</script>