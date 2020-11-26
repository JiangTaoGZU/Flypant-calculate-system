
function signconfirm() {
    if (window.confirm("确定要签收吗?")) {

        var itemid =  $("#sign_one").attr("itemid");
        $.getJSON("/fly/signone/", {'itemid': itemid}, function (data) {
            if (data['status'] === 200) {
                window.open('/fly/signdetail/?orderid=' + data['order_id'], target = "_self");
            }
        })
    } else {
// 取消时做的操作
        console.log('取消')
    }
}

// })