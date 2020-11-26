from django.conf.urls import url
from django.urls import path

from APP import views

urlpatterns = [
    path('login/', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('index/', views.index, name='index'),
    # 布匹管理
    path('bupi/', views.bupi, name='bupi'),
    # 布老板管理
    path('buboss/', views.buboss, name='buboss'),
    path('addbuboss/', views.addbuboss, name='addbuboss'),
    path('subbuboss/', views.subbuboss, name='subbuboss'),
    # 布品类管理
    path('butype/', views.butype, name='butype'),
    path('addbutype/', views.addbutype, name='addbutype'),
    path('subbutype/', views.subbutype, name='subbutype'),
    # 布匹入库
    path('indb/', views.indb, name='indb'),
    path('addincart/', views.addincart, name='addincart'),
    path('subincart/', views.subincart, name='subincart'),
    path('addmeter/', views.addmeter, name='addmeter'),
    # 订单
    path('makeorder/', views.makeorder, name='makeorder'),
    path('orderdetail/', views.orderdetail, name='orderdetail'),
    path('orderlist/', views.orderlist, name='orderlist'),
    path('suborder/', views.suborder, name='suborder'),

    # 裁床
    path("bed/", views.bed, name='bed'),
    # path('bedwrite/', views.bedwrite,name='bedwrite'),
    path('addinbed/', views.addinbed, name='addinbed'),
    path('subinbed/', views.subinbed, name='subinbed'),
    path('countbed/', views.countbed, name='countbed'),

    # 加工发放
    path('jiagong/', views.jiagong, name='jiagong'),
    # 工人管理
    path('worker/', views.worker, name='worker'),
    path('addworker/', views.addworker, name='addworker'),
    path('subworker/', views.subworker, name='subworker'),
    # 裤子品类管理
    path('kutype/', views.kutype, name='kutype'),
    path('addkutype/', views.addkutype, name='addkutype'),
    path('subkutype/', views.subkutype, name='subkutype'),
    # 裤子发放
    path('sendcart/', views.sendcart, name='sendcart'),
    path('addinsendcart/', views.addinsendcart, name='addinsendcart'),
    path('subinsendcart/', views.subinsendcart, name='subinsendcart'),
    path('bedlist/', views.bedlist, name='bedlist'),
    # 生成发放单
    path('makesendorder/', views.makesendorder, name='makesendorder'),
    path('sendorderdetail/', views.sendorderdetail, name='sendorderdetail'),
    path('sendorderlist/', views.sendorderlist, name='sendorderlist'),
    path('subsendorder/', views.subsendorder, name='subsendorder'),
    path('sendlistbyworker/', views.sendlistbyworker, name='sendlistbyworker'),
    path('signlistbyworker/', views.signlistbyworker, name='signlistbyworker'),
    url(r'printt/(?P<orderid>\d+)$', views.printt, name='printt'),

    # 工人签收
    path('sign/', views.sign, name='sign'),
    path('signdetail/', views.signdetail, name='signdetail'),  # 签收详情页
    path('signone/', views.signone, name='signone'),  # 签收一单下一个记录
    path('signsunhao/', views.signsunhao, name='signsunhao'),  # 录入损耗和备注
    path('canselsign/', views.canselsign, name='canselsign'),  # 取消签收

    # path('market/', views.market,name='market'),
    # # 闪购分类
    # url(r'marketwithparams/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)', views.market_with_params, name='market_with_params'),
    # # # 注册
    # url(r'register/', views.register, name='register'),
    # url(r'checkuser/', views.checkuser, name='checkuser'),
    # # 登录
    # url(r'login/', views.login, name='login'),
    # #登出
    # path('logout/',views.logout,name='logout'),
    # #我的
    # path('mine/', views.mine, name='mine'),

]