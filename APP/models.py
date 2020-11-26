from django.db import models


class Bupi(models.Model):
    b_bossname = models.CharField(max_length=32)  #  关联布老板的名字
    b_name = models.CharField(max_length=100)  # 布匹的名称
    b_price = models.FloatField(default=0)  # 布匹的一米的进价
    b_storenums = models.IntegerField(default=0)  # 布匹的库存数(多少匹)
    b_meters = models.FloatField(default=0) #该种布的总米数
    # btime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'fly_bupi'


class Boss(models.Model):
    l_username = models.CharField(max_length=32, unique=True) #布老板的名字
    l_tell = models.CharField(max_length=64) #布老板的电话
    class Meta:
        db_table = 'fly_boss'


class Cart(models.Model):
    c_bupi = models.ForeignKey(Bupi, on_delete=models.CASCADE)  # 关联的布
    # c_time = models.DateField(auto_now_add=True) #入库时间
    c_meter = models.FloatField(default=0)  # 该布入库的米数
    class Meta:
        db_table = 'fly_cart'


class Order(models.Model):
    o_allprice = models.FloatField(default=0)    #总价格
    o_meters = models.FloatField(default=0)    #总米数
    o_pishu = models.IntegerField(default=0)  #总匹数
    o_time = models.DateTimeField(auto_now_add=True)   #入库时间
    class Meta:
        db_table = 'fly_order'

class Orderbus(models.Model):
    # o_bupi = models.ForeignKey(Bupi, on_delete=models.CASCADE)  # 关联的布匹
    o_bupi = models.CharField(max_length=100)  # 布匹名字
    o_order = models.ForeignKey(Order, on_delete=models.CASCADE)  # 关联的订单
    o_price=models.FloatField(default=0)  # 布匹的一米的进价
    o_meter = models.FloatField(default=0)  # 一匹布入库的米数
    class Meta:
        db_table = 'fly_order_bus'

class Cairecord(models.Model):
    cai_bupin=models.CharField(max_length=100)  #裁剪的布品名字
    twonine= models.IntegerField(default=0)  #29 的条数
    treezero= models.IntegerField(default=0) #30
    treeone= models.IntegerField(default=0) #31
    treetwo= models.IntegerField(default=0) #32
    cai_price=models.FloatField(default=0) #裁剪一条的价格
    cai_nums=models.IntegerField(default=0) #一次裁的条数
    cai_meter=models.FloatField(default=0)#裁剪的米数
    cai_date=models.DateTimeField(auto_now_add=True)  #裁剪时间

    class Meta:
        db_table = 'fly_caicord'

class Worker(models.Model):
    w_name = models.CharField(max_length=32, unique=True) #工人的名字
    w_tell = models.CharField(max_length=64) #工人的电话
    class Meta:
        db_table = 'fly_worker'


class Pants(models.Model):
    p_name = models.CharField(max_length=100)  # 裤子的名称
    p_nums = models.IntegerField(default=0)  # 该种裤子发放的总条数
    class Meta:
        db_table = 'fly_pants'


class Sendcart(models.Model):
    s_kuname = models.ForeignKey(Pants, on_delete=models.CASCADE)  # 关联的裤子
    s_wname=  models.ForeignKey(Worker, on_delete=models.CASCADE) #关联的工人
    s_cai=  models.ForeignKey(Cairecord, on_delete=models.CASCADE) #关联的裁出的布
    s_price = models.FloatField(default=0) #加工该种布一条的价格

    class Meta:
        db_table = 'fly_sendcart'

class Sendorder(models.Model):
    s_o_worker= models.CharField(max_length=32)  #发放的工人
    s_o_allprice = models.FloatField(default=0)    #总价格
    s_o_nums = models.IntegerField(default=0)    #总条数
    s_o_pishu = models.IntegerField(default=0)  #总匹数
    s_o_time = models.DateTimeField(auto_now_add=True)   #入库时间
    s_o_is_sign=models.BooleanField(default=False)  #是否签收
    s_o_sunhao= models.FloatField(default=0)  #损耗
    s_o_beizhu=models.CharField(max_length=100) #损耗备注
    class Meta:
        db_table = 'fly_sendorder'

class Sendorderitems(models.Model):
    # o_bupi = models.ForeignKey(Bupi, on_delete=models.CASCADE)  # 关联的布匹
    soi_pname = models.CharField(max_length=64)  # 裤名
    soi_order = models.ForeignKey(Sendorder, on_delete=models.CASCADE)  # 关联的订单
    soi_price=models.FloatField(default=0)  # 该匹布的加工价格
    soi_nums = models.IntegerField(default=0)  # 该匹布的裁出的条数
    soi_caiid =  models.IntegerField(default=0)  #来源id
    soi_caibupin=models.CharField(max_length=64) #来源布品
    soi_is_sign=models.BooleanField(default=False) #一条发放记录是否签收

    class Meta:
        db_table = 'fly_sendorder_items'

class Flyuser(models.Model):
    u_username = models.CharField(max_length=32,unique=True)
    u_password = models.CharField(max_length=256)
    class Meta:
        db_table = 'fly_user'

