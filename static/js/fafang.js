/**
 * Created by JIANG on 2020/2/17.
 */
$(function () {
    $("#make_order").click(function () {
        $.getJSON("/fly/makesendorder/", function (data) {
            console.log(data);
            if (data['status'] === 200) {
                window.open('/fly/sendorderdetail/?orderid=' + data['order_id'], target = "_self");
            }
        })
    })


})