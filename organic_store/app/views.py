from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import logout as logouts
from django.shortcuts import render, redirect
from .models import register, suppliers, product, delivery_agent, category,cart,cart_items,orders
from .forms import registerform, Loginform, suppliersform, Editsuppliersform, addCategoryForm, addDeliveryAgentForm, \
    editCategoryForm, Addproductsform, editproductsform, Editcustomerform
from django.contrib import messages
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from PIL import Image
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date



# Create your views here.

def index(request):
    return render(request, "main/index.html")


def register_func(request):
    if request.method == 'POST':
        form = registerform(request.POST)
        if form.is_valid():
            post_email = form.cleaned_data['email']
            if User.objects.filter(email=post_email).exists():
                messages.warning(request, "Email Id Already Exist")
                return redirect('/register/')
            else:
                form.save()
                uname = register.objects.get(email=post_email)
                User.objects.create_user(username=uname, email=post_email)
                # fname = form.cleaned_data['firstname']
                # lname = form.cleaned_data['lastname']
                # subject = 'welcome to GFG world'
                # message = f'Hi {fname} {lname}, thank you for registering in geeksforgeeks.'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = ['aiswaryam421@gmail.com', ]
                # send_mail(subject, message, email_from, recipient_list)
                messages.warning(request, "Registration Successful")
                return redirect('/register/')

    else:
        form_value = registerform()
        return render(request, "main/register.html", {'form_key': form_value})


def supplier_reg(request):
    if request.method == 'POST':
        form = suppliersform(request.POST, request.FILES)
        if form.is_valid():
            post_email = form.cleaned_data['email']
            if User.objects.filter(email=post_email).exists():
                messages.warning(request, "Email Id Already Exist")
                return redirect('/supplier_reg/')
            else:
                form.save()
                uname = suppliers.objects.get(email=post_email)
                User.objects.create_user(username=uname, email=post_email)
                # fname = form.cleaned_data['firstname']
                # lname = form.cleaned_data['lastname']
                # subject = 'welcome to GFG world'
                # message = f'Hi {fname} {lname}, thank you for registering in geeksforgeeks.'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = ['aiswaryam421@gmail.com', ]
                # send_mail(subject, message, email_from, recipient_list)
                messages.warning(request, "Registration Successful")
                return redirect('/supplier_reg/')

    else:
        form_value = suppliersform()
        return render(request, "supplier/supplier_register.html", {'form_key': form_value})


def login(request):
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            email_val = form.cleaned_data['email']
            pswd = form.cleaned_data['password']
            try:
                user = register.objects.get(email=email_val)
                if user:

                    try:
                        user1 = register.objects.get(Q(reg_id=user.reg_id) & Q(password=pswd))
                        if user1:
                            request.session['session_id'] = user.reg_id
                            if user.usertype == 1:
                                return redirect('/admin_home/%s' % user.reg_id)
                            else:
                                return redirect('/customer_home/%s' % user.reg_id)
                    except register.DoesNotExist:
                        user1 = None
                        messages.warning(request, "Incorrect Password")
                        return redirect('/login/')
            except register.DoesNotExist:
                try:
                    user = suppliers.objects.get(email=email_val)
                    if user:
                        try:
                            user1 = suppliers.objects.get(Q(supplier_id=user.supplier_id) & Q(password=pswd))
                            if user1:
                                if user.status == True:
                                    request.session['session_id'] = user.supplier_id
                                    return redirect('/supplier_home/%s' % user.supplier_id)
                                else:
                                    messages.warning(request, "You are not yet approved")
                                    return redirect('/login/')
                        except suppliers.DoesNotExist:
                            user1 = None
                            messages.warning(request, "Incorrect Password")
                            return redirect('/login/')
                except suppliers.DoesNotExist:
                    try:
                        user = delivery_agent.objects.get(email=email_val)
                        if user:
                            try:
                                user1 = delivery_agent.objects.get(Q(agent_id=user.agent_id) & Q(password=pswd))
                                if user1:
                                    request.session['session_id'] = user.agent_id
                                    return redirect('/delivery_agent_home/%s' % user.agent_id)
                            except delivery_agent.DoesNotExist:
                                user1 = None
                                messages.warning(request, "Incorrect Password")
                                return redirect('/login/')
                    except delivery_agent.DoesNotExist:
                        user = None
                        messages.warning(request, "Invalid Email Id")
                        return redirect('/login/')
    else:
        form1 = Loginform()
        return render(request, "main/login.html", {'form': form1})


def customer_home(request, uid):
    if request.session.get('session_id'):
        categories = get_category()
        return render(request, "customers/customer_home.html", {'login_id': uid, 'categories': categories})
    else:
        return redirect('/login/')


def admin_home(request, uid):
    if request.session.get('session_id'):
        return render(request, "admin/admin_home.html", {'login_id': uid})
    else:
        return redirect('/login/')


def supplier_home(request, uid):
    if request.session.get('session_id'):
        return render(request, "supplier/supplier_home.html", {'login_id': uid})
    else:
        return redirect('/login/')


def customer_list(request, uid):
    if request.session.get('session_id'):
        customer = register.objects.filter(usertype=2)

        page_num = request.GET.get('page', 1)
        paginator = Paginator(customer, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/customer_list.html",
                      {'customer': customer, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def supplier_list(request, uid):
    if request.session.get('session_id'):
        supplier = suppliers.objects.filter(status=True)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(supplier, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/supplier_list.html",
                      {'supplier': supplier, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def delivery_agent_list(request, uid):
    if request.session.get('session_id'):
        agent = delivery_agent.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(agent, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)

        return render(request, "admin/delivery_agent_list.html",
                      {'agents': agent, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def delete_customer(request, uid, id):
    if request.session.get('session_id'):
        cust = register.objects.get(reg_id=id)
        user = User.objects.get(email=cust.email)
        user.delete()
        register.objects.filter(reg_id=id).delete()
        return redirect('/customer_list/%s' % uid)
    else:
        return redirect('/login/')


def delete_supplier(request, uid, id):
    if request.session.get('session_id'):
        supplier = suppliers.objects.get(supplier_id=id)
        user = User.objects.get(email=supplier.email)
        user.delete()
        suppliers.objects.get(supplier_id=id).delete()
        return redirect('/supplier_list/%s' % uid)
    else:
        return redirect('/login/')


def delete_delivery_agent(request, uid, id):
    if request.session.get('session_id'):
        agent = delivery_agent.objects.get(agent_id=id)
        user = User.objects.get(email=agent.email)
        user.delete()
        delivery_agent.objects.get(agent_id=id).delete()
        return redirect('/delivery_agent_list/%s' % uid)
    else:
        return redirect('/login/')


def approvesupplier(request, uid):
    if request.session.get('session_id'):
        supplier = suppliers.objects.filter(status=False)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(supplier, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/approve_supplier.html",
                      {'supplier': supplier, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def approve_supplier(request, uid, id):
    if request.session.get('session_id'):
        suppliers.objects.filter(supplier_id=id).update(status=True)
        return redirect('/approvesupplier/%s' % uid)
    else:
        return redirect('/login/')


def reject_supplier(request, uid, id):
    if request.session.get('session_id'):
        supplier = suppliers.objects.get(supplier_id=id)
        user = User.objects.get(email=supplier.email)
        user.delete()
        suppliers.objects.get(supplier_id=id).delete()
        return redirect('/approvesupplier/%s' % uid)
    else:
        return redirect('/login/')


def delivery_agent_reg(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = addDeliveryAgentForm(request.POST,request.FILES)
            length_of_string = 10
            sample_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@$^&*/!"
            pswd = ''.join(random.choices(sample_str, k=length_of_string))
            if form.is_valid():
                name = form.cleaned_data['name']
                post_email = form.cleaned_data['email']
                id_proof = form.files['id_proof']
                if User.objects.filter(email=post_email).exists():
                    messages.warning(request, "Email Id Already Exist")
                    return redirect('/delivery_agent_reg/%s' % uid)
                else:
                    delivery_agent.objects.create(name=name, email=post_email, password=pswd,id_proof=id_proof)
                    uname = delivery_agent.objects.get(email=post_email)
                    User.objects.create_user(username=uname, email=post_email)
                    name = form.cleaned_data['name']
                    # subject = 'Welcome to Organic Store'
                    # message = f'Hi {name}, Thank you for accepting our invitaion to join Organic Store.\n' \
                    #           f'Your Email Id and Password has been provided below :\n' \
                    #           f'Email Id : {post_email} \n' \
                    #           f'Password : {pswd} \n' \
                    #           f'Thank you..'
                    # email_from = settings.EMAIL_HOST_USER
                    # recipient_list = ['', ]
                    # send_mail(subject, message, email_from, recipient_list)
                    # messages.warning(request, "Registration Successful")
                    return redirect('/delivery_agent_reg/%s' % uid)
        else:
            form_value = addDeliveryAgentForm()
            return render(request, "admin/add_delivery_agent.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')

def add_category(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = addCategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.warning(request, "Category Added Successfully")
                return redirect('/add_category/%s' % uid)
        else:
            form_value = addCategoryForm()
            return render(request, "admin/add_category.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')

def edit_category(request, uid, id):
    if request.session.get('session_id'):
        categories = category.objects.get(category_id=id)
        if request.method == 'POST':
            form = editCategoryForm(request.POST, instance=categories)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/category_list/%s' % uid)
        else:
            form_value = editCategoryForm(instance=categories)
            return render(request, "admin/edit_category.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')


def category_list(request, uid):
    if request.session.get('session_id'):
        categories = category.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(categories, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/category_list.html",
                      {'categories': categories, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def delete_category(request, uid, id):
    if request.session.get('session_id'):
        category.objects.get(category_id=id).delete()
        return redirect('/category_list/%s' % uid)
    else:
        return redirect('/login/')


def supplier_profile(request, uid):
    if request.session.get('session_id'):
        supplier = suppliers.objects.get(supplier_id=uid)
        return render(request, "supplier/supplier_profile.html", {'supplier': supplier, 'login_id': uid})
    else:
        return redirect('/login/')


def edit_supplier_profile(request, uid):
    if request.session.get('session_id'):
        supplier = suppliers.objects.get(supplier_id=uid)
        if request.method == 'POST':
            form = Editsuppliersform(request.POST, instance=supplier)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/supplier_profile/%s' % uid)

        else:
            form_value = Editsuppliersform(instance=supplier)
            return render(request, "supplier/edit_supplier_profile.html",
                          {'form_key': form_value, 'supplier': supplier, 'login_id': uid})
    else:
        return redirect('/login/')

def customer_profile(request, uid):
    if request.session.get('session_id'):
        customer = register.objects.get(reg_id=uid)
        categories = get_category()
        return render(request, "customers/customer_profile.html", {'customer': customer,'categories':categories,'login_id': uid})
    else:
        return redirect('/login/')


def edit_customer_profile(request, uid):
    if request.session.get('session_id'):
        customer = register.objects.get(reg_id=uid)
        categories = get_category()
        if request.method == 'POST':
            form = Editcustomerform(request.POST, instance=customer)

            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/customer_profile/%s' % uid)

        else:
            form_value = Editcustomerform(instance=customer)
            return render(request, "customers/edit_customer_profile.html",
                          {'form_key': form_value, 'customer': customer,'categories':categories, 'login_id': uid})
    else:
        return redirect('/login/')


def add_product(request, uid):
    if request.session.get('session_id'):
        if request.method == 'POST':
            form = Addproductsform(request.POST, request.FILES)
            if form.is_valid():
                categories = form.cleaned_data['categories']
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                price = form.cleaned_data['price']
                image = form.files['image']
                supplier_id = suppliers.objects.get(supplier_id=uid)
                product.objects.create(categories=categories, name=name, description=description, price=price, image=image,
                                       supplier_id=supplier_id)
                messages.warning(request, "Product Added Successfully")
                return redirect('/add_product/%s' % uid)
        else:
            form_value = Addproductsform()
            return render(request, "products/add_products.html", {'form_key': form_value, 'login_id': uid})
    else:
        return redirect('/login/')


def edit_product(request, uid, id):
    if request.session.get('session_id'):
        products = product.objects.get(product_id=id)
        if request.method == 'POST':
            form = editproductsform(request.POST, request.FILES, instance=products)
            if form.is_valid():
                form.save()
                messages.warning(request, "Updated Successfully")
                return redirect('/products_list/%s' % uid)
        else:
            form_value = editproductsform(instance=products)
            return render(request, "products/edit_products.html",
                          {'form_key': form_value, 'products': products, 'login_id': uid})
    else:
        return redirect('/login/')


def products_list(request, uid):
    if request.session.get('session_id'):
        products = product.objects.filter(supplier_id=uid)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(products, 3)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "products/products_list.html",
                      {'products': products, 'page_obj': page_obj, 'login_id': uid})
    else:
        return redirect('/login/')


def delete_product(request, uid, id):
    if request.session.get('session_id'):
        product.objects.get(product_id=id).delete()
        return redirect('/products_list/%s' % uid)
    else:
        return redirect('/login/')


def admin_delete_product(request, uid, id):
    if request.session.get('session_id'):
        product.objects.get(product_id=id).delete()
        return redirect('/admin_products_list/%s' % uid)
    else:
        return redirect('/login/')


def admin_products_list(request, uid):
    if request.session.get('session_id'):
        products = product.objects.all()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(products, 3)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "admin/product_list.html", {'products': products, 'login_id': uid, 'page_obj': page_obj})
    else:
        return redirect('/login/')


def get_products(request, uid, id):
    if request.session.get('session_id'):
        products = product.objects.filter(categories_id=id)
        categories=get_category()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(products, 8)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "customers/view_products.html", {'page_obj': page_obj, 'login_id': uid, 'categories':categories})
    else:
        return redirect('/login/')

def product_more_details(request, uid, id):
    if request.session.get('session_id'):
        products = product.objects.get(product_id=id)
        categories=get_category()
        return render(request, "customers/product_more_details.html",{'products': products, 'login_id': uid,'categories':categories})
    else:
        return redirect('/login/')

def get_category():
    categories = category.objects.all()
    return categories



def add_to_cart(request,uid,products_id):
    if request.session.get('session_id'):
        products = product.objects.get(product_id=products_id)
        customers = register.objects.get(reg_id=uid)
        condition1 = Q(user_id=uid)
        condition2 = Q(status=True)
        try:
            carts=cart.objects.get(condition1 & condition2)

            if carts:
                cart_item=cart_items.objects.create(product_id=products,carts_id=carts,user_id=customers,suppliers_id=products.supplier_id)
                count=carts.count+1
                cart.objects.filter(user_id=uid).update(count=count)
                print(count)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except :
            carts=cart.objects.create(user_id=customers,count=1)
            cart_item=cart_items.objects.create(product_id=products,carts_id=carts,user_id=customers,suppliers_id=products.supplier_id)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/login/')

def carts(request,uid):
    if request.session.get('session_id'):
        categories=get_category()
        condition1 = Q(user_id=uid)
        condition2 = Q(status=True)
        try:
            carts=cart.objects.get(condition1 & condition2)
            try:
                cart_item = cart_items.objects.get(carts_id=carts.cart_id)
                return render(request, "cart/cart.html",{'cart_item': cart_item, 'login_id': uid, 'categories': categories,'count':carts.count,'cart_id':carts.cart_id})
            except cart_items.DoesNotExist:
                messages.warning(request, "Your cart is Empty")
                return render(request, "cart/cart.html", {'login_id': uid, 'categories': categories})
            except cart_items.MultipleObjectsReturned:
                cart_item = cart_items.objects.filter(carts_id=carts.cart_id)
                return render(request, "cart/cart.html",{'cart_item': cart_item, 'login_id': uid, 'categories': categories,'count':carts.count,'cart_id':carts.cart_id})
        except cart.DoesNotExist:
            messages.warning(request, "Your cart is Empty")
            return render(request, "cart/cart.html", {'login_id': uid, 'categories': categories})
    else:
        return redirect('/login/')

def remove_cart_item(request, uid, id,cart_id):
    if request.session.get('session_id'):
        cart_items.objects.get(item_id=id).delete()
        carts=cart.objects.get(cart_id=cart_id)
        count=carts.count-1
        cart.objects.filter(cart_id=cart_id).update(count=count)
        return redirect('/carts/%s' % uid)
    else:
        return redirect('/login/')

def get_item_count(request):
    if request.session.get('session_id'):
        uid=request.GET.get('login_id')
        condition1=Q(user_id=uid)
        condition2=Q(status=True)
        try:
            carts= cart.objects.get(condition1 and condition2)
            data = {'status': True, 'count': carts.count }
            return JsonResponse(data)
        except cart.DoesNotExist:
            data = {'status': False, 'count': 0}
            return JsonResponse(data)
    else:
        return redirect('/login/')

def inc_qty(request,uid,item_id):
    if request.session.get('session_id'):
        try:
            cart_item=cart_items.objects.get(item_id=item_id)
            if cart_item.qty < 5:
                qty=cart_item.qty+1
            else:
                qty=5
            cart_item1=cart_items.objects.filter(item_id=item_id).update(qty=qty)
            return redirect('/carts/%s' % uid)
        except cart_items.DoesNotExist:
            cart_item=None
            return redirect('/carts/%s' % uid)
    else:
        return redirect('/login/')



def dnc_qty(request,uid,item_id):
    if request.session.get('session_id'):
        try:
            cart_item=cart_items.objects.get(item_id=item_id)
            if cart_item.qty > 1:
                qty = cart_item.qty - 1
            else:
                qty = 1
            cart_item1=cart_items.objects.filter(item_id=item_id).update(qty=qty)
            return redirect('/carts/%s' % uid)
        except cart_items.DoesNotExist:
            cart_item=None
            return redirect('/carts/%s' % uid)
    else:
        return redirect('/login/')

def place_order(request,uid,carts_id):
    if request.session.get('session_id'):
        categories = get_category()
        user=register.objects.get(reg_id=uid)
        cart_item=cart_items.objects.filter(carts_id=carts_id)
        agent = delivery_agent.objects.filter(available=True).first()
        print(agent)
        total_price=0
        order_date=datetime.now().date()
        for i in cart_item:
            total_product_price=i.product_id.price * i.qty
            pickup_date = datetime.now() + timedelta(days=1)
            cart_item1 = cart_items.objects.get(item_id=i.item_id)
            total_price= total_price + total_product_price
            orders.objects.create(cart_item_id=cart_item1,pickup_date=pickup_date,total_product_price=total_product_price,user_id=user,order_date=order_date,agents_id=agent)
        return render(request, "orders/place_order.html", {'cart_item': cart_item,'login_id': uid, 'categories': categories, 'total_price' : total_price,'cart_id':carts_id})
    else:
        return redirect('/login/')

def checkout(request,uid,total_price,cart_id):
    if request.session.get('session_id'):
        categories = get_category()
        agent=orders.objects.filter(cart_item_id__carts_id=cart_id).values('agents_id').distinct().first()
        cart.objects.filter(user_id=uid).update(status=False)
        agent_id=agent['agents_id']
        delivery_agent.objects.filter(agent_id=agent_id).update(available=False)
        agent1=delivery_agent.objects.get(agent_id=agent_id)
        return render(request, "orders/checkout.html", {'agent':agent1,'login_id': uid, 'categories': categories, 'total_price' : total_price})
    else:
        return redirect('/login/')

def order_history(request,uid):
    if request.session.get('session_id'):
        order= orders.objects.filter(user_id=uid)
        categories=get_category()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(order, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "customers/orders.html", {'page_obj': page_obj, 'login_id': uid, 'categories':categories})
    else:
        return redirect('/login/')

def order_history(request,uid):
    if request.session.get('session_id'):
        order= orders.objects.filter(user_id=uid)
        categories=get_category()
        page_num = request.GET.get('page', 1)
        paginator = Paginator(order, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "customers/orders.html", {'page_obj': page_obj, 'login_id': uid, 'categories':categories})
    else:
        return redirect('/login/')

def new_order(request,uid):
    if request.session.get('session_id'):
        order = orders.objects.filter(cart_item_id__suppliers_id=uid).order_by('order_date')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(order, 5)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "supplier/new_orders.html", {'page_obj': page_obj, 'login_id': uid,})
    else:
        return redirect('/login/')

def delivery_agent_home(request, uid):
    if request.session.get('session_id'):
        return render(request, "delivery/delivery_agent_home.html", {'login_id': uid})
    else:
        return redirect('/login/')

def delivery_agent_orders(request,uid):
    if request.session.get('session_id'):
        order_list = orders.objects.filter(Q(agents_id=uid) & Q(deliver_status=False)).order_by('order_date')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(order_list, 4)  # 6 employees per page
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "delivery/my_orders.html", {'page_obj': page_obj, 'login_id': uid, })
    else:
        return redirect('/login/')

def pickup_order(request, uid, id):
    if request.session.get('session_id'):
        orders.objects.filter(order_id=id).update(pickup_status=True)
        return redirect('/delivery_agent_orders/%s' % uid)
    else:
        return redirect('/login/')

def deliver_order(request, uid, id):
    if request.session.get('session_id'):
        orders.objects.filter(order_id=id).update(deliver_status=True)
        delivery_agent.objects.filter(agent_id=uid).update(available=True)
        return redirect('/delivery_agent_orders/%s' % uid)
    else:
        return redirect('/login/')


def logout(request):
    del request.session['session_id']
    logouts(request)
    return redirect('/')

