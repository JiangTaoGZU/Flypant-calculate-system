/**
 * Created by JIANG on 2020/2/14.
 */
$ (function() {
    $(".orderli").click(function () {
        var $order = $(this);
        var order_id = $order.attr("orderid");
        window.open('/fly/orderdetail/?orderid='+ order_id,target="_self")
    })

})