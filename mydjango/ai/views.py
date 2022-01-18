# from bokeh.models import Scatter
import logging

from bokeh.embed import components
from bokeh.plotting import figure, curdoc
from bokeh.models import Range1d, LinearAxis

import matplotlib

from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from .models import Metering, Customer, Customerrec, Note, my_control, device

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .forms import AuthUserForm, RegisterUserForm, CustomCheckbox
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django import forms

from django.core.mail import send_mail
# import secrets
import uuid
import os
from .forms import account_check, get_ident
from django.contrib.auth.views import PasswordResetView, PasswordChangeView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeDoneView
# import json
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import my_controlSerializer
import numpy as np
from bokeh.layouts import gridplot
from scipy.cluster.hierarchy import *

from io import BytesIO
import base64
import matplotlib.pyplot as plt
from django.contrib.auth import get_user_model

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from datetime import datetime, timedelta



matplotlib.use('Agg')

# import numpy as np
#import pandas as pd

# matplotlib.style.use('ggplot')

# from bokeh.resources import INLINE
# import plotly.plotly as py
# import plotly.graph_objs as go
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# from  plotly.offline.offline import _plot_html

# from bokeh.util.string import encode_utf8


User = get_user_model()

password_old = {
    'FERM1': '1',
    'FERM2': '2',
    'FERM3': '3',
}

password = {
    '00001': '6546556987',
    '00002': '36645954',
    '00003': '984544559',
    '00004': '4565654123',
    '00005': '4566586123',
    '00006': '33847866558',
    '00007': '166954887',
    '00008': '111265587',
    '00009': '8642589',
    '00010': '1155887',
    '00011': '2865449762',
    '00012': '159755432',
    '00013': '259755432',
    '00033': '597554321',
}


# http://127.0.0.1:8000/add/?login=FERM1&pasw=1&name=Buryonka&t=38&h=25&co2=7&ch4=31&n2o=17
# http://127.0.0.1:8000/add/?login=FERM2&pasw=2&name=Vestka&t=38&h=25&co2=2&ch4=21&n2o=11

# Create your views here.

# def test(request):
#    return HttpResponse("<h3>ТЕСТОВАЯ СТРАНИЦА ИСКУССТВЕННОГО ИНТЕЛЛЕКТА</h3>")

def start(request):
    print('start')
    X = []
    Y = []
    if request.user.is_authenticated == True:
        try:
            a = User.objects.get(id=request.user.id)
        except:
            raise Http404("Пользователь отсутствует")
        print("User.is_authenticated")
        print(request.user.is_authenticated)
        print(request.user.id)
        print(request.user.id)
        print(request.user.first_name)
        print(request.user.last_name)
        customer = a.customer_set.order_by('id')[:]
        for cus in customer:
            X.append(cus.account)
            Y.append(cus.bank)
        # print(X)
        # print(Y)
    else:
        print("User.is_not_authenticated")
        print(request.user.is_authenticated)
        X.append("0")
        Y.append(" ")

    if len(X) == 0:
        X.append("0")

    return render(request, 'ai/start.html', {'Acc': X[-1]})


def page1(request):
    return render(request, 'ai/page1.html')


def page2(request):
    return render(request, 'ai/page2.html')


def add(request):
    print('add')
    f = "234"
    # now = datetime.datetime.now()
    now = timezone.now()
    nameandpaswcorrect = False
    cowlog = open('cow.log', 'a')
    try:
        login = request.GET.get('login')
        pasw = request.GET.get('pasw')
        t = request.GET.get('t')
        h = request.GET.get('h')
        pcname = 'pcname'

        name = request.GET.get('name')
        co2 = request.GET.get('co2')
        ch4 = request.GET.get('ch4')
        n2o = request.GET.get('n2o')
        mt = "Пояснения "
        data = 't = ' + str(t) + ' h = ' + str(h) + ' CO2 = ' + str(co2) + ' CH4 = ' + str(ch4) + ' n2o = ' + str(n2o)

        if login != "00001":
            try:
                print('from Customerrec try...')
                q = Customerrec.objects.filter(identificator=login)

                for LI in q:
                    f = LI.comment
                print('codeword =')
                print(f)

            except:
                print('from add Customerrec except:')
                return Response({"add": "wrong codeword - data rejected"})

        if f == pasw or password[login]== pasw:
            nameandpaswcorrect = True

        if nameandpaswcorrect == True:
            a = 'YES_'
            logging.info('user: ' + login)
            if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
                cowlog.write('user: ' + login + ' ' + str(now) + ' IP:' + request.environ[
                    'REMOTE_ADDR'] + ' / ' + pcname + ' / ' +
                             data + ' / ' + '\n')
            else:
                cowlog.write('user: ' + login + ' ' + str(now) + ' IP:' + request.environ[
                    'HTTP_X_FORWARDED_FOR'] + ' / ' + pcname + ' / ' +
                             "data" + ' / ' + '\n')
                # if behind a proxy
        else:
            a = 'Wrong user credentials!_'
            logging.warning('user ' + login + ': Wrong user credentials!')
            if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
                cowlog.write('user: ' + login + ' ' + str(now) + ' IP:' + request.environ[
                    'REMOTE_ADDR'] + ' / ' + pcname + ' / ' +
                             data + ' / ' + ': Wrong user credentials!' + '\n')
            else:
                cowlog.write('user: ' + login + ' ' + str(now) + ' IP:' + request.environ[
                    'HTTP_X_FORWARDED_FOR'] + ' / ' + pcname + ' / ' +
                             data + ' / ' + ': Wrong user credentials!' + '\n')
                # if behind a proxy

    except ValueError:
        logging.warning('user ' + login + ': Wrong user name_' + '\n')
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            cowlog.write('user: ' + login + ' ' + str(now) + ' IP:' + request.environ[
                'REMOTE_ADDR'] + ' / ' + pcname + ' / ' +
                         data + ' / ' + ': Wrong user name!' + '\n')
        else:
            cowlog.write('user: ' + login + ' ' + str(now) + ' IP:' + request.environ[
                'HTTP_X_FORWARDED_FOR'] + ' / ' + pcname + ' / ' +
                         data + ' / ' + ': Wrong user name!' + '\n')


    m = Metering(meter_identificator=login, meter_title=name, meter_text=mt, meter_temperature=t, meter_humidity=h,
                 meter_CO2=co2,
                 meter_CH4=ch4, meter_N2O=n2o, meter_datetime=now)
    m.save()

    v1 = my_condition_2(request)

    return JsonResponse(v1, safe=False)


def show(request):
    q = Metering.objects.filter(meter_title="Mumuka")
    z = {'metter_of_buryonka': q}
    return render(request, 'ai/show.html', z)


def graph1(request):
    try:
        # q =  Metering.objects.get(meter_title ="Mumuka")
        q = Metering.objects.filter(meter_title="Mumuka")
        # Yarushka
    except:
        raise Http404("Нет запрашиваемых данных")

    latest_data_list = q.order_by('-meter_datetime')[:3]
    # p = figure(title="Данные датчиков", x_axis_label='время в кварталах', y_axis_label='вероятность дефолта')
    # x1 =  latest_data_list.meter_datetime
    x1 = [1, 2, 3]
    # y1 = latest_data_list.Metering.meter_temperature
    y1 = [2, 4, 8]
    # y2 = latest_data_list.meter_humidity
    y2 = [10, 4, 1]
    # p.line(x1, y1, legend_label="y1", line_width=2, color='red')
    # p.line(x1, y2, line_width=2, color='green')
    # grab the static resources
    # js_resources = INLINE.render_js()
    # css_resources = INLINE.render_css()
    # script, div = components(p)
    # html = render(         "graph1.html",p)
    # return encode_utf8(html)
    # return html
    z = {'metter_of_buryonka': latest_data_list}

    return render(request, 'ai/graph1.html', z)


def graph2(request):
    pass


def addcom(request, metering_id):
    latest_comments_list = []
    try:
        q = Metering.objects.filter(id=metering_id)
    except:
        raise Http404("Нет запрашиваемых данных")
        # latest_comments_list = ["Нет запрашиваемых данных"]
        # latest_comments_list = append("Нет запрашиваемых данных")
    # latest_data_list = q.order_by('-meter_datetime')[:4]
    # try:
    #     latest_comments_list = q.note_set.order_by('-id')[:10]
    # except:
    #      raise Http404("Нет комментариев к измерению")

    # return render(request, 'ai/addcom.html', {'metter_of_buryonka': q, 'latest_comments_list': latest_comments_list})
    return render(request, 'ai/form1.html',
                  {'metter_of_buryonka': q, 'latest_comments_list': latest_comments_list, 'name': 'name'})


def starter(request, meter_title, chisizm):
    from sklearn import preprocessing
    from scipy.spatial.distance import pdist

    from sklearn.cluster import KMeans
    # Acc = account_check(request)
    # ident = get_ident(request)
    now = timezone.now()
    voc = get_ident(request)
    print('voc = ')
    print(voc)
    ident = voc['ident']

    RegFF = voc['RFF']
    if RegFF == False and request.user.is_authenticated:
        codegen_emailsend(request)
        return render(request, 'ai/recvizits.html')

    print(now)

    Metering.objects.filter(meter_datetime__lte=timezone.now() - timezone.timedelta(days=30)).delete()
    now = timezone.now()
    print(now)

    try:
        q = Metering.objects.filter(meter_title=meter_title, meter_identificator=ident)
        now = timezone.now()
        print(now)
    except:
        raise Http404("Нет запрашиваемых данных")
    y3 = []

    for data in q:
        y3.append(data.meter_humidity)
    len_all = len(y3)
    print('len_all=')
    print(len_all)

    latest_data_list = q.order_by('-meter_datetime')[:chisizm]
    z = {'metter_of_buryonka': latest_data_list}

    x0 = []
    y1 = []
    y2 = []
    y4 = []
    # d = []
    number = []
    i = 1
    # format = '%b %d %Y %I:%M%p' # Формат
    format = '%H:%M'  # Формат

    for data in latest_data_list:
        # d=str(datetime.date(data.meter_datetime))
        x0.append(data.meter_datetime)
        y1.append(data.meter_temperature)
        y2.append(data.meter_humidity)
        y4.append(data.meter_CO2)

        # n.append(data.meter_humidity)
        number.append(i)
        i = i + 1

    name_cow = data.meter_title
    print(name_cow)


    # result =np.column_stack((latest_data_list, number))

    if name_cow == 'Yarushka':
        nabobj_name = 'Объект 1'
        gas_name = 'LPG'
    elif name_cow == 'Mumuka':
        nabobj_name = 'Объект 2'
        gas_name = 'CO2'
    elif name_cow == 'Francheska':
        nabobj_name = 'Объект 3'
        gas_name = 'LPG'
    elif name_cow == 'Buryonka':
        nabobj_name = 'Объект 4'
        gas_name = 'Smoke gas'
    elif name_cow == 'Vestka':
        nabobj_name = 'Объект 5'
        gas_name = 'CH4'
    else:
        nabobj_name = 'Объект NoName'
        #gas_name = 'UnKnown gas'
        gas_name = 'gas'

    nabobj_name = def_comment(name_cow)

    x1 = range(len(y1))
    print(len(y1))
    # for el in x0:
    #   d.append(el)
    # Формируем список с обратной последовательностью
    y10 = y1[::-1]
    y20 = y2[::-1]
    y40 = y4[::-1]
    x10 = x0[::-1]

    # последние элементы списков
    date_last = x10[-1]
    y1_last = y10[-1]
    y2_last = y20[-1]
    y4_last = y40[-1]

    date_first = x10[0]
    y1_first = y10[0]
    y2_first = y20[0]

    # y2 = latest_data_list.meter_humidity
    # plot = figure()
    # plot.circle(x1, y1, size=5, color="blue")
    # plot.circle(x1, y2, size=5, color="red")
    plot = figure(
        plot_width=900,
        tools="pan, box_zoom, reset, save",
        x_axis_label='номер измерения', y_axis_label='температура, влажность'
    )

    plot.line(x1, y10, legend_label="температура, С", line_color="red")
    # plot.line(x1, y2, legend="влажность, %", line_color="blue", line_dash="4 4")
    plot.line(x1, y20, legend_label="влажность, %", line_color="blue")
    plot.line(x1, y40, legend_label="концентрация, ppm", line_color="green")

    name_dop_osi = 'концентрация ' + gas_name + ', ppm'
    # script, div = components(plot)
    script, div = components(myplot_2(request, x1, y10, y20, y40, 'температура, °С', 'влажность, %', name_dop_osi))
    # print(div)
    # x = np.concatenate((y40, y10, y20))
    # y = np.concatenate((y10, y20, y40))

    x = y20
    y = y40
    x_axis = 'Влажность, %'
    y_axis = 'Концентрация, ppm'
    title = "Распределение влажности и концентрации газа"
    layout = my_layout(x, y, x_axis, y_axis, title)
    script2, div2 = components(layout)

    x = y10
    y = y20
    x_axis = 'Температура, С'
    y_axis = 'Влажность, %'
    title = "Распределение температуры и влажности"
    layout = my_layout(x, y, x_axis, y_axis, title)
    script3, div3 = components(layout)

    x = y10
    y = y40
    x_axis = 'Температура, С'
    y_axis = 'Концентрация, ppm'
    title = "Распределение температуры и и концентрации газа"
    layout = my_layout(x, y, x_axis, y_axis, title)
    script4, div4 = components(layout)

    t_median = np.median(y10)
    t_mean = np.mean(y10)
    t_std = np.std(y10)
    h_median = np.median(y20)
    h_mean = np.mean(y20)
    h_std = np.std(y20)
    g_median = np.median(y40)
    g_mean = np.mean(y40)
    g_std = np.std(y40)
    t_mean = toFixed(t_mean, 2)
    t_std = toFixed(t_std, 2)
    h_mean = toFixed(h_mean, 2)
    h_std = toFixed(h_std, 2)
    g_mean = toFixed(g_mean, 2)
    g_std = toFixed(g_std, 2)
    corr_t_h = np.corrcoef(y10, y20)[1, 0]
    corr_t_h = toFixed(corr_t_h, 4)
    corr_t_g = np.corrcoef(y10, y40)[1, 0]
    corr_t_g = toFixed(corr_t_g, 4)
    corr_h_g = np.corrcoef(y20, y40)[1, 0]
    corr_h_g = toFixed(corr_h_g, 4)
    corr_t_h_g = np.corrcoef([y10, y20, y40])

    if len(y1) > 900:

        data_for_clust = np.column_stack((y10, y20, y40))
        dataNorm = preprocessing.scale(data_for_clust)
        # вычислим растояние между каждым набором данных
        data_dist = pdist(dataNorm, 'euclidean')
        # иерархическая кластеризация
        data_linkage = linkage(data_dist, method='average')
        # Метод локтя - определяем опттим колич сегментов
        # Показывает сумму внутри групповых вариаций
        last = data_linkage[-10:, 2]
        print('last=')
        print(last)
        last_rev = last[::-1]
        idxs = np.arange(1, len(last) + 1)
        # plt.plot(idxs, last_rev)
        acceleration = np.diff(last, 2)
        acceleration_rev = acceleration[::-1]
        # plt.plot(idxs[:-2] + 1, acceleration_rev)
        # plt.show()
        clusters = acceleration_rev.argmax() + 2
        print('clusters:', clusters)

        p5 = figure(
            plot_width=900,
            tools="pan, box_zoom, reset, save",
            x_axis_label='', y_axis_label='расстояние между измерениями',
            title="Метод локтя - определяем опттимальное количество сегментов"
        )
        p5.line(idxs, last_rev, legend_label="расстояние", line_color="red")
        p5.line(idxs[:-2] + 1, acceleration_rev, legend_label="2-я производная (ускорение)", line_color="blue")
        # p2.circle([1, 2.5, 3, 2], [2, 3, 1, 1.5], radius=0.3, alpha=0.5)
        script5, div5 = components(p5)

        nClaster = 5

        graphic = fancy_dendrogram(
            data_linkage,
            truncate_mode='lastp',
            p=nClaster,
            leaf_rotation=90.,
            leaf_font_size=12.,
            show_contracted=True,
            annotate_above=10,
        )


        return render(request, 'ai/starter.html', {'script': script, 'div': div,
                                               'script2': script2, 'div2': div2,
                                               'script3': script3, 'div3': div3,
                                               'script4': script4, 'div4': div4,
                                               'script5': script5, 'div5': div5,
                                               'metter_of_buryonka': latest_data_list,
                                               'len_all': len_all,
                                               'date_last': date_last,
                                               'date_first': date_first,
                                               't_last': y1_last,
                                               'h_last': y2_last,
                                               'CO2_last': y4_last,
                                               'data': data,
                                               'nabobj_name': nabobj_name,
                                               'gas_name': gas_name,
                                               'name_cow': name_cow,
                                               'number': number,
                                               't_median': t_median,
                                               't_mean': t_mean,
                                               't_std': t_std,
                                               'h_median': h_median,
                                               'h_mean': h_mean,
                                               'h_std': h_std,
                                               'g_median': g_median,
                                               'g_mean': g_mean,
                                               'g_std': g_std,
                                               'corr_t_h': corr_t_h,
                                               'corr_t_g': corr_t_g,
                                               'corr_h_g': corr_h_g,
                                               'corr_t_h_g': corr_t_h_g,
                                               'clusters': clusters,
                                               'graphic': graphic,
                                               'chisizm': chisizm,
                                               # 'Acc': Acc
                                               })
    else:
        return render(request, 'ai/starter.html', {'script': script, 'div': div,
                                               'script2': script2, 'div2': div2,
                                               'script3': script3, 'div3': div3,
                                               'script4': script4, 'div4': div4,
                                               'metter_of_buryonka': latest_data_list,
                                               'len_all': len_all,
                                               'date_last': date_last,
                                               'date_first': date_first,
                                               't_last': y1_last,
                                               'h_last': y2_last,
                                               'CO2_last': y4_last,
                                               'data': data,
                                               'nabobj_name': nabobj_name,
                                               'gas_name': gas_name,
                                               'name_cow': name_cow,
                                               'number': number,
                                               't_median': t_median,
                                               't_mean': t_mean,
                                               't_std': t_std,
                                               'h_median': h_median,
                                               'h_mean': h_mean,
                                               'h_std': h_std,
                                               'g_median': g_median,
                                               'g_mean': g_mean,
                                               'g_std': g_std,
                                               'corr_t_h': corr_t_h,
                                               'corr_t_g': corr_t_g,
                                               'corr_h_g': corr_h_g,
                                               'corr_t_h_g': corr_t_h_g,
                                               'chisizm': chisizm,
                                               # 'Acc': Acc
                                               })



def leave_comment2(request, metering_id):
    try:
        a = Metering.objects.get(id=metering_id)
    except:
        raise Http404("Статья не найдена!")
    a.note_set.create(author_name=request.POST['name'], comment_text=request.POST['text'])

    return HttpResponseRedirect(reverse('ai:addcom', args=(a.id,)))


# def detal2(request , metering_id):
#    try:
#        a = Metering.objects.get(id = metering_id)
# except:
#    raise Http404("Статья не найдена!")

# latest_comments_list = a.note_set.order_by('-id')[:10]

# return render(request, 'ai/addcom.html', {'metering': a, 'latest_comments_list': latest_comments_list})

def index2(request):
    # latest_metering_list = Metering.objects.order_by('-meter_datetime')[:4]
    latest_metering_list = Metering.objects.all()
    return render(request, 'ai/list2.html', {'latest_metering_list': latest_metering_list})


def nabobj(request):
    # ident = get_ident(request)
    voc = get_ident(request)
    print('voc = ')
    print(voc)

    ident = voc['ident']

    RegFF = voc['RFF']
    if RegFF == False and request.user.is_authenticated:
        codegen_emailsend(request)
        return render(request, 'ai/recvizits.html')

    print('nabobj_ident =')
    print(ident)
    # cow_metering_list = Metering.objects.all()
    cow_metering_list = Metering.objects.filter(meter_identificator=ident)

    # ! этот вариант работаем намного быстрее, но только для датчиков с мак-адресом
    # cow_metering_list = device.objects.filter(identificator=ident)

    X = []
    for cow in cow_metering_list:
        X.append(cow.meter_title)
    XM = set(X)
    y = sorted(list(XM))
    print('sorted(list(XM))=')
    print(y)

    return render(request, 'ai/nabobj.html', {'cow_metering_list': y})


def cows(request, meter_title, chisizm):
    print('cows ')
    chisizm_from_post = request.POST.get('chisizm')
    print('chisizm from POST = ')
    print(chisizm_from_post)
    print('meter_title = ')
    print(meter_title)
    if chisizm_from_post == None:
        chisizm_from_post = chisizm

    return HttpResponseRedirect(reverse('ai:starter', args=(meter_title, chisizm_from_post)))


def pdstart(request):
    print('pdstart_qqq')
    X = []
    Y = []
    if request.user.is_authenticated == True:
        try:
            a = User.objects.get(id=request.user.id)
        except:
            raise Http404("Пользователь отсутствует")
        print("User.is_authenticated")
        print(request.user.is_authenticated)
        print(request.user.id)
        print(request.user.first_name)
        print(request.user.last_name)
        # a = Customer.objects.get(id=request.user.id)

        # m = Customer(phone = '+7(495)7777777',email = "alex@bmail.org", account = 100, user_id = request.user.id)
        # m.save()

        # Cus = Customer.objects.filter(id = request.user.id)
        customer = a.customer_set.order_by('id')[:]

        for cus in customer:
            X.append(cus.account)
            Y.append(cus.bank)

        # print(X)
        # print(Y)

    else:
        print("User.is_not_authenticated")
        print(request.user.is_authenticated)
        X.append("0")
        Y.append(" ")

    if len(X) == 0:
        X.append("0")
    return render(request, 'ai/pdstart.html', {'Acc': X[-1]})


def pdcalc(request):
    # import numpy as np
    import pandas as pd
    from sklearn.preprocessing import StandardScaler  # Стандартизация данных
    import tensorflow
    # from tensorflow
    import keras
    import joblib
    import keras.backend as K
    from keras.utils.generic_utils import get_custom_objects
    import os.path

    regn = request.POST['name']
    print("regn = ")
    print(regn)

    # import adodbapi

    # database = "MosReg.mdb"
    ##constr = 'Provider=Microsoft.Jet.OLEDB.4.0; Data Source=D:\BASE_MDB\MosReg.mdb'
    ##constr = 'Provider=Microsoft.ace.oledb.12.0; Data Source=D:\BASE_MDB\MosReg.mdb'
    # constr = 'Provider=Microsoft.Jet.OLEDB.4.0; Data Source=%s'
    # tablename = "Banks"

    # Подключаемся к базе данных.
    # conn = adodbapi.connect(constr)

    # Создаем курсор.
    # cur = conn.cursor()

    # Получаем все данные.
    # sql = "select * from Banks"
    # sql = "select * from %s" % tablename
    # cur.execute(sql)

    # Показываем результат.
    # result = cur.fetchall()
    # for item in result:
    #   print(item)

    # Завершаем подключение.
    # cur.close()
    # conn.close()

    bank = {
        '1': 'UniCredit Bank',
        '170': 'РН банк',
        '316': 'Home Credit&Finance Bank',
        '354': 'Gazprombank',
        '963': 'Совкомбанк',
        '1000': 'VTB Bank OAO',
        '1326': 'АЛЬФА-БАНК',
        '1481': 'Sberbank',
        '1978': 'МОСКОВСКИЙ КРЕДИТНЫЙ БАНК',
        '2272': 'Rosbank',
        '2268': 'ОАО МТС БАНК',
        '2306': 'Absolut Bank',
        '2748': 'Bank of Moscow',
        '3255': 'Банк ЗЕНИТ ОАО',
        '2210': 'Транскапиталбанк',
        '1920': 'Ланта-Банк',
        '2664': 'АКБ Славия (ЗАО)',
        '1614': 'ЗАУБЕР Банк',
        '436': 'ОАО Банк Санкт-Петербург',
        '1439': 'Банк «Возрождение» (ОАО)',
        '2766': 'ОТП Банк',
        '3016': 'Нордеа Банк',
        '3328': 'Deutsche Bank',
        '3349': 'Russian Agricultural Bank',
        '1052': 'МТИ-банк',
        '3073': 'РГС банк',
        '3176': 'Балтинвестбанк',
        '1460': 'Восточный банк',
        '2209': 'Открытие',
        '1680': 'Сredit Agricole CIB',
        '2494': 'Credit Suisse',
        '2495': 'ING',
        '2557': 'Citibank',
        '2584': 'Кредит Урал Банк',
        '2629': 'JP Morgan',
        '2790': 'ЗАО РОСЭКСИМБАНК',
        '3292': 'Raiffeizenbank',
        '3311': 'Credit Europe Bank',
        '3333': 'Commerzbank Eurazia',
        '3337': 'ЗАО Мидзухо Корпорэйт Банк (Москва)',
        '3340': 'КБ МСП Банк',
        '3390': 'Натиксис Банк (ЗАО)',
        '3407': 'BNP Paribas',
        '3463': 'Ю Би Эс Банк',
        '3465': 'Эм-Ю-Эф-Джи Банк (Евразия)',
        '3470': 'Тойота Банк',
        '3490': 'Goldman Sachs',
        '2879': 'ОАО АКБ Авангард',
        '2707': 'КБ "ЛОКО-Банк" (ЗАО)',
        '2574': 'Банк РМП (ПАО)',
        '2440': 'Металлинвест',
        '2275': 'Уралсиб',
        '2846': 'Система',
        '2156': 'Нефтепромбанк',
        '2914': 'Арес-банк',
        '3124': 'НС–Банк',
        '2241': 'КИВИ Банк',
        '2929': 'ББР Банк',
        '665': 'ГТ банк',
        '2590': 'АК БАРС',
        '2546': 'НОВИКОМБАНК',
        '3261': 'ВНЕШПРОМБАНК',
        '2271': 'КРАНБАНК',
        '1776': 'ОАО Банк Петрокоммерц',
        '1557': 'ВУЗ-банк',
        '1751': 'МОСКОВСКИЙ ОБЛАСТНОЙ БАНК',
        '2110': 'Пересвет',
        '2989': 'Фондсервисбанк',
        '2763': 'Инвестторгбанк',
        '2490': 'Генбанк',
        '912': 'Московский Индустриальный банк',
        '1810': 'Азиатско-Тихоокеанский Банк',
        '3279': 'НБ ТРАСТ',
        '554': 'Солидарность',
        '1581': 'БТА-Казань(ОАО)',
        '1673': 'Банк Майский',
        '2764': 'ТЭМБР-БАНК',
        '2960': 'Славянский кредит',
        '2222': 'Инвесткомбанк БЭЛКОМ',
        '3379': 'Мааксима',

    }

    Dat1 = {
        '0': '1/07/2010',
        '1': '1/10/2010',
        '2': '1/01/2011',
        '3': '1/04/2011',
        '4': '1/07/2011',
        '5': '1/10/2011',
        '6': '1/01/2012',
        '7': '1/04/2012',
        '8': '1/07/2012',
        '9': '1/10/2012',
        '10': '1/01/2013',
        '11': '1/04/2013',
        '12': '1/07/2013',
        '13': '1/10/2013',
        '14': '1/01/2014',
        '15': '1/04/2014',
        '16': '1/07/2014',
        '17': '1/10/2014',
        '18': '1/01/2015',
        '19': '1/04/2015',
        '20': '1/07/2015',
        '21': '1/10/2015',
        '22': '1/01/2016',
        '23': '1/04/2016',
        '24': '1/07/2016',
        '25': '1/10/2016',
        '26': '1/01/2017',
        '27': '1/04/2017',
        '28': '1/07/2017',
        '29': '1/10/2017',
        '30': '1/01/2018',
        '31': '1/04/2018',
        '32': '1/07/2018',
        '33': '1/10/2018',
        '34': '1/01/2019',
        '35': '1/04/2019',
        '36': '1/07/2019',
        '37': '1/10/2019',
        '38': '1/01/2020',
        '39': '1/04/2020',
        '40': '1/07/2020',
        '41': '1/10/2020',
        '42': '1/01/2021',
        '43': '1/04/2021',
    }

    Dat2 = {

        '0': '1/01/2011',
        '1': '1/04/2011',
        '2': '1/07/2011',
        '3': '1/10/2011',
        '4': '1/01/2012',
        '5': '1/04/2012',
        '6': '1/07/2012',
        '7': '1/10/2012',
        '8': '1/01/2013',
        '9': '1/04/2013',
        '10': '1/07/2013',
        '11': '1/10/2013',
        '12': '1/01/2014',
        '13': '1/04/2014',
        '14': '1/07/2014',
        '15': '1/10/2014',
        '16': '1/01/2015',
        '17': '1/04/2015',
        '18': '1/07/2015',
        '19': '1/10/2015',
        '20': '1/01/2016',
        '21': '1/04/2016',
        '22': '1/07/2016',
        '23': '1/10/2016',
        '24': '1/01/2017',
        '25': '1/04/2017',

        '26': '1/07/2017',
        '27': '1/10/2017',
        '28': '1/01/2018',
        '29': '1/04/2018',
        '30': '1/07/2018',
        '31': '1/10/2018',
        '32': '1/01/2019',
        '33': '1/04/2019',
        '34': '1/07/2019',
        '35': '1/10/2019',
        '36': '1/01/2020',
        '37': '1/04/2020',
        '38': '1/07/2020',
        '39': '1/10/2020',
        '40': '1/01/2021',

        '41': '1/04/2021',
        '42': '1/07/2021',
        '43': '1/10/2021',
        '44': '1/01/2022',

        '45': '1/04/2022',
        '46': '1/07/2022',
        '47': '1/10/2022',
        '48': '1/01/2023',
        '49': '1/04/2023',
        '50': '1/07/2023',
        '51': '1/10/2023',
        '52': '1/01/2024',
        '53': '1/04/2024',
        '54': '1/07/2024',
        '55': '1/10/2024',

        '56': '1/01/2025',
        '57': '1/04/2025',
        '58': '1/07/2025',
        '59': '1/10/2025',

        '60': '1/01/2026',
        '61': '1/04/2026',
        '62': '1/07/2026',
        '63': '1/10/2026',

        '64': '1/01/2027',
        '65': '1/04/2027',
        '66': '1/07/2027',
        '67': '1/10/2027',

        '68': '1/01/2028',
        '69': '1/04/2028',
        '70': '1/07/2028',
        '71': '1/10/2028',
        '72': '1/01/2029',

    }

    Dat3 = {

        '0': '1/01/2004',
        '1': '1/04/2004',
        '2': '1/07/2004',
        '3': '1/10/2004',
        '4': '1/01/2005',
        '5': '1/04/2005',
        '6': '1/07/2005',
        '7': '1/10/2005',
        '8': '1/01/2006',
        '9': '1/04/2006',
        '10': '1/07/2006',
        '11': '1/10/2006',
        '12': '1/01/2007',
        '13': '1/04/2007',
        '14': '1/07/2007',
        '15': '1/10/2007',
        '16': '1/01/2008',
        '17': '1/04/2008',
        '18': '1/07/2008',
        '19': '1/10/2008',
        '20': '1/01/2009',
        '21': '1/04/2009',
        '22': '1/07/2009',
        '23': '1/10/2009',
        '24': '1/01/2010',
        '25': '1/04/2010',

        '26': '1/07/2010',
        '27': '1/10/2010',
        '28': '1/01/2011',
        '29': '1/04/2011',
        '30': '1/07/2011',
        '31': '1/10/2011',
        '32': '1/01/2012',
        '33': '1/04/2012',
        '34': '1/07/2012',
        '35': '1/10/2012',
        '36': '1/01/2013',
        '37': '1/04/2013',
        '38': '1/07/2013',
        '39': '1/10/2013',
        '40': '1/01/2014',
        '41': '1/04/2014',
        '42': '1/07/2014',
        '43': '1/10/2014',
        '44': '1/01/2015',
        '45': '1/04/2015',
        '46': '1/07/2015',
        '47': '1/10/2015',
        '48': '1/01/2016',
        '49': '1/04/2016',
        '50': '1/07/2016',
        '51': '1/10/2016',
        '52': '1/01/2017',
        '53': '1/04/2017',
        '54': '1/07/2017',
        '55': '1/10/2017',
        '56': '1/01/2018',
        '57': '1/04/2018',
        '58': '1/07/2018',
        '59': '1/10/2018',
        '60': '1/01/2019',
        '61': '1/04/2019',
        '62': '1/07/2019',
        '63': '1/10/2019',
        '64': '1/01/2020',
        '65': '1/04/2020',
        '66': '1/07/2020',
        '67': '1/10/2020',
        '68': '1/01/2021',
        '69': '1/04/2021',
        '70': '1/07/2021',
        '71': '1/10/2021',
        '72': '1/01/2022',

    }

    # файл для шкалирования (стандартизации) нужно делать в этой процедуре (файл шкалирования из Jupyter Notebook не подходит
    #data = pd.read_csv("M2B_PCZ20210216_B.csv", sep=';')
    #df6 = data[2600:10000]
    #df7 = data[10000:]
    #frames = [df6, df7]
    #df = pd.concat(frames)
    #print('df.shape = ')
    #print(df.shape)
    #df = df.dropna(how='all')
    #print('df.shape(after dropna) = ')
    #print(df.shape)
    # -----------------------------------------------'
    #count = []
    #num_in_diap = []
    ## число диапазонов n
    #n = 100
    #shag = 1 / n

    #for i in range(n + 2):
    #    count.append(0)

    #def rasp(count):
    #    for p in df['52']:
    #        # цикл по диапазонам
    #        for i in range(n + 2):
    #            if p >= i * shag and p < (i + 1) * shag:
    #                count[i] = count[i] + 1
    #                num_in_diap.append(count[i])
    #    return count

    #rasp(count)

    #df = df.assign(num_in_diap=num_in_diap)
    #df = df[df.num_in_diap < 125]
    # -----------------------------------------------'
    #colsm = []
    #for i in range(1, 52):
    #    colsm.append(str(i))

    #y = df['52']
    #X = df[colsm]

    #X = X.apply(pd.to_numeric)
    #scaler = StandardScaler(copy=False).fit(X)
    #X_train = scaler.transform(X)
    #scaler_filename = "scaler_x69a.save"
    #joblib.dump(scaler, scaler_filename)

    now = timezone.now()
    print('pdcalc')
    X = []
    Y = []
    if request.user.is_authenticated == True:
        try:
            a = User.objects.get(id=request.user.id)
        except:
            raise Http404("Пользователь отсутствует")
        print("User.is_authenticated = ", request.user.is_authenticated)
        # print(request.user.is_authenticated)
        print(request.user.id)
        print(request.user.first_name)
        print(request.user.last_name)

        # Cus = Customer.objects.filter(id = request.user.id)
        customer = a.customer_set.order_by('id')[:]

        for cus in customer:
            X.append(cus.account)
            Y.append(cus.bank)

        # print(X)
        # print(Y)

        # name = bank[regn]

    else:
        print("User.is_not_authenticated")
        print(request.user.is_authenticated)
        X.append("0")
        Y.append(" ")

    if len(X) == 0:
        depositIsNull = True
    else:
        if X[-1] > 0:
            depositIsNull = False
        else:
            depositIsNull = True

    if depositIsNull == True:
        mes = 'Не достаточно средств на текущем счете - пополните депозит'
        acc = 0
        # return render(request, 'ai/deposit.html', mes=mes)
        return render(request, 'ai/deposit.html', {'Acc': acc, 'mes': mes})
    else:
        # mod = "model_X20_jpt22"
        # mod = "model_X51PCZ_37"
        mod = "model_X51PCZ_38F"  # 20210810 нормализованное распределение
        # if regn in bank:
        #    name = bank[regn]
        # else:
        #    name = 'Название не определено'
        # print(name)

        # Пересоздаем ту же самую модель, включая веса и оптимизатор.
        def mean_pred2(y_true, y_pred):
            a = abs(y_true - y_pred)
            #a = 1 - a
            return a

        get_custom_objects().update({"mean_pred": mean_pred2})
        print("mean_pred2...")

        model = keras.models.load_model(mod + '.h5', custom_objects={"mean_pred": mean_pred2})
        print("keras.models.load_model...")
        scaler_filename = "scaler_x69a.save"
        print(scaler_filename)
        scaler = joblib.load(scaler_filename)
        print("scaler = joblib.load...")
        txt = str(regn)
        print("txt =")
        print(txt)
        name = serv(request, txt)

        #wayf = "Testob-" + txt + "PCZ69A.csv"
        wayf = "D:/TEMP2/CSV/Testob-" + txt + "PCZ69A.csv"
        wayf_1 = "D:/TEMP2/CSV/Testob-" + txt + "PCZ69.csv"
        wayf_2 = "D:/TEMP2/CSV/Testob-" + txt + "A51.csv"
        wayf_3 = "D:/TEMP2/CSV/Testob-" + txt + "PCZ51.csv"

        check_file = os.path.exists(wayf)
        check_file_1 = os.path.exists(wayf_1)
        check_file_2 = os.path.exists(wayf_2)
        check_file_3 = os.path.exists(wayf_3)

        if check_file:
            data2 = pd.read_csv(wayf, sep=',')
            print("Используются данные >> " + wayf)
        elif check_file_1:
            data2 = pd.read_csv(wayf_1, sep=',')
            print("Используются данные >> " + wayf_1)
        elif check_file_2:
            data2 = pd.read_csv(wayf_2, sep=',')
            print("Используются данные >> " + wayf_2)
        elif check_file_3:
            data2 = pd.read_csv(wayf_3, sep=',')
            print("Используются данные >> " + wayf_3)
        else:
            print("Нет данных")
            name = "Нет данных"
        Dat = Dat2

        print(check_file)
        print(check_file_1)
        print(check_file_2)
        print(check_file_3)


        info = 'Ответ сети: расчет невозможен - отсутствует отчетность банка ' + name + ' (лицензия №' + regn + ')'
        if not (check_file or check_file_1 or check_file_2 or check_file_3):
            return render(request, 'ai/pdstart.html', {'Acc': X[-1], 'info': info})

        #data2 = pd.read_csv(wayf, sep=',')
        #print('data2[1][1]=')
        #print(data2['1'][1])

        ds2 = data2.shape[1]
        if ds2 == 56:
            cols = ['52', '53', '54', '55', '56']
        else:
            cols = []

        data2.drop(cols, axis=1, inplace=True)

        ds2 = data2.shape[0]
        if ds2 >= 41:
            X_new1 = data2[ds2 - 41:]
        else:
            X_new1 = data2
        # начальный элемент после отбрасывания старых данных, т.е. с какой строки (индекса) начинают X_new1
        nachelem = ds2 - 41

        print('nachelem = ')
        print(nachelem)

        #print('data2[:]=')
        #print(data2[:])

        #print('X_new1[:]=')
        #print(X_new1[:])

        #print('X_new1.shape[1] = ')
        #print(X_new1.shape[1])
        #print('X_new1.shape[0] = ')
        #print(X_new1.shape[0])


        if X_new1.shape[1] != 51:
            print('X_new1.shape[1] != 51')
            return render(request, 'ai/pdstart.html', {'Acc': X[-1], 'info': info})

        X_new1 = X_new1.apply(pd.to_numeric)
        X_new2 = X_new1.copy()
        #print("X_new1['35'][10] = ")
        #print(X_new1['35'][10])
        X_new = scaler.transform(X_new1)
        #print("X_new1['35'][10](after scale) = ")
        #print(X_new1['35'][10])

        # расчет предсказания
        predictions = model.predict(X_new)
        # определяем число строк в массиве X_new
        ChDat = X_new.shape[0]

        print("ChDat...")
        x = np.arange(0, ChDat, 1)
        print("x = ", x)

        # y1 = predictions
        tmp = predictions
        k = 0.000757014277148727
        vdd = (-np.log(tmp) / k) / 365

        print(" predictions...")
        # y1 - PD
        # y2 - PD(фильтр)
        # y3 - время до дефолта
        # y4 - время до дефолта(фильтр)
        # y5 - рейтинг(фильтр)
        # y6 - рейтинг прогноз
        # если время до дефолта ниже, чем время до дефолта (фильтр), то прогноз отрицательный
        # если время до дефолта выше, чем время до дефолта (фильтр), то прогноз положительный
        # если время до дефолта не сильно (не более 3 лет) отличается от время до дефолта (фильтр), то прогноз стабильный

        y1 = tmp.ravel()

        i = 0
        y3 = vdd.ravel()
        y2 = []
        y4 = []
        while i <= ChDat - 1:
            if i == 0:
                y2.append(y1[i])
                y4.append(y3[i])
            elif i == 1:
                y2.append((y1[i] + y1[i - 1]) / 2)
                y4.append((y3[i] + y3[i - 1]) / 2)
            elif i == 2:
                y2.append((y1[i] + y1[i - 1] + y1[i - 2]) / 3)
                y4.append((y3[i] + y3[i - 1] + y3[i - 2]) / 3)
            elif i == 3:
                y2.append((y1[i] + y1[i - 1] + y1[i - 2] + y1[i - 3]) / 4)
                y4.append((y3[i] + y3[i - 1] + y3[i - 2] + y3[i - 3]) / 4)
            else:
                y2.append((y1[i] + y1[i - 1] + y1[i - 2] + y1[i - 3] + y1[i - 4]) / 5)
                y4.append((y3[i] + y3[i - 1] + y3[i - 2] + y3[i - 3] + y3[i - 4]) / 5)
            # print(y2[i])
            i = i + 1

        i = 0
        y5 = []
        y6 = []
        while i <= ChDat - 1:
            if y4[i] >= 26:
                y5.append('AAA')
            elif y4[i] >= 25:
                y5.append('AAA-')
            elif y4[i] >= 24:
                y5.append('AA+')
            elif y4[i] >= 23:
                y5.append('AA')
            elif y4[i] >= 22:
                y5.append('AA-')
            elif y4[i] >= 21:
                y5.append('A+')
            elif y4[i] >= 20:
                y5.append('A')
            elif y4[i] >= 19:
                y5.append('A-')
            elif y4[i] >= 18:
                y5.append('BBB+')
            elif y4[i] >= 17:
                y5.append('BBB')
            elif y4[i] >= 16:
                y5.append('BBB-')
            elif y4[i] >= 15:
                y5.append('BB+')
            elif y4[i] >= 14:
                y5.append('BB')
            elif y4[i] >= 13:
                y5.append('BB-')
            elif y4[i] >= 12:
                y5.append('B+')
            elif y4[i] >= 11:
                y5.append('B')
            elif y4[i] >= 10:
                y5.append('B-')
            elif y4[i] >= 9:
                y5.append('CCC+')
            elif y4[i] >= 8:
                y5.append('CCC')
            elif y4[i] >= 7:
                y5.append('CCC-')
            elif y4[i] >= 6:
                y5.append('CC+')
            elif y4[i] >= 5:
                y5.append('CC')
            elif y4[i] >= 4:
                y5.append('CC-')
            elif y4[i] >= 3:
                y5.append('C+')
            elif y4[i] >= 2:
                y5.append('C')
            elif y4[i] >= 1:
                y5.append('C-')
            elif y4[i] >= 0:
                y5.append('D')
            else:
                y5.append('D')
            if y3[i] - y4[i] > 2:
                y6.append('положительный')
            if y3[i] - y4[i] < -2:
                y6.append('отрицательный')
            if abs(y3[i] - y4[i]) <= 2:
                y6.append('стабильный')
            i = i + 1

        # уточнить критерий успешно произведенного расчета if i > 0:
        if i > 0:
            XX = X[-1]
            XX = XX - 1
            X[-1] = XX
            m = Customer(phone='+7(495)7777777', bank=name, account=XX, user_id=request.user.id, datetime=now)
            m.save()

        # y3 = []
        # y3.append(x[::-1])
        # y3.append(y1[::-1])
        # y3.append(y2[::-1])
        # Формируем список с обратной последовательностью
        y22 = y2[::-1]

        # расчетные данные data2 из csv - файла
        # cols = ['3', '7', '8', '9', '13', '18', '19', '20', '21', '22', '23', '24', '25', '27', '29', '32', '33', '34',
        #        '38', '39', '40', '41', '42', '43', '44', '45', '46']
        # data2 = data2.apply(pd.to_numeric)
        # print('data2 =')
        # print(data2)
        # z1 = X_new1['1']
        # z2 = X_new1['2']
        # z4 = X_new1['4']
        # z5 = X_new1['5']
        # z6 = X_new1['6']
        # z10 = X_new1['10']
        # z11 = X_new1['11']
        # z12 = X_new1['12']
        # z14 = X_new1['14']
        # z15 = X_new1['15']
        # z16 = X_new1['16']
        # z17 = X_new1['17']

        # z26 = X_new1['26']
        # z28 = X_new1['28']
        # z30 = X_new1['30']
        # z31 = X_new1['31']
        #print('z31=')
        #print(z31)
        # z35 = X_new1['35']
        # z36 = X_new1['36']
        # z37 = X_new1['37']
        # z47 = X_new1['47']

        print('len(x) = ', len(x))
        tab = []
        tab2 = []
        otchetnost_full = []
        z1=[]
        z2 = []
        z3 = []
        z4 = []
        z5 = []
        z6 = []
        z10 = []
        z11 = []
        z12 = []
        z14 = []
        z15 = []
        z16 = []
        z17 = []
        z26 = []
        z28 = []
        z30 = []
        z31 = []
        z35 = []
        z36 = []
        z37 = []
        z47 = []



        for i in range(nachelem, len(x)+ nachelem):
            #print('i =', i )
            #print('Dat =', Dat[str(i)])

            y1[i-nachelem] = toFixed(y1[i-nachelem], 10)
            y2[i-nachelem] = toFixed(y2[i-nachelem], 10)
            y4[i-nachelem] = toFixed(y4[i-nachelem], 1)

            z1.append(float(toFixed(X_new2['1'][i], 5)))    # уровень просроченных процентов
            z2.append(float(toFixed(X_new2['2'][i], 5)))   # Общая срочная КА
            z4.append(float(toFixed(X_new2['3'][i], 5)))   # уровень риска активов
            z5.append(float(toFixed(X_new2['5'][i], 5)))    # уровень риска капитала
            z6.append(float(toFixed(X_new2['6'][i], 5)))    # время оборачиваемости кп
            z10.append(float(toFixed(X_new2['10'][i], 5)))    # ЛАМ / Активы
            z11.append(float(toFixed(X_new2['11'][i], 5)))   # Прибыль / Активы
            z12.append(float(toFixed(X_new2['12'][i], 5)))   # Прибыль / Капитал
            z14.append(float(toFixed(X_new2['14'][i], 5)))   # Коэфф. замещения
            z15.append(float(toFixed(X_new2['15'][i], 5)))   # E_int
            z16.append(float(toFixed(X_new2['16'][i], 5)))   # H12
            z17.append(float(toFixed(X_new2['17'][i], 5)))   # E_pr / E_int

            z26.append(float(toFixed(X_new2['26'][i], 5)) )  # Норматив H7
            z28.append(float(toFixed(X_new2['28'][i], 5)))   # Норматив H10_1
            z30.append(float(toFixed(X_new2['30'][i], 5)))   # Средства граждан / активы
            z31.append(float(toFixed(X_new2['31'][i], 5)))   # Доля активов в системе
            z35.append(float(toFixed(X_new2['35'][i], 5)))   # фактор V1
            z36.append(float(toFixed(X_new2['36'][i], 5)))   # фактор V2
            z37.append(float(toFixed(X_new2['37'][i], 5)))  # фактор V3
            z47.append(float(toFixed(X_new2['47'][i], 5)))   # доля МБК в активах

            if (z12[-1] == 0 and z5[-1] == 5) or (z2[-1] == 0 and z4[-1] == 0):
            # if (X_new1['12'][i] == 0 and X_new1['5'][i] == 5) or (X_new1['2'][i] == 0 and X_new1['4'][i] == 0):

                print('z12[-1] = ', z12[-1])
                print('z5[-1] = ', z5[-1])
                print('z2[-1] = ', z2[-1])
                print('z4[-1] = ', z4[-1])
                print('z35[-1] = ', z35[-1])
                otchetnost_full.append('false')
                print('otchetnost_full = false')
            else:
                otchetnost_full.append('true')
                print('z35[-1] = ', z35[-1])

            # x-номер квартала
            row = [x[i-nachelem], y1[i-nachelem], y2[i-nachelem], Dat[str(i)], y5[i-nachelem], y6[i-nachelem], y4[i-nachelem], otchetnost_full[i-nachelem]]
            tab.append(row)
            row = [
                x[i-nachelem], Dat[str(i)], z1[-1], z2[-1], z4[-1], z5[-1], z6[-1], z10[-1], z11[-1], z12[-1], z14[-1], z15[-1], z16[-1],
                z17[-1],
                z26[-1], z28[-1], z30[-1], z31[-1], z35[-1], z36[-1], z37[-1], z47[-1]
            ]
            tab2.append(row)

        pokaz = [
            '№ квартал',
            'Дата',
            'Уровень просроч. процентов',
            'Общая срочная кредитная активность',
            'Уровень риска активов',
            'Уровень риска капитала',
            'Время оборач. кред. портфеля',
            'ЛАМ/Активы',
            'Прибыль/Активы',
            'Прибыль/Капитал',
            'Коэфф. замещения',
            'Интегральная доходность, E_int ',
            'Норматив H12',
            'Относит. себест. E_pr/E_int',
            'Норматив H7',
            'Норматив H10_1',
            'Средства граждан / активы',
            'Доля активов в системе',
            'фактор V1',
            'фактор V2',
            'фактор V3',
            'доля МБК в активах',
        ]

        pokaz_shrot = [
            '№ квартал',
            'Дата',
            'Уровень просроч. проц.',
            'Общ. срочная кредит. активн.',
            'Уровень риска активов',
            'Уровень риска капитала',
            'Время оборач. кред. портфеля',
            'ЛАМ/Активы',
            'Прибыль/Активы',
            'Прибыль/Капитал',
            'Коэфф. замещения',
            'Интегр. доход-ть, E_int ',
            'Норматив H12',
            'Отн. себест. E_pr/E_int',
            'Норматив H7',
            'Норматив H10_1',
            'Ср-ва граждан / активы',
            'Доля активов в системе',
            'фактор V1',
            'фактор V2',
            'фактор V3',
            'доля МБК в активах',

        ]
        nachdat = Dat[str(nachelem)]
        plot = figure(
            title='Вероятность дефолта банка ' + name,
            plot_width=900,
            tools="pan, box_zoom, reset, save",
            x_axis_label='номер квартала начиная с '+ nachdat, y_axis_label='Вероятность дефолта'
        )
        plot.line(x, y1, legend_label="вероятность дефолта", line_color="red")
        plot.line(x, y2, legend_label="вероятность дефолта фильтр", line_color="blue")
        script, div = components(plot)
        # -----------------график 2-----------------------------------------------------------------------------

        script2, div2 = components(myplot(request, x, y1, z14, pokaz[10], name, nachdat))
        script3, div3 = components(myplot(request, x, y1, z15, pokaz[11], name, nachdat))

        script4, div4 = components(myplot(request, x, y1, z1, pokaz[2], name, nachdat))
        script5, div5 = components(myplot(request, x, y1, z2, pokaz[3], name, nachdat))
        script6, div6 = components(myplot(request, x, y1, z4, pokaz[4], name, nachdat))
        script7, div7 = components(myplot(request, x, y1, z5, pokaz[5], name, nachdat))
        script8, div8 = components(myplot(request, x, y1, z6, pokaz[6], name, nachdat))
        script9, div9 = components(myplot(request, x, y1, z10, pokaz[7], name, nachdat))
        script10, div10 = components(myplot(request, x, y1, z11, pokaz[8], name, nachdat))
        script11, div11 = components(myplot(request, x, y1, z12, pokaz[9], name, nachdat))
        script12, div12 = components(myplot(request, x, y1, z16, pokaz[12], name, nachdat))
        script13, div13 = components(myplot(request, x, y1, z17, pokaz[13], name, nachdat))
        script14, div14 = components(myplot(request, x, y1, z26, pokaz[14], name, nachdat))
        script15, div15 = components(myplot(request, x, y1, z28, pokaz[15], name, nachdat))
        script16, div16 = components(myplot(request, x, y1, z30, pokaz[16], name, nachdat))
        script17, div17 = components(myplot(request, x, y1, z31, pokaz[17], name, nachdat))
        script18, div18 = components(myplot(request, x, y1, z35, pokaz[18], name, nachdat))
        script19, div19 = components(myplot(request, x, y1, z36, pokaz[19], name, nachdat))
        script20, div20 = components(myplot(request, x, y1, z37, pokaz[20], name, nachdat))
        script21, div21 = components(myplot(request, x, y1, z47, pokaz[21], name, nachdat))

        return render(request, 'ai/pdcalc.html', {'b_regn': regn, 'b_name': name, 'x': x,
                                                  'y1': y1, 'y2': y2, 'y3': y3, 'y22': y22, 'Acc': X[-1], 'tab': tab,
                                                  'dat': Dat,
                                                  'tab2': tab2, 'pokaz': pokaz, 'pokaz_shrot': pokaz_shrot,
                                                  'script': script, 'div': div,
                                                  'script2': script2, 'div2': div2,
                                                  'script3': script3, 'div3': div3,
                                                  'script4': script4, 'div4': div4,
                                                  'script5': script5, 'div5': div5,
                                                  'script6': script6, 'div6': div6,
                                                  'script7': script7, 'div7': div7,
                                                  'script8': script8, 'div8': div8,
                                                  'script9': script9, 'div9': div9,
                                                  'script10': script10, 'div10': div10,
                                                  'script11': script11, 'div11': div11,
                                                  'script12': script12, 'div12': div12,
                                                  'script13': script13, 'div13': div13,
                                                  'script14': script14, 'div14': div14,
                                                  'script15': script15, 'div15': div15,
                                                  'script16': script16, 'div16': div16,
                                                  'script17': script17, 'div17': div17,
                                                  'script18': script18, 'div18': div18,
                                                  'script19': script19, 'div19': div19,
                                                  'script20': script20, 'div20': div20,
                                                  'script21': script21, 'div21': div21,

                                                  })


def myplot(request, x, y1, y2, name_y2, b_name, nachdat):
    # print('y2 = ',y2)
    # y2 = y2.ravel()
    plot = figure(
        title='Вероятность дефолта банка и ' + name_y2 + ' банка ' + b_name,
        plot_width=1100,
        tools="pan, box_zoom, reset, save",
        x_axis_label='номер квартала начиная с '+ nachdat, y_axis_label='Вероятность дефолта'
    )
    plot.y_range = Range1d(start=0 - max(y1) * 0.1, end=max(y1) * 1.1)

    if min(y2) < 0:
        plot.extra_y_ranges['temp'] = Range1d(start=min(y2) + min(y2) * 0.1, end=max(y2) - 0.1 * min(y2))
    elif min(y2) == max(y2) == 0:
        plot.extra_y_ranges['temp'] = Range1d(start=-0.1, end=0.1)
    else:
        plot.extra_y_ranges['temp'] = Range1d(start=(min(y2) - max(y2) * 0.1), end=(max(y2) * 1.1))

    plot.add_layout(LinearAxis(y_range_name='temp', axis_label=name_y2), 'right')

    plot.line(x, y1, legend_label="вероятность дефолта", line_color="red")
    plot.line(x, y2, legend_label=name_y2, line_color="blue", y_range_name='temp')
    # script2, div2 = components(plot)
    return plot


def myplot_2(request, x, y1, y2, y4, name_y1, name_y2, name_y4):
    plot = figure(
        title='Данные телеметрии: ' + name_y1 + ', ' + name_y2 + ', ' + name_y4,
        plot_width=900,
        tools="pan, box_zoom, reset, save",
        x_axis_label='номер измерения в выборке',
        y_axis_label='температура, С° | влажность, %'
    )

    # print('y2 = ')
    # print(y2)
    y1_min = min(y1)
    y2_min = min(y2)
    y1_max = max(y1)
    y2_max = max(y2)
    if y1_min < y2_min:
        y_min = y1_min
    else:
        y_min = y2_min

    if y1_max > y2_max:
        y_max = y1_max
    else:
        y_max = y2_max

    if min(y1) < 0:
        plot.y_range = Range1d(start=y_min + y_min * 0.1, end=y_max - 0.1 * y_min)
    elif y_min == y_max == 0:
        plot.y_range = Range1d(start=-0.1, end=0.1)
    else:
        plot.y_range = Range1d(start=(y_min - y_max * 0.1), end=(y_max * 1.1))

    plot.extra_y_ranges['CO2'] = Range1d(start=min(y4) * 0.9, end=max(y4) * 1.1)

    plot.add_layout(LinearAxis(y_range_name='CO2', axis_label=name_y4), 'right')

    plot.line(x, y1, legend_label=name_y1, line_color="red")
    plot.line(x, y2, legend_label=name_y2, line_color="blue")
    plot.line(x, y4, legend_label=name_y4, line_color="green", y_range_name='CO2')
    # script2, div2 = components(plot)
    return plot


# удаление из БД
#  Metering.objects.filter(meter_datetime__day=21).delete()

class MyprojectLoginView(LoginView):
    template_name = 'ai/login.html'
    formclass = AuthUserForm
    success_url = reverse_lazy('ai:start')

    def get_success_url(self):
        return self.success_url


class RegisterUserView(CreateView):
    model = User
    template_name = 'ai/register_page.html'
    form_class = RegisterUserForm
    # success_url = reverse_lazy('ai:recstart_page')
    # success_url = reverse_lazy('ai:nabobj')
    success_url = reverse_lazy('ai:codegen_emailsend_page')
    success_msg = "Пользователь успешно зарегистрирован"

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class MyprojectLogout(LogoutView):
    next_page = reverse_lazy('ai:start')


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def upDateAcc(request):
    print("upDateAcc")
    acc = account_check(request)
    howmatch = int(acc) + int(request.POST['name'])
    now = timezone.now()
    m = Customer(phone='+7(495)7777777', bank="пополнение баланса", account=howmatch, user_id=request.user.id,
                 datetime=now)
    m.save()
    acc = account_check(request)
    return render(request, 'ai/pdstart.html', {'Acc': acc})


def rascheti(request):
    import os
    import sqlite3
    import urllib  # URL functions
    from time import strftime

    bd = 'D:\WORK\Python\django-learn\mydjango\db.sqlite3'
    now = timezone.now()
    f = open('D:/TEMP3/tudent.txt', 'a')
    f.write('Отчет о действиях клиента ' + request.user.first_name + ' ' + request.user.last_name + '\n')
    f.write('Дата и время формирования отчета: ' + str(now) + '\n')

    tdate = strftime("%d-%m")

    conn = sqlite3.connect(bd)
    cursor = conn.cursor()
    loc_stmt = 'SELECT account, bank, datetime, user_id from ai_customer WHERE user_id =' + str(request.user.id)
    cursor.execute(loc_stmt)
    while True:
        row = cursor.fetchone()
        if row == None:
            break
        account = row[0]
        bank = row[1]
        datetime = row[2]
        user_id = row[3]
        f.write('user_id =' + str(user_id) + ' счет: ' + str(account) + ' действие: ' + bank + ' on ' + datetime + '\n')

    # return render(request, 'ai/start.html', {'Acc': X[-1]})
    return render(request, 'ai/start.html')


def rascheti2(request):
    print("rascheti2")

    now = timezone.now()

    f = open('D:/TEMP3/tudent.txt', 'a')
    f.write('Отчет о действиях клиента ' + request.user.first_name + ' ' + request.user.last_name + '\n')
    f.write('Дата и время формирования отчета: ' + str(now) + '\n')

    X = []
    X.append("0")
    bank = []
    datetime = []
    user_id = []

    if request.user.is_authenticated == True:
        try:
            a = User.objects.get(id=request.user.id)
        except:
            raise Http404("Пользователь отсутствует")
        print("User.is_authenticated = ", request.user.is_authenticated)
        print(request.user.id)
        print(request.user.first_name)
        print(request.user.last_name)

        customer = a.customer_set.order_by('id')[:]
        tab = []
        for cus in customer:
            X.append(cus.account)
            bank.append(cus.bank)
            datetime.append(cus.datetime)
            user_id.append(cus.user_id)
            row = [cus.user_id, cus.bank, cus.account, cus.datetime]
            tab.append(row)
            f.write(
                'user_id =' + str(cus.user_id) + ' счет: ' + str(cus.account) + ' действие: ' + cus.bank + ' on ' + str(
                    cus.datetime) + '\n')
    f.close()
    if len(X) == 0:
        X.append("0")
    return render(request, 'ai/rascheti.html',
                  {'Acc': X[-1], 'bank': bank, 'datetime': datetime, 'user_id': user_id, 'tab': tab,
                   'len_X': len(X), 'now': now, 'first_name': request.user.first_name,
                   'last_name': request.user.last_name})


def sendSMS(request):
    print('sendSMS begin')
    import urllib  # URL functions
    from time import strftime
    import urllib.request  # URL functions
    from urllib.parse import urlencode

    f = open('D:/TEMP3/sms.txt', 'a')
    tdate = strftime("%d-%m")

    sname = 'Igor'
    snumber = '+79037835429'
    message = (
            sname + ' There will be NO training tonight on the ' + tdate + ' Sorry for the late notice, I have sent a mail as well, just trying to reach everyone, please do not reply to this message as this is automated')

    username = 'YOUR_USERNAME'
    sender = 'WHO_IS_SENDING_THE_MAIL'
    hash = 'YOUR HASH YOU GET FROM YOUR ACCOUNT'

    numbers = (snumber)
    print('numbers = ' + numbers)
    # Set flag to 1 to simulate sending, this saves your credits while you are testing your code. # To send real message set this flag to 0
    test_flag = 1

    # -----------------------------------
    # No need to edit anything below this line
    # -----------------------------------

    values = {'test': test_flag,
              'uname': username,
              'hash': hash,
              'message': message,
              'from': sender,
              'selectednums': numbers}

    url = 'http://www.txtlocal.com/sendsmspost.php'
    print('values = ')
    print(values)
    postdata = urlencode(values)
    print("postdata = ")
    print(postdata)
    # req = urllib.request.Request(url, postdata)
    # req = urllib.request.Request(url, postdata)
    req = url + postdata
    print('req = ')
    print(req)
    print('Attempting to send SMS to ' + sname + ' at ' + snumber + ' on ' + tdate)
    f.write('Attempting to send SMS to ' + sname + ' at ' + snumber + ' on ' + tdate + '\n')

    try:
        response = urllib.request.urlopen(req)
        response_url = response.geturl()
        if response_url == url:
            print('SMS sent!')
            sms_sux = 'SMS sent!'
            return render(request, 'ai/sms.html', {'response_url': response_url, "sms_sux": sms_sux})
    except urllib.request.URLError as e:
        print('Send failed!')
        print(e.reason)
        e_reason = e.reason
        sms_sux = 'Send failed!'

        return render(request, 'ai/sms.html', {'e_reason': e_reason, "sms_sux": sms_sux})


def offerta(request):
    return render(request, 'ai/offerta.html')


def fillrec(request):
    import string
    msg = ''
    un = user_name(request)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), un + '_tuden.txt')
    f = open(path, 'r')
    codeword_2 = f.read()
    f.close()

    # codeword_2 = 'c3be4580-0774-407d-b3fe-4f3ffd97c7b8'
    client_name = request.POST.get('client_name')
    client_name_full = request.POST.get('client_name_full')
    adres = request.POST.get('adres')

    inn = request.POST.get('inn')
    kpp = request.POST.get('kpp')
    ogrn = request.POST.get('ogrn')
    country = request.POST.get('country')
    # identificator = request.POST.get('identificator')
    identificator = identific(request)
    mac = request.POST.get('mac')
    codeword = request.POST.get('codeword')
    ul_fl = request.POST.get('ul_fl')
    print('ul_fl =')
    print(ul_fl)
    print('codeword_2 =')
    print(codeword_2)
    print('codeword =')
    print(codeword)

    codeword = codeword.strip()
    codeword_2 = codeword_2.strip()

    now = timezone.now()
    # if len(inn) == 0:
    # inn = 'ИНН'

    if ul_fl == 'true':
        vid = 1
    else:
        vid = 0

    X = []
    Y = []
    Z = []
    maci = []
    try:
        #a = device.objects.filter(identificator=identificator)
        a = device.objects.all()
        customer = a.order_by('id')[:]
        print('customer = ')
        print(customer)
        i = 0
        j = 0
        for cus in customer:
            X.append(cus.identificator)
            Y.append(cus.user_id)
            Z.append(cus.user.username)
            maci.append(cus.mac)
            i = i + 1

        # print('ID пользователя с таким же номером комплекта')
        # print(Y)
        # print('имена пользователей с таким же номером комплекта')
        # print(Z)

        for mac2 in maci:
            if mac == mac2:
                j = j + 1
        print('Число комплектов аппаратуры c таким же номером = ')
        print(j)

    except:
        i = 0
        # raise Http404("Комлект с таким номером отсутствует")

    mist_fild = []

    if j > 0:
        msg += ' Комлект аппаратуры с таким номером уже зарегистрирован. Регистрация невозможна /'
        mist_fild.append('true')
        return render(request, 'ai/message.html', {'msg': msg})

    if ul_fl == 'true':

        if len(client_name) == 0:
            mist_fild.append('true')
            msg += ' введите название организации /'
        else:
            mist_fild.append('false')

        if len(client_name_full) == 0:
            mist_fild.append('true')
            msg += ' введите полное название организации /'
        else:
            mist_fild.append('false')

        if len(adres) == 0:
            mist_fild.append('true')
            msg += ' введите адрес регистрации /'
        else:
            mist_fild.append('false')

        if len(inn) != 10 and len(inn) != 12:
            msg += ' введите ИНН организации /'
            mist_fild.append('true')
        else:
            mist_fild.append('false')

        if len(kpp) != 9:
            msg += ' введите КПП /'
            mist_fild.append('true')
        else:
            mist_fild.append('false')

        if len(ogrn) != 13 and len(ogrn) != 15:
            msg += ' введите ОГРН/ОГРНИП /'
            mist_fild.append('true')
        else:
            mist_fild.append('false')

        if len(country) == 0:
            mist_fild.append('true')
            msg += ' введите адрес регистрации /'
        else:
            mist_fild.append('false')

        if codeword != codeword_2:
            msg += ' введите кодовое слово'
            mist_fild.append('true')
        else:
            mist_fild.append('false')

        reg_fault = 'false'
        for i in mist_fild:
            if i == 'true':
                reg_fault = 'true'

        if reg_fault == 'true':
            msg_1 = 'Регистрация не завершена: '
            msg = msg_1 + msg
            return render(request, 'ai/recvizits.html', {'msg': msg, 'inn_2': inn, 'adres_2': adres,
                                                         'client_name_2': client_name,
                                                         'client_name_full_2': client_name_full,
                                                         'country_2': country, 'kpp_2': kpp,
                                                         'ogrn_2': ogrn, 'comment_2': codeword, 'vid_2': vid,
                                                         'mac_2': mac})
        else:
            msg_1 = 'Проверка введенных данных выполнена. '
            msg = msg_1 + msg


    else:
        if codeword != codeword_2:
            msg = 'Регистрация не завершена '
            msg += 'введите кодовое слово'
            return render(request, 'ai/recvizits.html', {'msg': msg, 'inn_2': inn, 'adres_2': adres,
                                                         'client_name_2': client_name,
                                                         'client_name_full_2': client_name_full,
                                                         'country_2': country, 'kpp_2': kpp,
                                                         'ogrn_2': ogrn, 'comment_2': codeword, 'vid_2': vid,
                                                         'mac_2': mac})

    m = Customerrec(client_name=client_name, adres=adres, inn=inn, user_id=request.user.id,
                    client_name_full=client_name_full, country=country, kpp=kpp, ogrn=ogrn,
                    comment=codeword, vid=vid, datetime=now, identificator=identificator, mac=mac)
    m.save()

    devname = 'Device_1'
    comment = ' '
    m2 = device(comment=comment, devname=devname, datetime=now, identificator=identificator, mac=mac,user_id=request.user.id)
    m2.save()

    msg += 'Реквизиты занесены в базу данных.'

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), un + '_tuden.txt')
    os.remove(path)

    return render(request, 'ai/message.html', {'msg': msg})


def recstart(request):
    return render(request, 'ai/recvizits.html')


def recstart2(request):
    return render(request, 'ai/recvizits2.html')


def deposit(request):
    print("deposit")
    acc = account_check(request)
    mes = ''
    return render(request, 'ai/deposit.html', {'Acc': acc, 'mes': mes})


def serv(request, zapros):
    import pandas as pd

    print('zapros =')
    print(zapros)
    data = pd.read_csv("Banks2.csv", sep=';')
    regn = data['Regn']
    regnstr = []
    for r in regn:
        regnstr.append(str(r))
    bname = data['Name']
    banks = dict(zip(regnstr, bname))
    # print('banks = ')
    # print(banks)
    if zapros in banks:
        otvet = banks[zapros]
    else:
        otvet = 'NoName'

    msg = 'данные из файла csv получены'

    # return render(request, 'ai/message.html', {'msg': msg, 'regn':regn,'bname':bname,'banks':banks})
    return otvet


def mail(request):
    return render(request, 'ai/mail.html')


def success_old(request):
    email = request.POST.get('name', '')
    print('email=')
    print(email)
    data = """
    Hello there!

    I wanted to personally write an email in order to welcome you to our platform.\
    We have worked day and night to ensure that you get the best service. I hope \
    that you will continue to use our service. We send out a newsletter once a \
    week. Make sure that you read it. It is usually very informative.
    
    Cheers!
    ~ Yasoob
    """
    print('data =')
    print(data)

    send_mail('Welcome!', data, "Yasoob",
              [email], fail_silently=False)
    msg = 'Сообщение отправлено по e-mail'

    return render(request, 'ai/success.html', {'msg': msg})


def success(request):

    email = request.POST.get('name', '')
    print('email=')
    print(email)

    message = Mail(
        from_email = 'info@amelin-gba.com',
        to_emails = email,
        subject = 'Sending with Twilio SendGrid is Fun',
        html_content = '<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        print('os.environ.get(SENDGRID_API_KEY) = ')
        print(os.environ.get('SENDGRID_API_KEY'))

        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        msg = 'Сообщение отправлено по e-mail'
    except Exception as e:

        print(e.message)
        msg = e.message

    return render(request, 'ai/success.html', {'msg': msg})


def send_codeword_old(request, codeword):
    email = user_email(request)
    print('email=')
    print(email)
    data = """
        Добрый день!
        
        Вы находитесь в процессе регистрации на сайте amelin-aga.com. Для завершения регистрации Вам понадобится следующее кодовое слово 
        """
    data += codeword

    data2 = """
        
        С уважением,
        Аналитическая группа Амелина 
                """
    data += data2

    print('data =')
    print(data)

    if email != 'no email':
        send_mail('Welcome!', data, "Yasoob",
                  [email], fail_silently=False)
    return email


def send_codeword(request, codeword):
    print('send_codeword...')
    email = user_email(request)
    print('email=')
    print(email)
    data = """
        Добрый день!

        Вы находитесь в процессе регистрации на сайте https://agame.pythonanywhere.com. Для завершения регистрации Вам понадобится следующее кодовое слово 
        """
    data += codeword

    data2 = """

        С уважением,
        Аналитическая группа Амелина 
                """
    data += data2

    print('data =')
    print(data)

    if email != 'no email':
        message = Mail(
            from_email='info@amelin-gba.com',
            to_emails=email,
            subject='Регистрация',
            html_content = data)
        try:
            # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY2'))
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cw.txt')
            f = open(path, 'r')
            cw = f.read()
            f.close()
            SENDGRID_API_KEY2 = cw
            print(cw)
            sg = SendGridAPIClient(SENDGRID_API_KEY2)
            print('os.environ.get(my_pc_2) = ')
            print(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            msg = 'Сообщение отправлено по e-mail'
        except Exception as e:

            print(e)
            msg = e
    return email


def user_email(request):
    # по user.id получаем email из связанной с моделью Uesr БД Customerrec
    X = []
    try:
        a = User.objects.get(id=request.user.id)
    except:
        raise Http404("Пользователь отсутствует")
    print("User.is_authenticated = ", request.user.is_authenticated)
    print(request.user.id)
    print(request.user.first_name)
    print(request.user.last_name)
    print(request.user.id)
    # customer = a.customer_set.order_by('id')[:]

    # for cus in customer:
    X.append(a.email)

    print('a.email = ')
    print(a.email)

    if len(a.email) == 0:
        resp = 'no email'
    else:
        resp = a.email

    return resp


def codegen_emailsend(request):
    # codeword_2 = str(secrets.token_bytes(16))
    codeword_2 = str(uuid.uuid4())
    email = send_codeword(request, codeword_2)
    un = user_name(request)
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), un + '_tuden.txt')
    # f = open(path, 'a')
    f = open(path, 'w')
    f.write(codeword_2)
    f.close()

    if email == 'no email':
        msg = ' отсутствует email - нет возможности отправить Вам кодовое слово /'
    else:
        msg = ' Произведена отправка Вам кодового слова, необходимого для регистрации в системе /'

    return render(request, 'ai/recvizits.html')


def user_name(request):
    # по user.id получаем итя клиента (login) из модели Uesr
    try:
        a = User.objects.get(id=request.user.id)
    except:
        raise Http404("Пользователь отсутствует")

    print('a.username = ')
    print(a.username)

    if len(a.username) == 0:
        resp = 'no Name'
    else:
        resp = a.username

    return resp


# -------------CHANGE PASSWORD--------------------------
class MyPasswordChangeView(PasswordChangeView):
    template_name = 'ai/password_change_form.html'
    # formclass = AuthUserForm
    success_url = reverse_lazy('ai:password_change_done')

    def get_success_url(self):
        return self.success_url


class MyPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'ai/password_change_done.html'
    # formclass = AuthUserForm
    success_url = reverse_lazy('ai:start')

    def get_success_url(self):
        return self.success_url


# -------------RESET PASSWORD--------------------------
class MyPasswordResetView(PasswordResetView):
    template_name = 'ai/password_reset_form.html'
    email_template_name = 'ai/password_reset_email.html'
    # formclass = AuthUserForm
    success_url = reverse_lazy('ai:password_reset_done')

    def get_success_url(self):
        return self.success_url


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'ai/password_reset_done.html'

    # formclass = AuthUserForm
    success_url = reverse_lazy('ai:start')

    def get_success_url(self):
        return self.success_url


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'ai/password_reset_confirm.html'
    # formclass = AuthUserForm
    success_url = reverse_lazy('ai:password_reset_complete')

    def get_success_url(self):
        return self.success_url


class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'ai/password_reset_complete.html'
    # formclass = AuthUserForm
    success_url = reverse_lazy('ai:start')

    def get_success_url(self):
        return self.success_url


def remotecontrol(request):
    X = []
    try:
        a = User.objects.get(id=request.user.id)
    except:
        raise Http404("Пользователь отсутствует")
    print("User.is_authenticated = ", request.user.is_authenticated)
    print(request.user.id)
    print(request.user.first_name)
    print(request.user.last_name)
    print(request.user.id)

    X.append(a.email)

    print('a.email = ')
    print(a.email)

    if len(a.email) == 0:
        resp = 'no email'
    else:
        resp = a.email

    print("hello!")

    return resp


def control(request):
    print("control")
    voc = get_ident(request)
    print('voc = ')
    print(voc)
    ident = voc['ident']
    RegFF = voc['RFF']
    if RegFF == False:
        codegen_emailsend(request)
        return render(request, 'ai/recvizits.html')

    now = timezone.now()

    dev_1 = []
    dev_2 = []
    dev_3 = []

    if request.user.is_authenticated == True:
        try:
            a = User.objects.get(id=request.user.id)
        except:
            raise Http404("Управляющие воздействия отсутствуют")

    print("User.is_authenticated = ", request.user.is_authenticated)
    print(request.user.id)
    print(request.user.first_name)
    print(request.user.last_name)

    control = a.my_control_set.order_by('id')[:]

    for c in control:
        dev_1.append(c.dev_1)
        dev_2.append(c.dev_2)
        dev_3.append(c.dev_3)

    if len(dev_1) == 0:
        dev_1.append("False")
        dev_2.append("False")
        dev_3.append("False")

    print('dev_1[-1] = ')
    print(dev_1[-1])

    if dev_1 == False or dev_1 == None:
        d1 = 'false'
    else:
        d1 = 'true'
    if dev_2 == False or dev_2 == None:
        d2 = 'false'
    else:
        d2 = 'true'
    if dev_3 == False or dev_3 == None:
        d3 = 'false'
    else:
        d3 = 'true'

    print("d1 =")
    print(d1)

    return render(request, 'ai/control.html',
                  {'dev_1': dev_1[-1], 'dev_2': dev_2[-1], 'dev_3': dev_3[-1], 'user_id': request.user.id,
                   'first_name': request.user.first_name, 'last_name': request.user.last_name})


def control_save(request):
    print("control_save")
    voc = get_ident(request)
    ident = voc['ident']
    RegFF = voc['RFF']
    if RegFF == False:
        codegen_emailsend(request)
        return render(request, 'ai/recvizits.html')

    dev_1 = request.POST.get('device_1')
    print("dev_1 =")
    print(dev_1)

    dev_2 = request.POST.get('device_2')
    print("dev_2 =")
    print(dev_2)
    dev_3 = request.POST.get('device_3')
    print("dev_3 =")
    print(dev_3)
    # comment = request.POST.get('text')
    comment = request.POST['text']
    print('comment = ')
    print(comment)

    print('user_id = ')
    print(request.user.id)

    if dev_1 == 'false' or dev_1 == None:
        d1 = False
    else:
        d1 = True
    if dev_2 == 'false' or dev_2 == None:
        d2 = False
    else:
        d2 = True
    if dev_3 == 'false' or dev_3 == None:
        d3 = False
    else:
        d3 = True

    print("d1 =")
    print(d1)

    now = timezone.now()
    m = my_control(user_id=request.user.id, dev_1=d1, dev_2=d2, dev_3=d3, comment=comment, phone='+7 (495) 777-77-77',
                   datetime=now, identificator=ident)
    m.save()
    acc = account_check(request)
    return render(request, 'ai/start.html', {'Acc': acc})


def my_condition(request):
    print("my_condition")
    login = request.GET.get('login')
    print("login = ")
    print(login)

    dev_1 = []
    dev_2 = []
    dev_3 = []

    try:
        print("control = ")
        a = my_control.objects.filter(identificator=login)
        # print(a)
    except:
        raise Http404("отсутствуют данные об управляющем состоянии для комплекта оборудования " + login)

    control = a.order_by('id')

    for c in control:
        dev_1.append(c.dev_1)
        dev_2.append(c.dev_2)
        dev_3.append(c.dev_3)

    # print ('dev_1[-1] = ')
    # print(dev_1[-1])
    # print('dev_2[-1] = ')
    # print(dev_2[-1])
    # print('dev_3[-1] = ')
    # print(dev_3[-1])

    if dev_1 == False or dev_1 == None:
        d1 = 'false'
    else:
        d1 = 'true'
    if dev_2 == False or dev_2 == None:
        d2 = 'false'
    else:
        d2 = 'true'
    if dev_3 == False or dev_3 == None:
        d3 = 'false'
    else:
        d3 = 'true'

    print("d1 =")
    print(d1)
    vocab = {'dev_1': dev_1[-1], 'dev_2': dev_2[-1], 'dev_3': dev_3[-1], 'identificator': login}
    print(vocab)
    # return ({'dev_1': dev_1[-1], 'dev_2': dev_2[-1], 'dev_3': dev_3[-1], 'identificator': login})
    # return render(request, 'ai/start.html', {'dev_1': dev_1[-1], 'dev_2': dev_2[-1], 'dev_3': dev_3[-1], 'identificator': login})
    return JsonResponse({"key": "value"})


def my_condition_2(request):
    # возникает ошибка, если управляющий вектор не задан. Например при первом использовании нового комплекта аппаратуры
    # нужно это предусмотреть
    print("my_condition_2")
    login = request.GET.get('login')
    print("login = ")
    print(login)

    dev_1 = []
    dev_2 = []
    dev_3 = []

    try:
        print("control = ")
        a = my_control.objects.filter(identificator=str(login))
        print('a=')
        print(a)
        control = a.order_by('id')
        print('a=')
        print(a)

        for c in control:
            dev_1.append(c.dev_1)
            dev_2.append(c.dev_2)
            dev_3.append(c.dev_3)

        print ('dev_1[-1] = ')
        print(dev_1[-1])
        print('dev_2[-1] = ')
        print(dev_2[-1])
        print('dev_3[-1] = ')
        print(dev_3[-1])

        if dev_1[-1] == False or dev_1[-1] == None:
            d1 = 'fals'
        else:
            d1 = 'true'
        if dev_2[-1] == False or dev_2[-1] == None:
            d2 = 'fals'
        else:
            d2 = 'true'
        if dev_3[-1] == False or dev_3[-1] == None:
            d3 = 'fals'
        else:
            d3 = 'true'

        vocab = {'dev_1': d1, 'dev_2': d2, 'dev_3': d3, 'identificator': login}
        print("my_condition_2.vocab = ")
        print(vocab)
        return (vocab)
    except:
        # raise Http404("отсутствуют данные об управляющем состоянии для комплекта оборудования " + login)
        vocab = {'dev_1': 'fals', 'dev_2': 'fals', 'dev_3': 'fals', 'identificator': login}
        print('my_condition_2.except:')
        print(vocab)
        return (vocab)




class my_controlView(APIView):
    def get(self, request):
        print("class my_controlView")
        login = request.GET.get('login')
        print("login = ")
        print(login)
        # my_co = my_control.objects.all()

        try:
            #print("control = ")
            a = my_control.objects.filter(identificator=login)
            #print("a = ")
            #print(a)
            my_co = a.order_by('id')
            #print("my_co = ")
            #print(my_co)
        except:
            # raise Http404("отсутствуют данные об управляющем состоянии для комплекта оборудования " + login)
            return Response({"my_control": "No data"})

        if len(my_co) != 0:
            serializer = my_controlSerializer(my_co, many=True)
            print("my_control = ")
            print(serializer.data[-1])
            return Response({"my_control": serializer.data[-1]})
        else:
            return Response({"my_control": "No data"})


def my_layout(x, y, x_axis, y_axis, title_name):
    TOOLS = "pan,wheel_zoom,box_select,lasso_select,reset"
    p = figure(tools=TOOLS, width=900, height=600, min_border=10, min_border_left=50,
               toolbar_location="above",
               x_axis_label=x_axis, y_axis_label=y_axis,
               title=title_name)
    p.background_fill_color = "#fafafa"
    r = p.scatter(x, y, size=3, color="#3A5785", alpha=0.6)

    # create the horizontal histogram
    hhist, hedges = np.histogram(x, bins=20)
    hzeros = np.zeros(len(hedges) - 1)
    hmax = max(hhist) * 1.1
    LINE_ARGS = dict(color="#3A5785", line_color=None)
    ph = figure(toolbar_location=None, width=p.width, height=250, x_range=p.x_range,
                y_range=(-hmax, hmax), min_border=10, min_border_left=50, y_axis_location="right")
    ph.xgrid.grid_line_color = None
    ph.yaxis.major_label_orientation = np.pi / 4
    ph.background_fill_color = "#fafafa"

    ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="white", line_color="#3A5785")
    hh1 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.5, **LINE_ARGS)
    hh2 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.1, **LINE_ARGS)

    # create the vertical histogram
    vhist, vedges = np.histogram(y, bins=20)
    vzeros = np.zeros(len(vedges) - 1)
    vmax = max(vhist) * 1.1

    pv = figure(toolbar_location=None, width=250, height=p.height, x_range=(-vmax, vmax),
                y_range=p.y_range, min_border=10, y_axis_location="right")
    pv.ygrid.grid_line_color = None
    pv.xaxis.major_label_orientation = np.pi / 4
    pv.background_fill_color = "#fafafa"

    pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vhist, color="white", line_color="#3A5785")
    vh1 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.5, **LINE_ARGS)
    vh2 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.1, **LINE_ARGS)

    layout = gridplot([[p, pv], [ph, None]], merge_tools=False)
    return layout


def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'colod_threshold' not in kwargs:
        kwargs['colod_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        # fig = plt.figure(figsize=(10, 8)) # после того как убрал это оператор стало выводиться дерево (дендрограмма), до этого выводилась только рамка
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        plt.title('Дендрограмма')
        plt.xlabel('sample index or (clastr size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
            plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                         textcoords='offset points',
                         va='top', ha='center')

        if max_d:
            plt.axhline(y=max_d, c='k')

    # plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()  # после включения этого оператора ушла ошибка

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return graphic


def test_js(request):
    return render(request, 'ai/test_js.html')

def test_js2(request):
    return render(request, 'ai/test_js2.html')

#def test_js3(request):
    #    meter_title = 'Francheska'
    #chisizm = 1000
    #return render(request, 'ai/test_js3.html', {'meter_title': meter_title, 'chisizm': chisizm})

def test_js3(request, meter_title, chisizm):

    return render(request, 'ai/test_js3.html', {'meter_title': meter_title, 'chisizm': chisizm})

class my_dataView(APIView):
    def get(self, request):
        print("class my_dataView")
        login = request.GET.get('login')
        meter_title = request.GET.get('meter_title')
        chisizm = int(request.GET.get('chisizm'))
        # p = request.GET.get('param')
        p = 5
        print("login=")
        print(login)
        print("meter_title=")
        print(meter_title)
        print("chisizm=")
        print(chisizm)
        voc = get_ident(request)
        print('voc = ')
        print(voc)
        ident = voc['ident']
        print('ident = ')
        print(ident)

        RegFF = voc['RFF']
        if RegFF == False and request.user.is_authenticated:
            codegen_emailsend(request)
            return render(request, 'ai/recvizits.html')



        try:
            print('try')
            q = Metering.objects.filter(meter_title=meter_title, meter_identificator=str(ident))
            print('q =')

        except:
            print('except:')
            # raise Http404("отсутствуют данные об управляющем состоянии для комплекта оборудования " + login)
            return Response({"my_data_try": "No data"})


        print('до my_data')
        my_data = q.order_by('-meter_datetime')[:chisizm]
        print('после my_data')

        x0 = []
        y1 = []
        y2 = []
        y4 = []
        # d = []
        number = []
        i = 1
        # format = '%b %d %Y %I:%M%p' # Формат
        format = '%H:%M'  # Формат

        for data in my_data:
            x0.append(data.meter_datetime)
            y1.append(data.meter_temperature)
            y2.append(data.meter_humidity)
            y4.append(data.meter_CO2)
            number.append(i)
            i = i + 1

        name_cow = data.meter_title
        print(name_cow)

        # result =np.column_stack((latest_data_list, number))

        if name_cow == 'Yarushka':
            nabobj_name = 'Объект 1'
            gas_name = 'LPG'
        elif name_cow == 'Mumuka':
            nabobj_name = 'Объект 2'
            gas_name = 'CO2'
        elif name_cow == 'Francheska':
            nabobj_name = 'Объект 3'
            gas_name = 'LPG'
        elif name_cow == 'Buryonka':
            nabobj_name = 'Объект 4'
            gas_name = 'Smoke gas'
        elif name_cow == 'Vestka':
            nabobj_name = 'Объект 5'
            gas_name = 'CH4'
        else:
            nabobj_name = 'Объект NoName'
            #gas_name = 'UnKnown gas'
            gas_name = 'gas'

        print(nabobj_name)

        x1 = range(len(y1))
        print(len(y1))

        # Формируем список с обратной последовательностью
        y10 = y1[::-1]
        y20 = y2[::-1]
        y40 = y4[::-1]
        x10 = x0[::-1]
        print('p =')
        print(p)
        param = int(p)
        print(param)
        res = y10
        if (param // 3) == 0:
            res = y10
        if (param // 3) == 1:
            res = y20
        if (param // 3) == 2:
            res = y40

        if len(my_data) != 0:
            print("len(my_data)= ")
            print(len(my_data))
            # print(y40)
            res = y10 + y20 + y40

            return Response(res)
        else:
            return Response({"my_data": "No data"})


def identific(request):
    # находим последний присвоенный идентификатор, увеличиваем его номер на 1 и присваиваем регистрирующемуся
    latest_ident = Customerrec.objects.order_by('-datetime')[:1]
    X = []
    for LI in latest_ident:
         X.append(LI.identificator)
         y =  LI.identificator

    if len(X) == 0:
        z = 1
    else:
        print('latest_ident = ')
        print(y)
        z = int(y)+1

    return z


def init_dev(request):
    print('init_dev...')
    now = timezone.now()
    mac = request.GET.get('mac')

    try:
        print('try...')
        q = device.objects.filter(mac=mac)

        for LI in q:
            y = LI.identificator
            z = LI.devname

        print('identificator =')
        print(y)
        print('devname =')
        print(z)
        # 30:83:98:A2:6B:51

    except:
        print('except:')
        return Response({"init_dev_try": "No data (identificator or devname)"})

    try:
        print('from Customerrec try...')
        q = Customerrec.objects.filter(identificator = y)

        for LI in q:
            f = LI.comment

        print('codeword =')
        print(f)

    except:
        print('from Customerrec except:')
        return Response({"init_dev_try": "No codeword"})



    v1 =  {'devname': z, 'identificator': y, 'codeword' : f }

    return JsonResponse(v1, safe=False)


def update_dev(request):
    print('update_dev...')
    now = timezone.now()
    try:
        print('try...')
        q = device.objects.filter(user_id=request.user.id)
        my_dev = q.order_by('datetime')

        comment = []
        ident = []
        devname = []
        mac = []
        dt = []

        for LI in my_dev:
            comment.append(LI.comment)
            ident.append(LI.identificator)
            devname.append (LI.devname)
            mac.append(LI.mac)
            dt.append(LI.datetime)

        print('comment =')
        print(comment[-1])
        print('devname =')
        print(devname[-1])
        print('mac =')
        print(mac[-1])
        # 30:83:98:A2:6B:51

    except:
        print('except:')
        # return Response({"update_dev_try": "No data (identificator or devname)"})



    #return render(request, 'ai/update_dev.html', {"comment":comment, "devname":devname, "mac":mac, "dt":dt })
    return render(request, 'ai/update_dev.html', {"dev": my_dev})


def save_dev(request):
    print('save_dev...')
    now = timezone.now()
    mac = request.POST.get('mac')
    comment = request.POST.get('comment')

    print('len(mac) = ')
    print(len(mac))



    try:
        print('try...')
        q = device.objects.filter(user_id=request.user.id)
        my_dev = q.order_by('datetime')

        ident = []
        devname = []

        for LI in my_dev:
            ident.append(LI.identificator)
            devname.append (LI.devname)

        print('ident =')
        print(ident[-1])
        print('devname =')
        print(devname[-1])

    except:
        print('except:')
        return Response({"save_dev_try": "No data (identificator or devname)"})



    devname_new = 'Device_' + str(len(devname)+1)

    if len(mac)!=17:
        msg = "Внимание! Некорректно указан MAC-адрес, пожалуйста, повторите ввод"
        return render(request, 'ai/update_dev.html', {"dev": my_dev, 'msg': msg})

    maci=[]
    try:
        q = device.objects.filter(mac=mac)
        for LI in q:
            maci.append(LI.mac)


    except:
        print('нет такого MAC - заносим')

    if len(maci) >0:
        msg = "Внимание! Устройство с таким MAC-адресом уже зарегистрировано. Возможно некорректно указан MAC-адрес, пожалуйста, повторите ввод"
        return render(request, 'ai/update_dev.html', {"dev": my_dev, 'msg': msg})

    m = device(comment=comment, devname=devname_new, datetime=now, identificator=ident[-1], mac=mac,
                user_id=request.user.id)
    m.save()

    #return render(request, 'ai/update_dev.html', {"comment":comment, "devname":devname, "mac":mac, "dt":dt })
    return render(request, 'ai/update_dev_done.html',{'devname':devname_new, "comment":comment, "mac":mac, "datetime": now})





def def_comment(name_cow):
    print('def_comment...')
    try:
        print('try...')
        q = device.objects.filter(devname=name_cow)
        my_dev = q.order_by('datetime')
        comment = []
        for LI in my_dev:
            comment.append(LI.comment)

        print('comment =')
        print(comment[-1])
        z = comment[-1]

    except:
        print('except:')
        #return Response({"def_comment": "No data - devname"})
        z = "Строение 1"
    return z

def java_call(request):
    print("java_call")
    login = request.GET.get('login')
    print("login = ")
    print(login)

    try:
        print('try...')
        q = device.objects.filter(identificator=login)
        my_dev = q.order_by('datetime')
        devname = []
        for LI in my_dev:
            devname.append(LI.devname)

        print('devname =')
        print(devname)
        # z = comment[-1]

    except:
        print('except:')
        z  = {'device': 'false'}
        return z

    date_last = 1/1/2022
    y1_last = 0
    y2_last = 0
    y4_last = 0

    V_V = {}
    for dev in devname:
        try:
            q = Metering.objects.filter(meter_title=dev, meter_identificator=login)
            now = timezone.now()
            print(now)
            print("dev = ")
            print(dev)
        except:
            raise Http404("Нет запрашиваемых данных")
        latest_data_list = q.order_by('-meter_datetime')[:5]

        x0 = []
        y1 = []
        y2 = []
        y4 = []
        number = []

        i = 1
        # format = '%b %d %Y %I:%M%p' # Формат
        format = '%H:%M'  # Формат

        for data in latest_data_list:
            x0.append(data.meter_datetime)
            y1.append(data.meter_temperature)
            y2.append(data.meter_humidity)
            y4.append(data.meter_CO2)
            number.append(i)
            i = i + 1

        #name_cow = data.meter_title
        #print(name_cow)

        print("i=")
        print(i)
        print("x0 = ")
        print(x0)
        print("y1=")
        print(y1)
        print("y2=")
        print(y2)
        print("y4=")
        print(y4)


        # Формируем список с обратной последовательностью
        #y10 = y1[::-1]
        #y20 = y2[::-1]
        #y40 = y4[::-1]
        #x10 = x0[::-1]
        if i > 1:
        # последние элементы списков
            date_last = x0[-1]
            y1_last = y1[-1]
            y2_last = y2[-1]
            y4_last = y4[-1]
        else:
            date_last = 0
            y1_last = 0
            y2_last = 0
            y4_last = 0

        #v1  =   {'my_time': date_last, 'temperature': y1_last, "humidity": y2_last, 'gaz': y4_last}
        #temp_1 = "\""
        #print("temp_1=")
        #print(temp_1)
        #v2 = { dev : v1}

        v1  =  {'my_time': date_last, 'temperature': y1_last, "humidity": y2_last, 'gaz': y4_last}
        #V_V.append(v2)
        V_V[dev] = v1

    return JsonResponse(V_V, safe=False)