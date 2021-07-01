from .models import SubscriptionTypes, Subscription, CargoTypes
from django.utils import timezone
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


class Subscrip:
    def __init__(self, user):
        self.user = user

    def create_trial_access(self):
        """После подтверждения регистрации, вызывается этот метод, для создания пробной подписки на 7 дней, на все грузы"""
        subs_types = SubscriptionTypes.objects.get(name='Trial Access')
        date_from = timezone.now()
        date_to = date_from + timedelta(days=7)
        cargos = CargoTypes.objects.all()
        self.__added_base(subs_types, date_from, date_to, cargos)

    def create_subscribe(self, data_post, type_sub):
        """Метод обрабатывает/создает подписки у пользователей
         data_post - данные с пост запроса
         type_subs - тип подписки, которую выбрал пользователь"""
        cargos_post = (dict(data_post)['cargo'])
        cargos = CargoTypes.objects.filter(name__in=cargos_post)
        subs_types = SubscriptionTypes.objects.get(name=type_sub)
        date_from = timezone.now()

        active_subs = Subscription.objects.filter(user=self.user)

        if active_subs.filter(subscription_types__name='Free Access'):
            # Если у пользователь нет подписок, создаем подписку на те грузы которые он выбрал
            months = 1 if type_sub == '1 MONTH' else 6
            date_to = date_from + relativedelta(months=months)
            self.__added_base(subs_types, date_from, date_to, cargos)
            Subscription.objects.filter(user=self.user, subscription__name='Free Access').delete()


        elif type_sub == '1 MONTH':
            if active_subs.filter(subscription_types__name='Trial Access'):
                active_subs = active_subs.get(subscription_types__name='Trial Access')

                # Дата которая осталась с подписки 'Trail Acces' добавляем к новой подписке
                date_from_old = active_subs.date_from.strftime('%Y-%m-%d')
                date_to_old = active_subs.date_to.strftime('%Y-%m-%d')
                date_remainder = self.__days_between(date_from_old, date_to_old)
                date_to = date_from + relativedelta(months=+1) + timedelta(days=date_remainder)

                # Удаление груза с подписки
                cargos_id = []
                for id in cargos.values('pk'):
                    cargos_id.append(*id.values())
                active_subs.cargo.remove(*cargos_id)

                # Если у пользователя не осталось активных пробных подписок с грузами, удаление подписку 'Trial Access'
                quan_cargo = active_subs.cargo.all()
                if len(quan_cargo) == 0:
                    active_subs.delete()

            else:
                date_to = date_from + relativedelta(months=+1)

            self.__added_base(subs_types, date_from, date_to, cargos)


        elif type_sub == '6 MONTHS':
            # Проходимся циклом по каждому грузу, выбраному пользователем
            for cargo in cargos_post:
                cargos = CargoTypes.objects.filter(name=cargo)

                # Если на груз уже есть подписка, суммируем даты с старой подпиской , удаляем груз с старой подписки
                if active_subs.filter(user=self.user, cargo__name=cargo):
                    active_subscription = Subscription.objects.get(user=self.user, cargo__name=cargo)
                    date_from_old = active_subscription.date_from.strftime('%Y-%m-%d')
                    date_to_old = active_subscription.date_to.strftime('%Y-%m-%d')
                    date_remainder = self.__days_between(date_from_old, date_to_old)
                    date_to = date_from + relativedelta(months=+6) + timedelta(days=date_remainder)

                    # Eсли груз в подписке последний, удаляем подписку
                    if len(active_subscription.cargo.all()) == 1:
                        active_subscription.delete()
                    else:
                        active_subscription.cargo.remove(cargos[0].id)

                else:
                    date_to = date_from + relativedelta(months=+6)
                self.__added_base(subs_types, date_from, date_to, cargos)


    def __added_base(self, subs_types, date_from, date_to, cargos):
        """Метод заносит информацию в бд
        subs_types - тип подписки
        date_from - дата начала подписки
        date_to - дата окончания подписки
        cargos - список грузов, на которые пользователь подписывается"""
        subscription_create = Subscription(user=self.user,
                                           subscription_types=subs_types,
                                           date_from=date_from,
                                           date_to=date_to)
        subscription_create.save()
        subscription_create.cargo.set(cargos)

    def __days_between(self, d1, d2):
        """Метод находит кол-во дней, между даты начала подписки а даты окончания подписки
        d1 - сколько осталось у пользователя дней подписки
        d2 - сколько дней выбрал пользователь"""
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)

    @property
    def get_active_subscription(self):
        """Метод возвращает активные подписки пользователя"""
        if Subscription.objects.filter(user=self.user, subscription_types__name='Free Access'):
            return None
        else:
            return Subscription.objects.filter(user=self.user)

    @property
    def get_cargo_not_user(self):
        """Метод возвращает список подписок, которых нет у пользователя"""
        subscription = Subscription.objects.values('cargo__name').filter(user=self.user)

        cargo_activ_1month = subscription.filter(subscription_types__name__in=['1 MONTH', '6 MONTHS'])
        cargo_activ_6months = subscription.filter(subscription_types__name='6 MONTHS')
        cargos_not_user_1month = CargoTypes.objects.exclude(name__in=cargo_activ_1month)
        cargos_not_user_6months = CargoTypes.objects.exclude(name__in=cargo_activ_6months)

        return {'1_month': cargos_not_user_1month, '6_months': cargos_not_user_6months}
