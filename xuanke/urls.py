from django.contrib import admin
from django.urls import path
from xuanzuo.views import WechatLoginView, SeatApiView, SeatListApiView


# def trigger_error(request):
#     division_by_zero = 1 / 0
urlpatterns = [
    path('admin/', admin.site.urls),
    path('member/login', WechatLoginView.as_view()),
    path('seat', SeatApiView.as_view()),
    path('seatList', SeatListApiView.as_view()),
    # path('sentry-debug/', trigger_error),
]
