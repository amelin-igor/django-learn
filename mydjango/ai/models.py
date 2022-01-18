from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
#from gcharts import GChartsManager

User = get_user_model()

# Create your models here.
class Metering(models.Model):
    meter_title = models.CharField('название измерения', max_length = 200) # (кличка) или рег номер животного
    meter_text = models.TextField('текст статьи')
    meter_temperature = models.IntegerField('температура', default=0)
    meter_humidity = models.IntegerField('влажность', default=0)
    meter_CO2 = models.IntegerField('CO2', default=0)
    meter_CH4 = models.IntegerField('CH4', default=0)
    meter_N2O = models.IntegerField('N2O', default=0)
    meter_datetime = models.DateTimeField('дата публикации')
    meter_identificator = models.CharField(max_length=10, verbose_name='Идентификатор копмлекта (аппаратуры)',
                                     default='00001')
    def __str__(self):
        #return self.meter_title
        return 'Мониторинг: {}'.format(self.meter_identificator +" / "+ self.meter_title +" / "+ str(self.meter_datetime))

    def was_measured_recently(self):
        return self.meter_datetime >= (timezone.now() - datetime.timedelta(days = 7))

    class Meta:
        verbose_name = 'Измерение'
        verbose_name_plural = 'Измерения'

class Note(models.Model):
    metering = models.ForeignKey(Metering, on_delete = models.CASCADE)
    author_name = models.CharField('имя автора', max_length = 50)
    comment_text = models.CharField('текст комментария', max_length = 1200)

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name= 'Пользователь', on_delete = models.CASCADE)
    phone = models.CharField ( max_length = 20, verbose_name= 'Номер телефона')
    bank = models.CharField(max_length=50, verbose_name='Банк')
    account = models.IntegerField('account', default=0)
    datetime = models.DateTimeField('дата операции')

    def __str__(self):
        return 'Покупатель: {}'.format(self.user.username)

    class Meta:
        verbose_name = 'Действие клиентов PD '
        verbose_name_plural = 'Действия клиентов PD '

class Customerrec(models.Model):
    user = models.ForeignKey(User, verbose_name= 'Пользователь', on_delete = models.CASCADE)
    phone = models.CharField ( max_length = 20, verbose_name= 'Номер телефона')
    adres = models.CharField(max_length=20, verbose_name='Адрес', null=True)
    client_name = models.CharField(max_length=50, verbose_name='Наименование клиента', null=True)
    client_name_full = models.CharField(max_length=50, verbose_name='Полное наименование клиента', null=True)
    country = models.CharField(max_length=50, verbose_name='Страна', null=True)
    inn = models.CharField(max_length=20, verbose_name='ИНН', null=True)
    kpp = models.CharField(max_length=20, verbose_name='КПП', null=True)
    ogrn = models.CharField(max_length=20, verbose_name='ОГРН', null=True)
    comment = models.CharField(max_length=200, verbose_name='Кодовое слово')
    vid = models.IntegerField('vid', default=0) # вид контрагента 0 - физлицо; 1 -юрлицо; 2 - ИП
    identificator = models.CharField(max_length=10, verbose_name='Идентификатор устройства', default='00001')
    mac = models.CharField(max_length=20, verbose_name='MAC-адрес', default='30:83:98:A2:6B:51')
    # Zoryka mac = 30:83:98:A2:6B:51
    datetime = models.DateTimeField('дата регистрации')

    def __str__(self):
        return 'Покупатель реквизиты: {}'.format(self.user.username)

    class Meta:
        verbose_name = 'Реквизит'
        verbose_name_plural = 'Реквизиты клиентов'

class my_control(models.Model):
    user = models.ForeignKey(User, verbose_name= 'Пользователь', on_delete = models.CASCADE)
    phone = models.CharField ( max_length = 20, verbose_name= 'Номер телефона')
    dev_1 = models.BooleanField( verbose_name='Устройство 1', default = 0)
    dev_2 = models.BooleanField(verbose_name='Устройство 2', default=0)
    dev_3 = models.BooleanField(verbose_name='Устройство 3', default=0)
    comment = models.CharField(max_length=200, verbose_name='Комментарий к действию', default='No comments')
    identificator = models.CharField(max_length=10, verbose_name='Идентификатор копмлекта (аппаратуры)', default='00001')
    datetime = models.DateTimeField('дата действия')

    def __str__(self):
        #return 'Управляющее действие: {}'.format(self.user.username)
        return 'Управляющее действие: {}'.format(self.identificator)

    class Meta:
        verbose_name = 'Состояние вектора управляения '
        verbose_name_plural = 'Состояния векторов управляения '

class device(models.Model):
    user = models.ForeignKey(User, verbose_name= 'Пользователь', on_delete = models.CASCADE)
    mac = models.CharField(max_length=20, verbose_name='MAC-адрес', default='30:83:98:A2:6B:50')
    devname = models.CharField(max_length=20, verbose_name='Имя устройства', default='No Name')
    comment = models.CharField(max_length=200, verbose_name='Комментарий к действию', default='No comments')
    identificator = models.CharField(max_length=10, verbose_name='Идентификатор копмлекта (аппаратуры)', default='00001')
    datetime = models.DateTimeField('дата действия')

    def __str__(self):
        return f'Устройства пользователя: {self.user.username +" / " + self.devname}'

    class Meta:
        verbose_name = 'Устройство '
        verbose_name_plural = 'Устройства '