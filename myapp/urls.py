"""
URL configuration for WaterProofing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    #admin
    path('',views.login),
    path('register',views.register),
    path('dealer_register',views.dealer_register),
    path('dealer_register_post',views.dealer_register_post),
    path('administrative_staff_register',views.administrative_staff_register),
    path('administrative_staff_register_post',views.administrative_staff_register_post),
    path('add_manage_worker',views.add_manage_worker),
    path('add_product',views.add_product),
    path('admin_home',views.admin_home),
    path('allocate_works/<id>',views.allocate_works),
    path('allocate_works_post',views.allocate_works_post),
    path('approve_job_request',views.approve_job_request),
    path('delete_work/<id>',views.delete_work),
    path('send_reply/<id>',views.send_reply),
    path('verify_administrativestaff',views.verify_administrativestaff),
    path('verify_dealer',views.verify_dealer),
    path('view_complaint',views.view_complaint),
    path('view_feedback',views.view_feedback),
    path('specify_feedback/<id>',views.specify_feedback),
    path('view_job_allocation',views.view_job_allocation),
    path('view_product',views.view_product),
    path('view_worker',views.view_worker),
    path('send_reply_post',views.send_reply_post),
    path('product_update_admin/<id>',views.product_update_admin),
    path('product_update_admin_post',views.product_update_admin_post),
    path('edit_worker/<id>',views.edit_worker),
    path('edit_worker_post',views.edit_worker_post),
    path('delete_worker/<id>',views.delete_worker),
    path('delete_product/<id>',views.delete_product),
    path('search_product',views.search_product),




    #administrtive staff
    path('add_manage_worker_administrative', views.add_manage_worker_administrative),
    path('administrative_staff_home', views.administrative_staff_home),
    path('product_update/<id>', views.product_update),
    path('send_reply_administrative/<id>', views.send_reply_administrative),
    path('view_complaint_administrative', views.view_complaint_administrative),
    path('view_feedback_administrative', views.view_feedback_administrative),
    path('view_job_allocation_administrative', views.view_job_allocation_administrative),
    path('view_job_request', views.view_job_request),
    path('view_product_administrative', views.view_product_administrative),
    path('view_job_request', views.view_job_request),
    path('view_product_administrative', views.view_product_administrative),
    path('view_purchase_request', views.view_purchase_request),
    path('view_purchase_request_more', views.view_purchase_request_more),
    path('view_worker_administrative', views.view_worker_administrative),
    path('accept_dealers/<id>', views.accept_dealers),
    path('reject_dealers/<id>', views.reject_dealers),
    path('accept_administrativestaff/<id>', views.accept_administrativestaff),
    path('reject_administrativestaff/<id>', views.reject_administrativestaff),
    path('add_product_post',views.add_product_post),
    path('add_manage_worker_post',views.add_manage_worker_post),
    path('add_product_administrative',views.add_product_administrative),
    path('add_product_administrative_post',views.add_product_administrative_post),
    path('send_reply_administrative_post',views.send_reply_administrative_post),
    path('indexad',views.indexad),
    path('indexadm',views.indexadm),


    #DEALERS
    path('cart/<id>',views.cart),
    path('order',views.order),
    path('view_cart',views.view_cart),
    path('view_order',views.view_order),
    path('send_feedback/<id>',views.send_feedback),
    path('send_feedback_post',views.send_feedback_post),
    path('view_order_more',views.view_order_more),
    path('view_product_dealer',views.view_product_dealer),
    path('view_product_more_dealer/<id>',views.view_product_more_dealer),
    path('dealer_home',views.dealer_home),
    path('orderscode',views.orderscode),
    path('add_to_cart',views.add_to_cart),
    path('send_request',views.send_request),
    path('check_order',views.check_order),
    path('check_order_more/<id>',views.check_order_more),
    path('send_request_post',views.send_request_post),
    path('delete_cart/<cartid>',views.delete_cart),
    path('send_complaint',views.send_complaint),
    path('send_complaint_post',views.send_complaint_post),
    path('view_replay_dealer',views.view_replay_dealer),
    path('view_feedback_dealer',views.view_feedback_dealer),
    path('check_status',views.check_status),
    path('search_date',views.search_date),
    path('contact',views.contact),
    path('about',views.about),
    # path('user_pay_proceed/<id>/<amt>',views.user_pay_proceed),
    # path('on_payment_success',views.on_payment_success),
    path('buy_post',views.buy_post),



    #WORKER
    path('worker_home', views.worker_home),
    path('view_work', views.view_work),
    path('status_update/<id>', views.status_update),
    path('status_update_post', views.status_update_post),
    path('index', views.index),
    path('dealer_index', views.dealer_index),

    #actions
    path('login_post',views.login_post),
]
