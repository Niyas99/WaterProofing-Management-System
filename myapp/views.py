import json
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from myapp.models import *


def login(request):
    return render(request,'login.html')
def login_post(request):
    username=request.POST['textfield']
    pswd=request.POST['textfield2']

    a=login_table.objects.get(username=username,password=pswd)
    if a.type=='admin':
        return  HttpResponse('''<script>alert('ADMIN LOGINED');window.location='/admin_home'</script>''')
    elif a.type=='administrative_staff':
        return HttpResponse('''<script>alert('ADMINISTRATIVE LOGINED');window.location='/administrative_staff_home'</script>''')
    elif a.type=='dealer':
        request.session['lid']=a.id
        return HttpResponse('''<script>alert('DEALER LOGINED');window.location='/dealer_home'</script>''')
    elif a.type=='worker':
        request.session['lid'] = a.id
        return HttpResponse('''<script>alert('WORKER LOGINED');window.location='/worker_home'</script>''')
    else:
        return HttpResponse('''<script>alert('INVALID LOGIN');window.location='/'</script>''')

def register(request):
    return render(request,'register.html')

#DEALER REGISTRATION:

def dealer_register(request):
    return render(request,'dealer_register.html')

def dealer_register_post(request):
    username = request.POST['textfield8']
    password = request.POST['textfield10']
    name = request.POST['textfield']
    contact = request.POST['textfield2']
    email = request.POST['textfield3']
    place = request.POST['textfield4']
    post = request.POST['textfield5']
    pin = request.POST['textfield6']
    id_proof_number = request.POST['textfield7']
    image = request.FILES['file']

    fs = FileSystemStorage()
    fp = fs.save(image.name, image)

    l=login_table()
    l.username = username
    l.password = password
    l.type = 'PENDING'
    l.save()





    d=dealers_table()
    d.name = name
    d.LOGIN = l
    d.contact = contact
    d.email = email
    d.place = place
    d.post = post
    d.pin = pin
    d.id_proof_number = id_proof_number
    d.image = fp
    d.save()
    return HttpResponse('''<script>alert('REGISTER REQUEST SEND');window.location='/register'</script>''')

#ADMINISTRATIVE STAFF REGISTRATION

def administrative_staff_register(request):
    return render(request,'administrative_staff_register.html')


def administrative_staff_register_post(request):
    username = request.POST['textfield8']
    password = request.POST['textfield10']
    name = request.POST['textfield']
    contact = request.POST['textfield2']
    email = request.POST['textfield3']
    role = request.POST['textfield4']
    id_proof_number = request.POST['textfield7']
    image = request.FILES['file']

    fs = FileSystemStorage()
    fp = fs.save(image.name, image)

    l = login_table()
    l.username = username
    l.password = password
    l.type = 'PENDING'
    l.save()

    a=administrative_staff_table()

    a.name = name
    a.LOGIN = l
    a.contact = contact
    a.email = email
    a.role = role
    a.id_proof_number = id_proof_number
    a.image = fp
    a.save()

    return HttpResponse('''<script>alert('REGISTER REQUEST SEND');window.location='/register'</script>''')



#ADD WORKER

def add_manage_worker(request):
    return render(request,'admin/add_manage_worker.html')

def add_manage_worker_post(request):
    name=request.POST['textfield']
    contact = request.POST['textfield3']
    email = request.POST['textfield2']
    skills = request.POST['textfield4']
    availability = request.POST['textfield5']
    image=request.FILES['file']
    id_proof_number = request.POST['textfield6']
    username=request.POST['textfield7']
    password=request.POST['textfield8']


    l=login_table()
    l.username=username
    l.password=password
    l.type='worker'
    l.save()



    fs=FileSystemStorage()
    fp=fs.save(image.name,image)

    c=workers_table()
    c.name = name
    c.contact = contact
    c.email = email
    c.skills = skills
    c.availability = availability
    c.image = fp
    c.id_proof_number = id_proof_number
    c.LOGIN = l
    c.save()

    return HttpResponse('''<script>alert('WORKER ADDED');window.location='/view_worker'</script>''')
    return render(request,'admin/add_manage_worker.html')

#add product


def add_product(request):
    return render(request,'admin/add_product.html')


def add_product_post(request):
    name=request.POST['textfield']
    description=request.POST['textfield2']
    price = request.POST['textfield3']
    stock = request.POST['textfield4']
    image = request.FILES['file']

    fs=FileSystemStorage()
    fp=fs.save(image.name,image)

    c=product_table()
    c.name=name
    c.description=description
    c.price=price
    c.stock=stock
    c.image=fp
    c.save()
    return HttpResponse('''<script>alert('PRODUCT ADDED');window.location='/view_product'</script>''')
    return render(request,'admin/add_product.html')

def admin_home(request):
    obusers=dealers_table.objects.filter(LOGIN__type="dealer")
    obworkers = workers_table.objects.all()
    oborder = purchase_request_more_table.objects.all()
    obfeed = feedback_table.objects.all()


    request.session["dealers"]=len(obusers)
    request.session["workers"]=len(obworkers)
    request.session["order"]=len(oborder)
    request.session["feed"]=len(obfeed)

    return render(request,'admin/index.html',{"dealers":len(obusers),"workers":len(obworkers),"order":len(oborder),"feed":len(obfeed)})


#PRODUCT UPDATE

def product_update_admin(request,id):
    request.session['pid'] = id
    return  render(request,'admin/product_update_admin.html')

def product_update_admin_post(request):
    stock=request.POST['textfield']
    r = request.session['pid']

    p=product_table.objects.get(id=r)
    p.stock = stock
    p.save()
    return HttpResponse('''<script>alert('STOCK UPDATED');window.location='/view_product'</script>''')



def approve_job_request(request):
    a=job_request_table.objects.all()
    return render(request,'admin/approve_job_request.html',{'data':a})

def allocate_works(request,id):
    request.session['jid'] = id # job request id
    a=workers_table.objects.all()
    return render(request, 'admin/allocate_works.html', {'data':a})

def allocate_works_post(request):
    from datetime import date
    name=request.POST['select']

    r = request.session['jid']
    start_date = request.POST['startdate']
    end_date = request.POST['enddate']


    a=allocate_work()
    a.JOB_REQUEST_id=r
    a.start_date = start_date
    a.allocation_date = date.today()
    a.end_date = end_date
    a.WORKER = workers_table.objects.get(id=name)
    a.save()
    return HttpResponse('''<script>alert('WORK ALLOCATED');window.location='/approve_job_request'</script>''')

def delete_work(request,id):
    work = allocate_work.objects.get(id=id)
    work.delete()
    return HttpResponse('''<script>alert('WORK DELETED');window.location='/approve_job_request'</script>''')
def send_reply(request,id):
    request.session['cid']=id
    return render(request,'admin/send_reply.html')

def send_reply_post(request):
    replay=request.POST['textfield']
    r=request.session['cid']

    c=complaint_table.objects.get(id=r)
    c.replay = replay
    c.save()
    return HttpResponse('''<script>alert('REPLIED');window.location='/view_complaint'</script>''')




#admin administartive staff
def verify_administrativestaff(request):
    a=administrative_staff_table.objects.all()
    return render(request,'admin/verify_administrativestaff.html',{'data':a})

def accept_administrativestaff(request,id):
    ob=login_table.objects.get(id=id)
    ob.type='administrative_staff'
    ob.save()
    return HttpResponse('''<script>alert('ACCEPTED');window.location='/verify_administrativestaff'</script>''')

def reject_administrativestaff(request,id):
    ob=login_table.objects.get(id=id)
    ob.type='rejected'
    ob.save()
    return HttpResponse('''<script>alert('REJECTED');window.location='/verify_administratiestaff'</script>''')


#dealer verification
def verify_dealer(request):
    a=dealers_table.objects.all()
    return render(request,'admin/verify_dealer.html',{'data':a})

def accept_dealers(request,id):
    ob=login_table.objects.get(id=id)
    ob.type='dealer'
    ob.save()
    return HttpResponse('''<script>alert('ACCEPTED');window.location='/verify_dealer'</script>''')

def reject_dealers(request,id):
    ob=login_table.objects.get(id=id)
    ob.type='rejected'
    ob.save()
    return  HttpResponse('''<script>alert('REJECTED');window.location='/verify_dealer'</script>''')




def view_complaint(request):
    a=complaint_table.objects.all()
    return render(request,'admin/view_complaint.html',{'data':a})

def view_feedback(request):
    a=feedback_table.objects.all()
    return render(request,'admin/view_feedback.html',{'data':a})

def specify_feedback(request,id):

    # request.session["productid"] = id
    a = product_table.objects.get(id=id)

    feed = feedback_table.objects.filter(PRODUCT=id)
    return render(request,'admin/specify_feedback.html',{'i':a,'feed':feed})


def view_job_allocation(request):
    a = allocate_work.objects.all()
    return render(request,'admin/view_job_allocation.html',{'data':a})


def view_product(request):
    a=product_table.objects.all()
    return render(request,'admin/view_product.html',{'data':a})

def search_product(request):
    search = request.POST['textfield']
    a=product_table.objects.filter(name__icontains=search)
    return render(request,'admin/view_product.html',{'data':a})





def view_worker(request):
    a=workers_table.objects.all()
    return render(request,'admin/view_worker.html',{'data':a})

def edit_worker(request,id):
    worker= workers_table.objects.get(id=id)
    request.session['wid'] = id
    return render(request,'admin/edit_worker.html',{'data':worker})

def edit_worker_post(request):
    r = request.session['wid']
    name = request.POST['textfield']
    contact = request.POST['textfield3']
    email = request.POST['textfield2']
    skills = request.POST['textfield4']
    availability = request.POST['textfield5']
    id_proof_number = request.POST['textfield6']

    w = workers_table.objects.get(id=r)


    if 'file' in request.FILES:
        image=request.FILES['file']
        fs = FileSystemStorage()
        fp = fs.save(image.name, image)
        w.image = fp
        w.save()

    w.name = name
    w.contact = contact
    w.email = email
    w.skills = skills
    w.availability = availability
    w.id_proof_number = id_proof_number
    w.save()
    return HttpResponse('''<script>alert('WORKER UPDATED');window.location='/view_worker'</script>''')

def delete_worker(request,id):
    worker = workers_table.objects.get(id=id)
    worker.delete()
    return HttpResponse('''<script>alert('WORKER DELETED');window.location='/view_worker'</script>''')

def delete_product(request,id):
    product = product_table.objects.get(id=id)
    product.delete()
    return HttpResponse('''<script>alert('PRODUCT DELETED');window.location='/view_worker'</script>''')





#administrative staff

def add_manage_worker_administrative(request):
    return render(request,'administrative_staff/add_manage_worker_administrative.html')


#ADD PRODUCT ADMINISTRATIVE

def add_product_administrative(request):
    return render(request,'administrative_staff/add_product_administrative.html')

def add_product_administrative_post(request):
    name = request.POST['textfield']
    description =  request.POST['textfield2']
    price = request.POST['textfield3']
    stock = request.POST['textfield4']
    image = request.FILES['file']

    fs = FileSystemStorage()
    fp = fs.save(image.name,image)

    c = product_table
    c.name = name
    c.description = description
    c.price = price
    c.stock = stock
    c.image = fp
    c.save()


    return  HttpResponse('''<script>aleret('PRODUCT ADDED');window.location='/view_product_admnistrative'</script>''')
    return render(request,'administrative_staff/add_product_administrative.html')

def administrative_staff_home(request):
    return render(request,'administrative_staff/indexad.html')

#PRODUCT UPDATE

def product_update(request,id):
    request.session['pid'] = id
    return  render(request,'admin/product_update_admin.html')

def product_update_admin_post(request):
    stock=request.POST['textfield']
    r = request.session['pid']

    p=product_table.objects.get(id=r)
    p.stock = stock
    p.save()
    return HttpResponse('''<script>alert('STOCK UPDATED');window.location='/view_product'</script>''')

    # return  render(request,'admin/product_update_admin.html')

def administrative_staff(request):
    return render(request,'administrative_staff/adminstrative_staff_home.html')
#ADDMINISTARTIVE REPLY COMPLAINT

def send_reply_administrative(request,id):
    request.session['cid'] = id
    return render(request,'administrative_staff/send_reply_administrative.html')


def send_reply_administrative_post(request):
    r = request.session['cid']
    replay = request.POST['textfield']

    s = complaint_table.objects.get(id=r)
    s.replay = replay
    s.save()


    return HttpResponse('''<script>alert('REPLAIED');window.location='/view_complaint_administrative'</script>''')


def view_complaint_administrative(request):
    a=complaint_table.objects.all()
    return render(request,'administrative_staff/view_complaint_administrative.html',{'data':a})

def view_feedback_administrative(request):
    a = feedback_table.objects.all()
    return render(request,'administrative_staff/view_feedback_administrative.html',{'data':a})

def view_job_allocation_administrative(request):
    a = allocate_work.objects.all()
    return render(request,'administrative_staff/view_job_allocation_administrative.html',{'data':a})

def view_job_request(request):
    a = job_request_table.objects.all()
    return render(request,'administrative_staff/view_job_request.html',{'data':a})

def view_product_administrative(request):
    a=product_table.objects.all()
    return render(request,'administrative_staff/view_product_administrative.html',{'data':a})

def view_purchase_request(request):
    a=purchase_request_table.objects.all()
    return render(request,'administrative_staff/view_purchase_request.html',{'data':a})

def view_purchase_request_more(request):
    a= purchase_request_more_table.objects.all()
    return render(request,'administrative_staff/view_purchase_request_more.html',{'data':a})

def view_worker_administrative(request):
    a=workers_table.objects.all()
    return render(request,'administrative_staff/view_worker_administrative.html',{'data':a})



#DEALERS

def cart(request,id):
    request.session['pid']=id
    return render(request,'dealers/cart.html')

def dealer_home(request):
    products = product_table.objects.all()

    return render(request,'dealers/index.html',{'products':products})


def order(request):
    return render(request,'dealers/order.html')

def contact(request):
    return render(request,'dealers/contact.html')

def view_cart(request):
    a=purchase_request_more_table.objects.filter(PURCHASE__status="CART",PURCHASE__DEALEARS__LOGIN=request.session["lid"])
    amt=0
    for i in a:
        amt=amt+i.amount
    return render(request,'dealers/view_cart.html',{'data':a,"total":amt})

def view_order(request):
    return render(request,'dealers/view_order.html')

def view_order_more(request):
    return render(request,'dealers/view_order_more.html')

def view_product_dealer(request):

    a = product_table.objects.all()
    return render(request, 'dealers/view_product_dealer.html', {'data':a})

def send_request(request):
    return render(request,'dealers/send_request.html')

def send_request_post(request):
    work=request.POST['textfield']
    description=request.POST['textfield2']
    import datetime

    a=job_request_table()
    a.work=work
    a.DEALEARS=dealers_table.objects.get(LOGIN=request.session["lid"])
    a.description = description
    a.date = datetime.datetime.today().now()
    a.save()
    return HttpResponse('''<script>alert('JOB REQUEST SEND SUCCESSFULLY');window.location='/send_request'</script>''')


def view_product_more_dealer(request,id):
    request.session['proid']=id
    a = product_table.objects.get(id=id)

    feed=feedback_table.objects.filter(PRODUCT=id)
    return render(request, 'dealers/view_product_more_dealer.html', {'i':a,'feed':feed})


def orderscode(request):

    pro_id = request.session['proid']
    qty = request.POST['textfield']
    lid = request.session['lid']

    ob = product_table.objects.get(id=pro_id)
    tt = int(ob.price) * int(qty)
    stock = ob.stock
    nstk = int(stock) - int(qty)
    if int(stock)>= int(qty):
        up = product_table.objects.get(id=pro_id)
        up.stock = nstk
        up.save()
        ob = purchase_request_table()
        ob.status = 'ORDER'
        from datetime import datetime

        ob.date = datetime.today().date()
        ob.DEALEARS = dealers_table.objects.get(LOGIN__id=lid)
        ob.amount = tt
        ob.save()
        obj = purchase_request_more_table()
        obj.PURCHASE = ob
        obj.PRODUCT=product_table.objects.get(id=pro_id)
        obj.quantity = qty
        obj.status = 'ORDER'
        obj.date=datetime.now()
        obj.amount = tt
        obj.save()

        obx = payment()
        obx.date = datetime.today()
        obx.time = datetime.now()
        obx.PURCHASE_REQUEST_TABLE = purchase_request_table.objects.get(id=ob.id)
        obx.status = 'ordered'
        obx.save()


        # return HttpResponse("<script>window.location='/user_pay_proceed/"+str(ob.id)+"/"+str(tt)+"'</script>")
        return HttpResponse("<script>alert('Ordered');window.location='/view_product_dealer'</script>")
    else:
        return HttpResponse('''<script>alert('OUT OF STOCK');window.location='/view_product_dealer'</script>''')


def add_to_cart(request):
    qty = request.POST['textfield']
    pid = request.session['pid']
    lid = request.session['lid']

    qq = product_table.objects.get(id=pid)
    tt = int(qq.price) * int(qty)
    stock = int(qq.stock)
    nstk = int(stock) - int(qty)
    from datetime import datetime


    if stock >= int(qty):
        up = product_table.objects.get(id=pid)
        up.stock = nstk
        up.save()
        q =purchase_request_table.objects.filter(DEALEARS=dealers_table.objects.get(LOGIN__id=lid), status='CART')
        if len(q) == 0:
            qt = purchase_request_table()


            qt.date = datetime.today().date()
            qt.DEALEARS = dealers_table.objects.get(LOGIN=lid)
            qt.status = 'CART'
            qt.amount = tt
            qt.save()

            qty1 = purchase_request_more_table()
            qty1.quantity = qty
            qty1.PRODUCT = product_table.objects.get(id=pid)
            qty1.PURCHASE = qt
            qty1.amount=tt

            qty1.date = datetime.today()
            qty1.save()

            return HttpResponse('''<script>alert('ADDED SUCCESSFULLY');window.location='/view_product_dealer'</script>''')

        else:
            total = int(q[0].amount) + int(tt)
            qt = purchase_request_table.objects.get(id=q[0].id)
            qt.amount = total
            qt.save()
            qty1 = purchase_request_more_table.objects.filter(PRODUCT__id=pid, PURCHASE__id=q[0].id)
            if len(qty1) == 0:
                qqt = purchase_request_more_table()
                qqt.PURCHASE = q[0]
                qqt.PRODUCT = product_table.objects.get(id=pid)
                qqt.quantity = qty
                qqt.amount=tt
                qqt.date = datetime.now().date()
                qqt.save()
            else:
                qry1 = purchase_request_more_table.objects.get(id=qty1[0].id)
                quty = int(qty1[0].quantity) + int(qty)
                amt=int(qty1[0].amount)+int(tt)
                qry1.quantity = quty
                qry1.amount=amt
                qry1.save()
                return HttpResponse('''<script>alert('ADDED SUCCESSFULLY');window.location='/view_product_dealer'</script>''')

    else:
        return HttpResponse('''<script>alert('OUT OF STOCK');window.location='/view_product_dealer'</script>''')

    return HttpResponse('''<script>alert('ADDED SUCCESSFULLY');window.location='/view_product_dealer'</script>''')

def delete_cart(request,cartid):
    ob=purchase_request_more_table.objects.get(id=cartid)
    amt=ob.amount
    qty=ob.quantity
    pid=ob.PRODUCT.id

    obx=purchase_request_table.objects.get(id=ob.PURCHASE.id)
    tot=int(obx.amount)-int(amt)
    obx.amount=tot
    obx.save()

    obx1=product_table.objects.get(id=pid)
    totqty=int(obx1.stock)+int(qty)
    obx1.stock=totqty
    obx1.save()

    ob.delete()
    return HttpResponse('''<script>alert('REMOVED FROM CART');window.location='/view_cart'</script>''')

def check_order(request):
    lid = request.session['lid']
    a = purchase_request_table.objects.filter(~Q(status="CART"),DEALEARS=dealers_table.objects.get(LOGIN__id=lid))
    return render(request,'dealers/check_order.html',{'data':a})

def check_order_more(request,id):
    a=purchase_request_more_table.objects.filter(PURCHASE=id)
    return render(request, 'dealers/check_order_more.html', {'data': a})

def send_complaint(request):
    return render(request,'dealers/send_complaint.html')

def send_complaint_post(request):
    description = request.POST['textfield']

    a = complaint_table()
    a.DEALEARS = dealers_table.objects.get(LOGIN=request.session["lid"])
    a.description = description
    a.replay = 'PENDING'
    a. date = datetime.datetime.today().now()
    a.save()
    return HttpResponse('''<script>alert('COMPLAINT SEND SUCCESSFULLY');window.location='/view_replay_dealer'</script>''')

def view_replay_dealer(request):
    lid = request.session['lid']
    a = complaint_table.objects.filter(DEALEARS=dealers_table.objects.get(LOGIN__id=lid))
    return render(request,'dealers/view_replay_dealer.html',{'data':a})


def send_feedback(request,id):

    request.session["productid"]=id

    return render(request,'dealers/send_feedback.html')




def send_feedback_post(request):

    print(request.POST)
    comments = request.POST['textfield']
    rating = request.POST['rating']

    a = feedback_table()
    a.DEALEARS = dealers_table.objects.get(LOGIN=request.session["lid"])
    a.PRODUCT_id=request.session["productid"]
    a.comments =comments
    a.rating = rating
    a.date = datetime.now().date()
    a.save()
    return HttpResponse('''<script>alert('FEEDBACK SEND SUCCESSFULLY');window.location='/view_product_dealer'</script>''')

def search_date(request):
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')


        if fromdate and todate:
            records = purchase_request_more_table.objects.filter(date__range=[fromdate, todate])
        else:
            records = purchase_request_more_table.objects.all()

        return render(request, 'dealers/check_order.html', {'data': records})

    return render(request, 'dealers/check_order.html', {'data': []})


def view_feedback_dealer(request):
    lid = request.session['lid']
    a = feedback_table.objects.filter(DEALEARS=dealers_table.objects.get(LOGIN__id=lid))
    return  render(request,'dealers/view_feedback_dealer.html',{'data':a})


def check_status(request):
    b= allocate_work.objects.filter(JOB_REQUEST__DEALEARS__LOGIN_id=request.session['lid'])
    return render(request,'dealers/check_status.html',{'data':b})


#WORKER

def worker_home(request):
    return render(request,'worker/worker_home.html')

def view_work(request):
    a = allocate_work.objects.filter(WORKER__LOGIN__id=request.session['lid'])
    return render(request,'worker/view_work.html',{'data': a })

def status_update(request,id):
    request.session['aid'] =id
    return render(request,'worker/status_update.html')


def status_update_post(request):
    status = request.POST['select']
    i = request.session['aid']


    a=allocate_work.objects.get(id=i)
    a.status = status
    a.save()
    return HttpResponse('''<script>alert('STATUS UPDATED');window.location='/view_work'</script>''')


def index(request):

    return render(request,'admin/index.html')


def dealer_index(request):
    return render(request,'dealers/index.html')

def about(request):
    return render(request,'dealers/about.html')



def indexad(request):
    return render(request,'administrative_staff/indexad.html')

def indexadm(request):
    return render(request,'administrative_staff/indexadm.html')


# ------------------------------payment-----------------


# import  razorpay
# def user_pay_proceed(request,id,amt):
#     request.session['rid'] = id
#
#
#     request.session['pay_amount'] = int(amt)
#     client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
#     print(client)
#     payment = client.order.create({'amount': str(amt)+"00", 'currency': "INR", 'payment_capture': '1'})
#     res=dealers_table.objects.get(LOGIN__id=request.session['lid'])
#
#
#     ob=purchase_request_table.objects.get(id=request.session['rid'])
#
#     purchase_request_more_table.objects.filter(PURCHASE=ob.id).update(status="paid")
#
#     ob.status='paid'
#
#     ob.save()
#
#
#
#     return render(request, 'dealers/UserPayProceed.html', {'p':payment, 'val':res, "lid":request.session['lid'], "id":request.session['rid']})

#
#
# def on_payment_success(request):
#     request.session['rid'] = request.GET['id']
#     request.session['lid'] = request.GET['lid']
#     # var = auth.authenticate(username='admin', password='admin')
#     # if var is not None:
#     #     auth.login(request, var)
#     # amt = request.session['pay_amount']
#     ob=payment()
#     ob.date=datetime.today()
#     ob.time=datetime.now()
#     ob.PURCHASE_REQUEST_TABLE=purchase_request_table.objects.get(id=request.session['rid'])
#     ob.status='paid'
#     ob.save()
#
#
#     return HttpResponse('''<script>alert("Success! Thank you for your Contribution");window.location="/view_product_dealer"</script>''')
#



def buy_post(request):

    lid=request.session["lid"]

    ob=purchase_request_table.objects.filter(DEALEARS__LOGIN=lid,status="CART")
    if len(ob)>0:
        ob1 = purchase_request_table.objects.get(DEALEARS__LOGIN=lid, status="CART")

        ob2=purchase_request_more_table.objects.filter(PURCHASE=ob1.id).update(status="ordered")

        obx = payment()
        obx.date = datetime.today()
        obx.time = datetime.now()
        obx.PURCHASE_REQUEST_TABLE = purchase_request_table.objects.get(id=ob1.id)
        obx.status = 'ordered'
        obx.save()

        ob1.status="ordered"
        ob1.save()



        # return HttpResponse("<script>window.location='/user_pay_proceed/" + str(ob[0].id) + "/" + str(ob[0].amount) + "'</script>")
        return HttpResponse("<script>alert('Ordered');window.location='/view_cart'</script>")



    else:
        return HttpResponse('''<script>alert('No Products in Cart');window.location='/view_cart'</script>''')







