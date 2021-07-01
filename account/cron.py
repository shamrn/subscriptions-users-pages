from .models import Subscription,SubscriptionTypes
from django.utils import timezone


def check_subscription():
    """Функция запускается каждый час ( в setting.py > CRONJOBS , возможно изменить время)
    функция проверяет, если у пользователя истекла подписка, он ее удаеляет,
    если удаленная подписка была последняя, он ставит пользователю статус Free Access"""

    current_date = timezone.now()
    subscriptions = Subscription.objects.filter(date_to__lte=current_date)

    for sub in subscriptions:
        user = sub.user
        subs_user = Subscription.objects.filter(user=user)
        quan_sub = [x.subscription for x in subs_user]

        if len(quan_sub) == 1:
            subscription_types = SubscriptionTypes.objects.get(name='Free Access')
            Subscription.objects.create(user=user, subscription=subscription_types)

        sub.delete()