from django.conf.urls import url
from .import views
from django.urls import path
from django.contrib.auth import views as auth_views
app_name = 'ai'
urlpatterns = [
    path('', views.start, name='start'),
    #path('ai/', views.index2, name='index2'),
    path('add/', views.add, name='add'),
    path('nabobj/', views.nabobj, name='nabobj'),
    path('show/', views.show, name='show'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    path('graph1/', views.graph1, name='graph1'),
    path('graph2/', views.graph2, name='graph2'),
    path('starter/<str:meter_title>/<int:chisizm>', views.starter, name='starter'),
    #path('starter/', views.starter, name='starter'),
    path('cows/<str:meter_title>/<int:chisizm>', views.cows, name='cows_page'),
    path('addcom/', views.index2, name='index2'),
    path('addcom/<int:metering_id>/', views.addcom, name='addcom'),
    path('addcom/<int:metering_id>/leave_comment2/', views.leave_comment2, name='leave_comment2'),
    path('pdstart/', views.pdstart, name='pdstart'),
    #path('pdcalc/<str:regn>/', views.pdcalc, name='pdcalc'),
    path('pdcalc/', views.pdcalc, name='pdcalc'),
    path('login/', views.MyprojectLoginView.as_view(), name='login_page'),
    path('register/', views.RegisterUserView.as_view(), name='register_page'),
    path('logout/', views.MyprojectLogout.as_view(), name='logout_page'),
    path('updateacc/', views.upDateAcc, name='updateacc'),
    path('rascheti/', views.rascheti, name='rascheti'),
    path('rascheti2/', views.rascheti2, name='rascheti2'),
    path('sendsms/', views.sendSMS, name='sendsms'),
    path('offerta/', views.offerta, name='offerta_page'),
    path('fillrec/', views.fillrec, name='fillrec_page'),
    path('recstart/', views.recstart, name='recstart_page'),
    path('recstart2/', views.recstart2, name='recstart2_page'),
    path('deposit/', views.deposit, name='deposit_page'),
    path('serv/', views.serv, name='serv_page'),
    path('mail/', views.mail, name='mail_page'),
    path('success/', views.success, name='mail_success_page'),
    path('codegen_emailsend/', views.codegen_emailsend, name='codegen_emailsend_page'),
    path('password-reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.MyPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('control/', views.control, name='control_page'),
    path('control_save/', views.control_save, name='control_save_page'),
    path('my_condition/', views.my_condition, name='my_condition_page'),
    path('my_condition_3/', views.my_condition_3, name='my_condition_3_page'),
    path('my_control/', views.my_controlView.as_view(), name='my_control_page'),
    path('test_js/', views.test_js, name='test_js_page'),
    path('test_js2/', views.test_js2, name='test_js_page2'),
    # path('test_js3/', views.test_js3, name='test_js3_page'),

    path('test_js3/<str:meter_title>/<int:chisizm>/', views.test_js3, name='test_js3_page'),

    path('my_data/', views.my_dataView.as_view(), name='my_data_page'),
    path('init_dev/', views.init_dev, name='init_dev_page'),
    path('update_dev/', views.update_dev, name='update_dev_page'),
    path('save_dev/', views.save_dev, name='save_dev_page'),
    path('java_call/', views.java_call, name='java_call_page'),
    path('edit_dev/', views.edit_dev, name='edit_dev_page'),
    path('start_edit/<str:dev_name>/', views.start_edit, name='start_edit_page'),
    path('save_edit_dev', views.save_edit_dev, name='save_edit_dev_page'),




]

