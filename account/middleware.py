from django.utils.deprecation import MiddlewareMixin
from .models import PortUser,Ip
from ipware import get_client_ip

class IPMiddleware(MiddlewareMixin):
    """Функция отслеживает ip адреса пользователей"""

    def process_request(self, request):
        if request.user.is_authenticated:
            client_ip, is_routable = get_client_ip(request)
            if not Ip.objects.filter(ip=client_ip).exists():
                user = PortUser.objects.get(email=request.user)
                ip_create = Ip(ip=client_ip,quantity_user=1)
                ip_create.save()
                ip_create.user.add(user)
                user.quantity_ip = int(user.user_ip.all().count()) + 1
                user.save()
                user.user_ip.add(ip_create)
            else:
                if not PortUser.objects.filter(email=request.user, user_ip__ip=client_ip).exists():
                    user = PortUser.objects.get(email=request.user)
                    ip = Ip.objects.get(ip=client_ip)
                    ip.quantity_user = int(ip.user.all().count()) + 1
                    ip.save()
                    ip.user.add(user)
                    user.quantity_ip = int(user.user_ip.all().count()) + 1
                    user.save()
                    user.user_ip.add(ip)

