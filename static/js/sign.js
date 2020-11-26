/**
 * Created by JIANG on 2020/2/17.
 */
$ (function() {
    $(".orderli").click(function () {
        var $order = $(this);
        var order_id = $order.attr("orderid");
        window.open('/fly/signdetail/?orderid='+ order_id,target="_self")
    })

})