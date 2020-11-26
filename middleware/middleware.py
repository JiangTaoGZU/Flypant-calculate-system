from django.http import JsonResponse,HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from APP.models import Flyuser
REQUILE_LOGIN_JSON = [
    # '/axf/addtocart/',
    # '/axf/subtocart/',
    # '/axf/changecartstate/',
    # '/axf/makeorder/',

]
REQUILE_LOGIN = [
    '/fly/bupi/',
    '/fly/bed/',
    '/fly/sign/',
    '/fly/jiagong/',
    '/fly/index/',
    '/fly/',
    '/fly/indb/',
    '/fly/orderlist/',
    '/fly/sendcart/',
    '/fly/sendorderlist/',
    '/fly/signlistbyworker/',
    '/fly/signdetail/',
]

REQUILE_FEI = [
    '/fly/bupi/',
    '/fly/orderlist/',
    '/fly/buboss/',
    '/fly/butype/',
    '/fly/indb/',

]

class LoginMiddleware(MiddlewareMixin):
    def process_request(self,request):
        # if request.path in REQUILE_LOGIN_JSON:
        #     user_id = request.session.get('user_id')
        #     if user_id:
        #         try:
        #              print('哈哈')
        #              user = Flyuser.objects.get(pk=user_id)
        #              request.user = user #将user赋值给request作为一个参数
        #         except:
        #             print('哈哈哈')
        #             data={
        #                 'status':301,
        #                 'msg':'user not avaliable'
        #             }
        #             # return redirect(reverse('axf:login')),由于重定向是浏览的行为，所以不能直接在中间件（也就是服务器）重定向,ps:由于这个请求是在点击+时js文件geujson触发的，所以必须返回jason response
        #             return JsonResponse(data=data)
        #     else:
        #         print('哈哈哈哈')
        #         data = {
        #             'status': 301,
        #             'msg': 'user not login'
        #         }
        #         return JsonResponse(data=data)  #如果发现用户没有登录，中间件这里直接返回浏览器，不再到views
        #         # return redirect(reverse('axf:login'))

        if request.path in REQUILE_LOGIN :
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = Flyuser.objects.get(pk=user_id)
                    print(user.u_username)
                    if user.u_username!='jxb'and request.path in REQUILE_FEI:
                        return HttpResponse("当前用户不允许查看！")

                    # request.user = user  # 将user赋值给request作为一个参数
                except:
                    return redirect(reversed('fly:login')),
            else:
                print('嘿嘿嘿')
                return redirect(reverse('fly:login'))