/**
 * Created by JIANG on 2020/2/13.
 */
$(function () {
    $("#make_order").click(function () {
        $.getJSON("/fly/makeorder/", function (data) {
            console.log(data);
            if (data['status'] === 200) {
                window.open('/fly/orderdetail/?orderid=' + data['order_id'], target = "_self");
            }
        })
    })


})