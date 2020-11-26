from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.core.paginator import Paginator

from APP.models import Bupi, Boss, Cart, Order, Orderbus, Cairecord, Worker, Pants, Sendcart, Sendorder, Sendorderitems, \
    Flyuser
from django.contrib.auth.decorators import login_required #django用户认证

def index(request):
    return render(request, 'index.html')

def bupi(request):
    # busss=Bupi.objects.all().raw('  SELECT id,b_name,sum(b_meters),sum(b_storenums) FROM fly_bupi group by b_name;')
    bus = Bupi.objects.all()
    # buss=Buppi.objects.all().values('列名').annotate(新列名=Sum('列名'))
    bosslist = Boss.objects.all()

    data = {
        "title": '布匹管理',
        # "totalm":totalm,
        # "totalp":totalp,
        "bus": bus,
        # "bn":bn,
        "bosslist": bosslist,

    }
    return render(request, 'bupi.html', context=data)


def buboss(request):
    bosslist = Boss.objects.all()
    data = {
        "title": '布老板列表',
        # "bus": bus,
        "bosslist": bosslist,
    }
    return render(request, 'buboss.html', context=data)


def addbuboss(request):
    if request.method == "POST":
        try:
            if request.POST.get('bossname') != '':
                bossname = request.POST.get('bossname')
                tell = request.POST.get('tell')
                buboss_obj = Boss.objects.create(l_username=bossname, l_tell=tell)
                return redirect(reverse('fly:buboss'))
            else:
                return HttpResponse("请输入姓名！")
        except:
            return HttpResponse("请输入正确的布老板信息！")


def subbuboss(request):
    if request.method == "POST":
        bossid = request.POST.get('boss')
        buboss_obj = Boss.objects.filter(id=bossid)
        buboss_obj.delete()
        return redirect(reverse('fly:buboss'))


def butype(request):
    bus = Bupi.objects.all()
    bosslist = Boss.objects.all()
    data = {
        "title": '布品类列表',
        "bus": bus,
        "bosslist": bosslist,
    }
    return render(request, 'butype.html', context=data)


def addbutype(request):
    if request.method == "POST":
        try:
            bname = request.POST.get('bname')
            price = request.POST.get('price')
            boss = request.POST.get('boss')
            bu_obj = Bupi.objects.create(b_name=bname, b_price=price, b_bossname=boss)
            return redirect(reverse('fly:butype'))
        except:
            return HttpResponse("输入完整且单价正确才能添加！")


def subbutype(request):
    if request.method == "POST":
        buid = request.POST.get('bu')
        bu_obj = Bupi.objects.filter(id=buid)
        bu_obj.delete()
        return redirect(reverse('fly:butype'))


def indb(request):
    bus = Bupi.objects.all()
    bosslist = Boss.objects.all()
    carts = Cart.objects.all()
    data = {
        "title": "布匹入库",
        "bus": bus,
        "bosslist": bosslist,
        "carts": carts,
        'total_price': get_total_price(),
        'total_meters': get_total_meters(),
        'total_nums': get_total_nums(),

    }
    return render(request, 'indb.html', context=data)


def addincart(request):
    if request.method == "POST":
        try:
            buid = request.POST.get('butype')
            bunum = request.POST.get('bunum')
            for num in range(int(bunum)):
                Cart.objects.create(c_bupi_id=buid)
            # carts = Cart.objects.all()
            return redirect(reverse('fly:indb'))

        except:
            return HttpResponse("请输入要入库的布匹数目")


# 删除入库列表
def subincart(request):
    if request.method == "POST":
        cartbuid = request.POST.get('cartbu')
        bu_obj = Cart.objects.filter(id=cartbuid)
        bu_obj.delete()
    else:
        Cart.objects.all().delete()
    return redirect(reverse('fly:indb'))


def addmeter(request):
    if request.method == "POST":
        meters = request.POST.getlist('meter')
        for i, item in enumerate(meters):
            if item == '':
                meters[i] = '0'
        cart_objs = Cart.objects.filter(c_meter=0)
        lens = len(cart_objs)
        if (lens == len(meters)):
            for le in range(lens):
                cart_objs[le].c_meter = meters[le]
                cart_objs[le].save()
            return redirect(reverse('fly:indb'))

        else:
            return redirect(reverse('fly:indb'))



def get_total_price():
    carts = Cart.objects.all()
    total = 0
    for cart in carts:
        total += cart.c_meter * cart.c_bupi.b_price
    return "{:.3f}".format(total)


def get_total_meters():
    carts = Cart.objects.all()
    total = 0
    for cart in carts:
        total += cart.c_meter
    return "{:.2f}".format(total)


def get_total_nums():
    carts = Cart.objects.all()
    total = len(carts)
    return total


def makeorder(request):
    carts = Cart.objects.all()
    # 防止重复点击
    if carts.exists():
        order = Order()
        order.o_allprice = get_total_price()
        order.o_meters = get_total_meters()
        order.o_pishu = get_total_nums()
        order.save()
        for cart_obj in carts:
            # 将布匹的匹数和米数入库
            bupi = Bupi.objects.get(pk=cart_obj.c_bupi_id)
            bupi.b_storenums = bupi.b_storenums + 1
            bupi.b_meters = bupi.b_meters + cart_obj.c_meter
            bupi.save()
            # 录入每个订单的每项入库记录
            orderbus = Orderbus()
            orderbus.o_order = order
            orderbus.o_meter = cart_obj.c_meter
            orderbus.o_bupi = cart_obj.c_bupi.b_bossname + '|' + cart_obj.c_bupi.b_name  # 拼接布品名，取消外键的联系，防止当删除布品后订单详情页被删除
            orderbus.o_price = cart_obj.c_bupi.b_price
            orderbus.save()
            cart_obj.delete()  # 完成入库后马上删除刚刚的购物车赞！

        data = {
            'status': 200,
            'msg': 'make order ok',
            'order_id': order.id
        }
        return JsonResponse(data=data)
        # return render(request, 'order_detail.html', context=data)


def orderdetail(request):
    order_id = request.GET.get('orderid')
    order = Order.objects.get(pk=order_id)
    bupi = Bupi.objects.filter()
    data = {
        'title': "入库单详情",
        'order': order,
    }
    return render(request, 'order_detail.html', context=data)


def orderlist(request):
    orders = Order.objects.all().order_by('-o_time')
    #分页
    paginator = Paginator(orders, 7)
    pages = paginator.page_range  # 生成所有页码
    pages_num = paginator.num_pages  # 总页数
    page = request.GET.get('page')  # 当前页面
    contacts = paginator.get_page(page)  # 当前页并具有处理超出页码范围的状况,页码不是数字返回第一页，超出返回最后一页

    data = {
        'title': '入库单列表',
        'orders': orders,

        'contacts': contacts,
        'pages': pages,
        'pagenums': pages_num,


    }
    return render(request, 'orderlist.html', context=data)


def suborder(request):
    if request.method == "POST":
        try:
            orderid = request.POST.get('orderl')
            order_obj = Order.objects.filter(id=orderid)
            if order_obj.exists():
                orderbus = Orderbus.objects.filter(o_order=orderid)
                # 将订单关联布匹的匹数和米数减少
                for orderbu in orderbus:
                    bupinames = orderbu.o_bupi.split('|')
                    bupi_obj = Bupi.objects.filter(b_bossname=bupinames[0], b_name=bupinames[1]).first()
                    bupi_obj.b_storenums = bupi_obj.b_storenums - 1
                    # print('dd',bupi_obj.b_storenums)
                    bupi_obj.b_meters = bupi_obj.b_meters - orderbu.o_meter
                    # print('cc', bupi_obj.b_meters)
                    bupi_obj.save()

                order_obj.delete()
                return redirect(reverse('fly:orderlist'))
            else:
                return HttpResponse("请输入正确的编号！")
        except:
            return HttpResponse("请输入正确的编号！")


# 裁床管理
def bed(request):
    bus = Bupi.objects.all()
    #分页
    cairecords = Cairecord.objects.all().order_by('-cai_date')
    paginator = Paginator(cairecords, 7)
    pages = paginator.page_range  # 生成所有页码
    pages_num = paginator.num_pages  # 总页数
    page = request.GET.get('page')  # 当前页面
    contacts = paginator.get_page(page)  # 当前页并具有处理超出页码范围的状况,页码不是数字返回第一页，超出返回最后一页

    total_nums = len(cairecords)
    # 这里用到了arregate
    cais = Cairecord.objects.all().aggregate(c_pants=Sum('cai_nums'))
    # 计算总价
    total_price = 0
    for cai in cairecords:
        total_price += cai.cai_nums * cai.cai_price

    data = {
        "title": '裁床管理',
        "bus": bus,
        "cairecords": cairecords,
        "total_pants": cais['c_pants'],
        "total_nums": total_nums,
        "total_price": "{:.2f}".format(total_price),

        'contacts': contacts,
        'pages': pages,
        'pagenums': pages_num,


    }
    return render(request, 'bed.html', context=data)


def addinbed(request):
    if request.method == "POST":
        try:
            bupinid = request.POST.get('bupin')
            caiprice = request.POST.get('caiprice')
            if request.POST.get('29')=='':
                erjiu = 0
            else:
                erjiu=request.POST.get('29')
            if request.POST.get('30')=='':
                sanlin = 0
            else:
                sanlin = request.POST.get('30')
            if request.POST.get('31')=='':
                sanyi = 0
            else:
                sanyi = request.POST.get('31')
            if request.POST.get('32')=='':
                saner = 0
            else:
                saner = request.POST.get('32')
            cai_meter = request.POST.get('mi')
            # 计算总条数
            cai_nums = int(erjiu) + int(sanlin) + int(sanyi) + int(saner)
            # 拼接得到裁剪记录的布品品名
            bupin_obj = Bupi.objects.get(pk=bupinid)
            bupin_boss = bupin_obj.b_bossname
            bupin_name = bupin_obj.b_name
            bupin = bupin_boss + '|' + bupin_name
            Cairecord.objects.create(cai_bupin=bupin, twonine=erjiu, treezero=sanlin,
                                     treeone=sanyi, treetwo=saner, cai_price=caiprice, cai_nums=cai_nums,
                                     cai_meter=cai_meter)
            # 每生成一条裁剪记录，库存中的相应字段也要减少
            bupin_obj.b_storenums = bupin_obj.b_storenums - 1
            bupin_obj.b_meters = bupin_obj.b_meters - float(cai_meter)
            bupin_obj.save()

            return redirect(reverse('fly:bed'))

        except:
            return HttpResponse("输入完整合正确才能入库！")


def subinbed(request):
    if request.method == "POST":
        try:
            caiid = request.POST.get('caidele')
            cai_obj = Cairecord.objects.get(pk=caiid)
            # 将库存相应字段增加
            bupinames = cai_obj.cai_bupin.split('|')
            bupi_obj = Bupi.objects.filter(b_bossname=bupinames[0], b_name=bupinames[1]).first()
            if bupi_obj:
                bupi_obj.b_storenums = bupi_obj.b_storenums + 1
                bupi_obj.b_meters = bupi_obj.b_meters + cai_obj.cai_meter
                bupi_obj.save()

            cai_obj.delete()
            return redirect(reverse('fly:bed'))
        except:
            return HttpResponse("输入正确的编号才能删除！")


def jiagong(request):
    pants = Pants.objects.all()

    data = {
        "title": '工人加工',
        # "totalm":totalm,
        # "totalp":totalp,
        "pants": pants,

    }
    return render(request, 'jiagong.html', context=data)


def worker(request):
    workerlist = Worker.objects.all()
    data = {
        "title": '工人列表',
        # "bus": bus,
        "workerlist": workerlist,
    }
    return render(request, 'worker.html', context=data)


def addworker(request):
    if request.method == "POST":
        try:
            if request.POST.get('workername') != '':
                workername = request.POST.get('workername')
                tell = request.POST.get('tell')
                worker_obj = Worker.objects.create(w_name=workername, w_tell=tell)
                return redirect(reverse('fly:worker'))
            else:
                return HttpResponse("请输入工人姓名！")
        except:
            return HttpResponse("请输入正确的工人信息！")


def subworker(request):
    if request.method == "POST":
        workerid = request.POST.get('worker')
        worker_obj = Worker.objects.filter(id=workerid)
        worker_obj.delete()
        return redirect(reverse('fly:worker'))


def kutype(request):
    pants = Pants.objects.all()
    data = {
        "title": '裤品类列表',
        "pants": pants,
    }
    return render(request, 'kutype.html', context=data)


def addkutype(request):
    if request.method == "POST":
        try:
            pname = request.POST.get('pname')
            p_obj = Pants.objects.create(p_name=pname)
            return redirect(reverse('fly:kutype'))
        except:
            return HttpResponse("输入完整且单价正确才能添加！")


def subkutype(request):
    if request.method == "POST":
        pid = request.POST.get('pants')
        p_obj = Pants.objects.filter(id=pid)
        p_obj.delete()
        return redirect(reverse('fly:kutype'))


def sendcart(request):
    pants = Pants.objects.all()
    workerlist = Worker.objects.all()
    cailist = Cairecord.objects.all()
    sendcarts = Sendcart.objects.all()

    data = {
        "title": "裤子发放",
        "pants": pants,
        "sendcarts": sendcarts,
        "workerlist": workerlist,
        "cailist": cailist,
        'all_price': get_all_price(),  # 发放的总价
        'all_nums': get_all_nums(),  # 发放的总条数
        'all_pishu': get_all_pishu(),  # 发放的匹数

    }
    return render(request, 'sendcart.html', context=data)


def addinsendcart(request):
    if request.method == "POST":
        try:
            workerid = request.POST.get('worker')
            pantsid = request.POST.get('pants')
            caiid = request.POST.get('caiid')
            price = request.POST.get('price')
            pishu = request.POST.get('pishu')
            if Sendcart.objects.filter(s_cai_id=caiid) or Sendorderitems.objects.filter(soi_caiid=caiid):
                return HttpResponse("一匹裁好的布只能发放一次！")
            else:
                # s_nums=
                Sendcart.objects.create(s_wname_id=workerid, s_kuname_id=pantsid, s_cai_id=caiid, s_price=price)
                return redirect(reverse('fly:sendcart'))
        except:
            return HttpResponse("请输入正确的布匹编号和加工价格！")


def bedlist(request):
    cairecords = Cairecord.objects.all().order_by('-cai_date')
    # 分页
    paginator = Paginator(cairecords, 7)
    pages = paginator.page_range  # 生成所有页码
    pages_num = paginator.num_pages  # 总页数
    page = request.GET.get('page')  # 当前页面
    contacts = paginator.get_page(page)  # 当前页并具有处理超出页码范围的状况,页码不是数字返回第一页，超出返回最后一页

    data = {
        "title": '裁床列表',
        "cairecords": cairecords,

        'contacts': contacts,
        'pages': pages,
        'pagenums': pages_num,


    }
    return render(request, 'bedlist.html', context=data)


def subinsendcart(request):
    if request.method == "POST":
        cartid = request.POST.get('deleone')
        s_obj = Sendcart.objects.filter(id=cartid)
        s_obj.delete()
    else:
        Sendcart.objects.all().delete()
    return redirect(reverse('fly:sendcart'))


def get_all_price():
    carts = Sendcart.objects.all()
    total = 0
    for cart in carts:
        total += cart.s_price * cart.s_cai.cai_nums
    return "{:.3f}".format(total)


def get_all_nums():
    carts = Sendcart.objects.all()
    total = 0
    for cart in carts:
        total += cart.s_cai.cai_nums
    return total


def get_all_pishu():
    carts = Sendcart.objects.all()
    total = len(carts)
    return total


def makesendorder(request):
    sendcarts = Sendcart.objects.all()
    cais = Cairecord.objects.all()
    # 防止重复点击
    if sendcarts.exists():
        # 创建一个发送订单
        order = Sendorder()
        order.s_o_worker = sendcarts[0].s_wname.w_name
        order.s_o_allprice = get_all_price()
        order.s_o_nums = get_all_nums()
        order.s_o_pishu = get_all_pishu()
        order.save()
        for cart_obj in sendcarts:
            # 将订单的总条数记录在Pants中
            pant = Pants.objects.get(pk=cart_obj.s_kuname_id)
            pant.p_nums = pant.p_nums + cart_obj.s_cai.cai_nums
            pant.save()
            # 录入每个订单的每项入库记录
            items = Sendorderitems()
            items.soi_order = order
            items.soi_pname = cart_obj.s_kuname.p_name  # 裤品名
            items.soi_price = cart_obj.s_price  # 加工单价
            items.soi_nums = cart_obj.s_cai.cai_nums  # 一次发放记录的总条数
            items.soi_caiid = cart_obj.s_cai.id  # 来源

            #将发放出去的布的状态改变
            cai=cais.get(pk=items.soi_caiid)
            cai.cai_sign=True
            cai.save()

            items.soi_caibupin = cart_obj.s_cai.cai_bupin
            items.save()
            cart_obj.delete()  # 完成入库后马上删除刚刚的购物车赞！

        data = {
            'status': 200,
            'msg': 'make order ok',
            'order_id': order.id
        }
        return JsonResponse(data=data)


def sendorderdetail(request):
    order_id = request.GET.get('orderid')
    order = Sendorder.objects.get(pk=order_id)
    data = {
        'title': "发放单详情",
        'order': order,
    }
    return render(request, 'send_order_detail.html', context=data)


def sendorderlist(request):
    workerlist = Worker.objects.all()
    orders = Sendorder.objects.all().order_by('-s_o_time')
    # 分页
    paginator = Paginator(orders, 7)
    pages = paginator.page_range  # 生成所有页码
    pages_num = paginator.num_pages  # 总页数
    page = request.GET.get('page')  # 当前页面
    contacts = paginator.get_page(page)  # 当前页并具有处理超出页码范围的状况,页码不是数字返回第一页，超出返回最后一页

    data = {
        'title': '发放单列表',
        'orders': orders,
        "workerlist": workerlist,


        'contacts': contacts,
        'pages': pages,
        'pagenums': pages_num,


    }
    return render(request, 'sendorderlist.html', context=data)


def subsendorder(request):
    if request.method == "POST":
        try:
            orderid = request.POST.get('orderl')
            order_obj = Sendorder.objects.filter(id=orderid)
            if order_obj.exists():
                items = Sendorderitems.objects.filter(soi_order_id=orderid)
                # 将订单关联裤子的发放数减少
                for item in items:
                    pant_obj = Pants.objects.filter(p_name=item.soi_pname).first()
                    pant_obj.p_nums = pant_obj.p_nums - item.soi_nums
                    pant_obj.save()
                    try:
                        #将发放状态改变
                        cai=Cairecord.objects.filter(id=item.soi_caiid).first()
                        cai.cai_sign=False
                        cai.save()
                    except:
                        pass
                order_obj.delete()
                return redirect(reverse('fly:sendorderlist'))
            else:
                return HttpResponse("请输入正确的编号！")
        except:
            return HttpResponse("请输入正确的编号！")


def sign(request):
    workerlist = Worker.objects.all()
    orders = Sendorder.objects.all().order_by('-s_o_time')
    # 分页
    paginator = Paginator(orders, 7)
    pages = paginator.page_range  # 生成所有页码
    pages_num = paginator.num_pages  # 总页数
    page = request.GET.get('page')  # 当前页面
    contacts = paginator.get_page(page)  # 当前页并具有处理超出页码范围的状况,页码不是数字返回第一页，超出返回最后一页

    data = {
        "title": '加工签收',
        "orders": orders,
        "workerlist": workerlist,
        # "totalm":totalm,
        # "totalp":totalp,

        'contacts': contacts,
        'pages': pages,
        'pagenums': pages_num,

    }
    return render(request, 'sign.html', context=data)


def signdetail(request):
    order_id = request.GET.get('orderid')
    order = Sendorder.objects.get(pk=order_id)
    data = {
        'title': "签收页详情",
        'order': order,
    }
    return render(request, 'sign_detail.html', context=data)


def signone(request):
    itemid = request.GET.get('itemid')
    item = Sendorderitems.objects.get(pk=itemid)
    item.soi_is_sign = True
    item.save()
    order = item.soi_order
    # 判断是否每个发放单都签收，如果是则修改订单的签收状态
    os = Sendorderitems.objects.filter(soi_order_id=order.id)
    cc = os.aggregate(aa=Sum('soi_is_sign'))
    if cc['aa'] == len(os):
        order.s_o_is_sign = True
        order.save()

    data = {
        'status': 200,
        'msg': 'make order ok',
        'order_id': order.id
    }
    return JsonResponse(data=data)


def signsunhao(request):
    if request.method == "POST":
        try:
            orderid = request.POST.get('orderid')
            sunhao = request.POST.get('sunhao')
            beizhu = request.POST.get('beizhu')
            order = Sendorder.objects.get(pk=orderid)
            if not sunhao:
                return HttpResponse("请输入损耗金额！")

            if order.s_o_sunhao == 0:
                order.s_o_sunhao = sunhao
                order.s_o_beizhu = beizhu
                order.s_o_allprice = order.s_o_allprice - float(sunhao)
                order.save()
                data = {
                    'title': "签收页详情",
                    'order': order,
                }
                return render(request, 'sign_detail.html', context=data)
            else:
                return HttpResponse("每一单只能填写一次损耗，请勿重复填写！若想重新填写备注，可以在签收列表先取消本单的签收，再重新输入损耗")

        except:
            return HttpResponse("请填写正确的损耗金额！")


def canselsign(request):
    if request.method == "POST":
        try:
            orderid = request.POST.get('orderli')
            order_obj = Sendorder.objects.get(pk=orderid)
            if order_obj:
                items = Sendorderitems.objects.filter(soi_order_id=orderid)
                # 将订单关联的所有记录签收状态改变
                for item in items:
                    item.soi_is_sign = False
                    item.save()
                #改变订单签收状态并加上损耗的价格
                order_obj.s_o_is_sign = False
                p = order_obj.s_o_sunhao
                order_obj.s_o_sunhao = 0
                order_obj.s_o_beizhu=''
                order_obj.s_o_allprice = order_obj.s_o_allprice + p
                order_obj.save()
                return redirect(reverse('fly:sign'))
            else:
                return HttpResponse("请输入正确的编号哦！")
        except:
            return HttpResponse("请输入正确的编号！")


def sendlistbyworker(request):
    workerlist = Worker.objects.all()
    worker= request.POST.get('worker')
    orders = Sendorder.objects.filter(s_o_worker=worker).order_by('-s_o_time')

    # 分页
    paginator = Paginator(orders, 7)
    pages = paginator.page_range  # 生成所有页码
    pages_num = paginator.num_pages  # 总页数
    page = request.GET.get('page')  # 当前页面
    contacts = paginator.get_page(page)  # 当前页并具有处理超出页码范围的状况,页码不是数字返回第一页，超出返回最后一页

    data = {
        'title': '发放单列表',
        'orders': orders,
        "workerlist": workerlist,

        'contacts': contacts,
        'pages': pages,
        'pagenums': pages_num,


    }
    return render(request, 'sendorderlist.html', context=data)


def signlistbyworker(request):
    workerlist = Worker.objects.all()
    worker = request.POST.get('worker')
    orders = Sendorder.objects.all().filter(s_o_worker=worker).order_by('-s_o_time')

    # 分页
    paginator = Paginator(orders, 7)
    pages = paginator.page_range  # 生成所有页码
    pages_num = paginator.num_pages  # 总页数
    page = request.GET.get('page')  # 当前页面
    contacts = paginator.get_page(page)  # 当前页并具有处理超出页码范围的状况,页码不是数字返回第一页，超出返回最后一页

    #计算已签收的单子的总价
    total_price = orders.filter(s_o_is_sign=True).aggregate(price=Sum('s_o_allprice'))
    total_nums = orders.filter(s_o_is_sign=True).aggregate(nums=Sum('s_o_nums'))
    total_pishu = orders.filter(s_o_is_sign=True).aggregate(pishu=Sum('s_o_pishu'))

    data = {
        "title": '加工签收',
        "orders": orders,
        "workerlist": workerlist,
        "worker":worker,
        "total_price":total_price['price'],
        "total_nums":total_nums['nums'],
        "total_pishu":total_pishu['pishu'],

        'contacts': contacts,
        'pages': pages,
        'pagenums': pages_num,

    }
    return render(request, 'signlistbyworker.html', context=data)


def countbed(request):
    #计算裁床总价
    cairecords = Cairecord.objects.all().order_by('-cai_date')
    total_nums = len(cairecords)
    # 这里用到了arregate
    cais = Cairecord.objects.all().aggregate(c_pants=Sum('cai_nums'))
    # 计算总价
    total_price = 0
    for cai in cairecords:
        total_price += cai.cai_nums * cai.cai_price

    data = {
        "title": '裁床总价',
        "cairecords": cairecords,
        "total_pants": cais['c_pants'],
        "total_nums": total_nums,
        "total_price": "{:.2f}".format(total_price),

    }
    return render(request, 'countbed.html', context=data)


def login(request):
    if request.method == 'GET':
        error_message = request.session.get('error_message')
        data = {
            "title": "登录",
        }
        # 判断是否有错误信息
        if error_message:
            del request.session['error_message']  # 用完马上session删掉存入的error message
            data['error_message'] = error_message
        return render(request, 'login.html', context=data)
    elif request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        if Flyuser.objects.filter(u_username=name).exists():
            user = Flyuser.objects.get(u_username=name)
            if user.u_password==password:
                # 这里很重要， 当密码检查通过后将user_id写入session
                request.session['user_id'] = user.id
                return redirect(reverse('fly:index'))
            else:
                # 当页面重定向时可以将 要传入前端渲染的data放入session，进入get方法渲染
                request.session['error_message'] = '密码错误'
                return redirect(reverse('fly:login'))
        request.session['error_message'] = '用户不存在'
        return redirect(reverse('login'))

def logout(request):
    # 清空缓存
    request.session.flush()
    return redirect(reverse('fly:login'))

def printt(request,orderid):
    # order_id = request.GET.get('orderid')
    # print(order_id)
    order = Sendorder.objects.get(pk=orderid)
    data = {
        'title': "发放单打印",
        'order': order,
    }
    return render(request, 'print.html', context=data)