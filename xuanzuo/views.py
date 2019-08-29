from django.shortcuts import render
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
from .models import Metting, UserMetting
User = get_user_model()
import json
import datetime
from rest_framework import serializers
# Create your views here.
class WechatLoginView(APIView):
    """
    微信登录逻辑
    """

    def post(self, request):
        # 前端发送code到后端,后端发送网络请求到微信服务器换取openid
        code = request.data.get('code')
        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(settings.APP_ID, settings.APP_KEY, code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = res['openid'] if 'openid' in res else None
        # session_key = res['session_key'] if 'session_key' in res else None
        if not openid:
            return Response({'message': '微信调用失败'}, status=status.HTTP_503)

        # 判断用户是否第一次登录
        try:
            user = User.objects.get(openid=openid)
        except Exception:
            # 微信用户第一次登陆,新建用户
            username = request.data.get('nickName')

            sex = request.data.get('gender')
            avatar = request.data.get('avatarUrl')

            user = User.objects.create(username=username, sex=sex, avatar=avatar, openid=openid)
            user.set_password(openid)

        # 手动签发jwt
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        resp_data = {
            "user_id": user.id,
            "username": user.username,
            "avatar": user.avatar,
            "token": token,
        }

        return Response(resp_data)

class MettingSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        week_day = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期日',
        }
        ret['time'] = '未指定时间'
        date = instance.time
        if instance.time is not None:
            # date = datetime.datetime.strptime(instance.time, datetime.datetime.strptime(str,'%Y-%m-%dT%H:%M:%SZ'))
            ret['time'] =  str(date.year) +'-'+ str(date.month) +'-'+ str(date.day)\
                           +' '+ week_day[date.weekday()] + ' ' + str(date.hour)+ ':'+\
                           str(date.minute)
        return ret
    class Meta:
        model = Metting
        fields = "__all__"

class SeatListApiView(APIView):
    def get(self, request):
        # result = Metting.objects.all().values()
        serializer = MettingSerializer(instance=Metting.objects.all(),many=True, read_only=True)
        result = serializer.data
        return Response(result)

class SeatApiView(APIView):

    def get(self, request):
        result = dict(seatArr="", name="")
        metting_obj = Metting.objects.last()
        result["seatArr"] = metting_obj.result
        result["name"] = metting_obj.mettingName
        return Response(result)

    def post(self, request):

        seatArr = request.data.get('seatArr')
        user_id = request.data.get('user_id')

        metting_obj = Metting.objects.last()
        try:
            user_obj = User.objects.get(pk=int(user_id))
        except User.DoesNotExist:
            return Response({'message': '没有取到用户信息'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        print(user_obj.metting.all())
        UserMetting.objects.filter(user_id=int(user_id), metting_id=metting_obj.id)
        if UserMetting.objects.filter(user_id=int(user_id), metting_id=metting_obj.id):
            return Response({'message': '座位已经被使用'}, status=status.HTTP_504_GATEWAY_TIMEOUT)

        UserMetting.objects.create(user=user_obj, metting=metting_obj)

        metting_obj.result = seatArr
        metting_obj.save()

        return Response({'message': '占座成功'})