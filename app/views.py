from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from email.mime.multipart import MIMEMultipart
from django.utils.encoding import force_bytes
from django.contrib.auth.hashers import *
from email.mime.text import MIMEText
from datetime import date, timedelta
from django.db.models import *
from app.models import *
import smtplib, ssl

def Home(request):
    return render(request, "home.html")

def SignIn(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_superuser == True:
                return redirect('/admindashboard')
            else:
                return redirect('/investingtoday/'+urlsafe_base64_encode(force_bytes(request.POST['username'])))
        elif SignUpRequests.objects.filter(username=request.POST['username']).exists() == True:
            msg = "your account must be approved first"
            context = {'message': msg}
            return render(request, "signin.html", context)
        else:
            msg = "username or password is incorrect !!!"
            context = {'message': msg}
            return render(request, "signin.html", context)   
    else:        
        return render(request, "signin.html")

def SignUp(request):
    if request.method == 'POST':   
        if request.POST['password1'] == request.POST['password2']:
            if SignUpRequests.objects.filter(username=request.POST['username']).exists() or User.objects.filter(username=request.POST['username']).exists():
                msg = "username already taken !!!"
                context = {'message': msg}
                return render(request, "signup.html", context)
            elif SignUpRequests.objects.filter(number_phone=request.POST['number_phone']).exists() or ApprovedSignUpRequests.objects.filter(number_phone=request.POST['number_phone']).exists():
                msg = "number phone already taken !!!"
                context = {'message': msg}
                return render(request, "signup.html", context)         
            elif SignUpRequests.objects.filter(bank_account=request.POST['bank_account']).exists() or ApprovedSignUpRequests.objects.filter(bank_account=request.POST['bank_account']).exists():
                msg = "bank account already taken !!!"
                context = {'message': msg}
                return render(request, "signup.html", context)       
            elif SignUpRequests.objects.filter(email=request.POST['email']).exists() or User.objects.filter(email=request.POST['email']).exists():
                msg = "email already taken !!!"
                context = {'message': msg}
                return render(request, "signup.html", context)  
            else:       
                SignUpRequests.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], username=request.POST['username'], adress=request.POST['adress'], number_phone=request.POST['number_phone'], email=request.POST['email'], bank_name=request.POST['bank_name'], bank_account=request.POST['bank_account'], password=request.POST['password1'], front_identity_card=request.FILES['front_identity_card'], back_identity_card=request.FILES['back_identity_card'], date_of_request=date.today())
                return redirect('/')
        else:
            msg = "password doesn't match !!!"
            context = {'message': msg}
            return render(request, "signup.html", context)       
    else:
        return render(request, "signup.html")

def ResetPassword(request):  
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'])
        except User.DoesNotExist:
            user = None 
        if user is not None:     
            sender_email = User.objects.get(is_superuser=True).email
            receiver_email = user.email
            password = "Replace_the_password_of_your_Gmai_here"
            message = MIMEMultipart("alternative")
            message["Subject"] = "Reset Password Request"
            message["From"] = sender_email
            message["To"] = receiver_email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_mail = """<html>
                             <body>
                              <p>Hello {},<br><br>
                               We received a request to reset the password for your account for this email address. To do that, click the link below.<br><br>
                               <a href="http://localhost:8000/newpassword/{}/{}">http://localhost:8000/newpassword/{}/{}</a><br><br> 
                               If you did not make this request, you can simply ignore this email.<br><br>
                               Sincerely,<br>
                               Nkobo Brice
                              </p>
                             </body>
                            </html>
                         """.format(user.username, uid, token, uid, token)
            part = MIMEText(reset_mail, "html")
            message.attach(part)      
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string()) 
            return redirect('/resetpasswordcheckinbox')
        elif SignUpRequests.objects.filter(email=request.POST['email']).exists() == True:
            msg = "Your account must be approved first"
            context = {'message': msg}
            return render(request, "resetpassword.html", context)                
        else:
            msg = "There is no user with this email !!!"
            context = {'message': msg}
            return render(request, "resetpassword.html", context)    
    else:        
        return render(request, "resetpassword.html") 

def CkeckYourInbox(request):
    return render(request, "resetpasswordcheckinbox.html")

def ChangePassword(request, uid, token):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(id=urlsafe_base64_decode(uid).decode())
            except User.DoesNotExist:
                user = None    
            if user is not None:
                user.set_password(request.POST['password1'])
                user.save()
                return render(request, "resetpasswordsuccess.html")
            else:
                return redirect('/')  
        else:
            return redirect('/')          
    else:    
        return render(request, "changepassword.html")

def AdminDashboard(request):
    if request.method == 'POST':
        List1 = SignUpRequests.objects.all() 
        for r in List1:    
            if 'approve_account'+str(r.username) in request.POST:
                newinv = SignUpRequests.objects.get(username=r.username)
                newinvemail = newinv.email
                newinvusername = newinv.username
                if User.objects.filter(username=newinv.username).exists() == False:
                    User.objects.create_user(username=newinv.username, password=newinv.password, email=newinv.email, is_superuser=False)
                    ApprovedSignUpRequests.objects.create(first_name=newinv.first_name, last_name=newinv.last_name, username=newinv.username, adress=newinv.adress, number_phone=newinv.number_phone, email=newinv.email, bank_name=newinv.bank_name, bank_account=newinv.bank_account, password=make_password(newinv.password), front_identity_card=newinv.front_identity_card, back_identity_card=newinv.back_identity_card)
                    SignUpRequests.objects.filter(username=newinv.username).delete()
                    sender_email = User.objects.get(is_superuser=True).email
                    receiver_email = newinvemail
                    password = "Replace_the_password_of_your_Gmai_here"
                    message = MIMEMultipart("alternative")
                    message["Subject"] = "Account Request Approval"
                    message["From"] = sender_email
                    message["To"] = receiver_email
                    activation_mail = """<html>
                                          <body>
                                           <p>Hello {},<br><br>
                                            We received a request to activate your account. Congratulations, your request has been approved and you have now access to it.<br><br>
                                            <a href="http://localhost:8000">http://localhost:8000</a><br><br> 
                                            You are most welcome to join us in our journey and as a new investor, we invite you to invest your money and gain more using our platform InvestionToday and don't hesitate to contact us for more detailed information or any kind of assistance.<br><br>
                                            Sincerely,<br>
                                            InvestingToday
                                           </p>
                                          </body>
                                         </html>
                                      """.format(newinvusername)
                    part = MIMEText(activation_mail, "html")
                    message.attach(part)      
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message.as_string())
                    return redirect('/admindashboard')
            elif 'view_account'+str(r.username) in request.POST:
                AD = SignUpRequests.objects.get(username=r.username)
                context = {'ad': AD}
                return render(request, "adminaccountdetails.html", context)                
            elif 'cancel_account'+str(r.username) in request.POST:         
                SignUpRequests.objects.filter(username=r.username).delete()
                return redirect('/admindashboard')   
        List2 = InvestmentRequests.objects.all()
        for r in List2:
            if 'approve_investment'+str(r.id) in request.POST:
                newinv = InvestmentRequests.objects.get(id=r.id)
                ApprovedInvestmentRequests.objects.create(username=newinv.username, amount_to_invest=newinv.amount_to_invest, amount_to_get=newinv.amount_to_get, interest=newinv.interest, date_of_investment=newinv.date_of_request, date_of_payment=newinv.date_of_payment, status='in progress')
                InvestmentRequests.objects.filter(id=newinv.id).delete()
                sender_email = User.objects.get(is_superuser=True).email
                receiver_email = User.objects.get(username=newinv.username).email
                password = "Replace_the_password_of_your_Gmai_here"
                message = MIMEMultipart("alternative")
                message["Subject"] = "Investment Request Approval"
                message["From"] = sender_email
                message["To"] = receiver_email
                mail = """<html>
                           <body>
                            <p>Hello {},<br><br>
                             We received a request to invest your money. Congratulations, your request has been approved.<br><br>
                             These are the details of your investment :<br><br>
                             Amount invested : {} $<br>
                             Interest : {} $<br>
                             Date of investment : {}<br>
                             Date of payment : {}<br><br>
                             Sincerely,<br>
                             InvestingToday
                            </p>
                           </body>
                          </html>
                       """.format(newinv.username, newinv.amount_to_invest, newinv.interest, newinv.date_of_request, newinv.date_of_payment)
                part = MIMEText(mail, "html")
                message.attach(part)      
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                if TopInvestors.objects.filter(username=r.username).exists():
                    last_amount = TopInvestors.objects.get(username=r.username).amount_invested
                    last_profit = TopInvestors.objects.get(username=r.username).net_profit
                    TopInvestors.objects.filter(username=r.username).update(amount_invested=round(last_amount+newinv.amount_to_invest,2), net_profit=round(last_profit+newinv.interest,2))    
                else:
                    TopInvestors.objects.create(username=r.username, amount_invested=newinv.amount_to_invest, net_profit=newinv.interest)
                return redirect('/admindashboard')
            elif 'cancel_investment'+str(r.id) in request.POST:         
                InvestmentRequests.objects.filter(id=r.id).delete()
                return redirect('/admindashboard')           
        List3 = ApprovedInvestmentRequests.objects.all()
        for r in List3:
            if 'approve_payment'+str(r.id) in request.POST:
                newpay = ApprovedInvestmentRequests.objects.get(id=r.id)
                PaymentCompleted.objects.create(username=newpay.username, amount_paid=newpay.amount_to_get, interest_paid=newpay.interest, date_of_payment=date.today())
                ApprovedInvestmentRequests.objects.filter(id=r.id).update(status='done')
                sender_email = User.objects.get(is_superuser=True).email
                receiver_email = User.objects.get(username=newpay.username).email
                password = "Replace_the_password_of_your_Gmai_here"
                message = MIMEMultipart("alternative")
                message["Subject"] = "Payment"
                message["From"] = sender_email
                message["To"] = receiver_email
                mail = """<html>
                           <body>
                            <p>Hello {},<br><br>
                             The payment for your investment which has the details below has been done.<br><br>
                             Amount invested : {} $<br>
                             Interest : {} $<br>
                             Date of investment : {}<br>
                             Date of payment : {}<br><br>
                             We hope sincerly that our collaboration will continue.<br>
                             InvestingToday
                            </p>
                           </body>
                          </html>
                       """.format(newpay.username, newpay.amount_to_invest, newpay.interest, newpay.date_of_investment, date.today())
                part = MIMEText(mail, "html")
                message.attach(part)      
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                return redirect('/admindashboard')
    else: 
        TOTAL = ApprovedSignUpRequests.objects.count() 
        if ApprovedInvestmentRequests.objects.count() != 0: 
            ALL_AMOUNT_INVESTED = round(ApprovedInvestmentRequests.objects.aggregate(sum=Sum('amount_to_invest'))['sum'],2)
        else:
            ALL_AMOUNT_INVESTED = 0
        if PaymentCompleted.objects.count() != 0: 
            ALL_INTEREST_PAID = round(PaymentCompleted.objects.aggregate(sum=Sum('interest_paid'))['sum'],2)
        else:
            ALL_INTEREST_PAID = 0
        if ApprovedInvestmentRequests.objects.filter(status='in progress').count() != 0: 
            ACTIVE_INVESTED_AMOUNT = round(ApprovedInvestmentRequests.objects.filter(status='in progress').aggregate(sum=Sum('amount_to_invest'))['sum'],2)
        else:
            ACTIVE_INVESTED_AMOUNT = 0
        if ApprovedInvestmentRequests.objects.filter(date_of_payment__lt=date.today(), status='in progress').count() != 0: 
            TOTAL_INTEREST_TO_PAY = round(ApprovedInvestmentRequests.objects.filter(date_of_payment__lt=date.today(), status='in progress').aggregate(sum=Sum('interest'))['sum'],2)
        else:
            TOTAL_INTEREST_TO_PAY = 0
        if InvestmentRequests.objects.count() != 0: 
            PENDING_AMOUNT = round(InvestmentRequests.objects.aggregate(sum=Sum('amount_to_invest'))['sum'],2)
        else:
            PENDING_AMOUNT = 0
        allaccreq = SignUpRequests.objects.count()
        if allaccreq >= 5: 
            SUR = SignUpRequests.objects.all().order_by('id')[:5] 
        else:
            SUR = SignUpRequests.objects.all()  
        allinvreq = InvestmentRequests.objects.count() 
        if allinvreq >= 5: 
            IR = InvestmentRequests.objects.all().order_by('id')[:5] 
        else:
            IR = InvestmentRequests.objects.all()  
        topinv = TopInvestors.objects.count() 
        if topinv >= 5: 
            TOP = TopInvestors.objects.all().order_by('amount_invested').reverse()[:5] 
        else:
            TOP = TopInvestors.objects.all().order_by('amount_invested').reverse()  
        allpp = ApprovedInvestmentRequests.objects.filter(date_of_payment__lt=date.today(), status='in progress').count()
        DL = []
        if allpp >= 5: 
            PP = ApprovedInvestmentRequests.objects.filter(date_of_payment__lt=date.today(), status='in progress').order_by('date_of_payment')[:5]
            for p in PP:
                DL.append(str(date.today() - p.date_of_payment).split(',')[0])
        else:
            PP = ApprovedInvestmentRequests.objects.filter(date_of_payment__lt=date.today(), status='in progress').order_by('date_of_payment')                                  
            for p in PP:
                DL.append(str(date.today() - p.date_of_payment).split(',')[0])   
        context = {'total': TOTAL, 'all_amount_invested': ALL_AMOUNT_INVESTED, 'all_interest_paid': ALL_INTEREST_PAID, 'active_invested_amount': ACTIVE_INVESTED_AMOUNT, 'total_interest_to_pay': TOTAL_INTEREST_TO_PAY, 'pending_amount': PENDING_AMOUNT, 'sur': SUR, 'ir': IR, 'top': TOP, 'pp': PP, 'dl': DL}
        return render(request, "admindashboard.html", context)       

def TotalAmountInvested(request):
    if ApprovedInvestmentRequests.objects.count() != 0:
        allinvestments = TopInvestors.objects.all().order_by('amount_invested')
        context = {'all': allinvestments}
        return render(request, "totalamountinvested.html", context)
    else:    
        return render(request, "totalamountinvested.html")

def TotalInterestPaid(request):
    if PaymentCompleted.objects.count() != 0:
        allinterestpaid = PaymentCompleted.objects.all()
        context = {'all': allinterestpaid}
        return render(request, "totalinterestpaid.html", context)
    else:    
        return render(request, "totalinterestpaid.html")

def ActiveInvestedAmount(request):
    if ApprovedInvestmentRequests.objects.filter(status='in progress').count() != 0:
        allactiveamount = ApprovedInvestmentRequests.objects.filter(status='in progress')
        context = {'all': allactiveamount}
        return render(request, "activeinvestedamount.html", context)
    else:    
        return render(request, "activeinvestedamount.html")

def TotalInterestToPay(request):
    if ApprovedInvestmentRequests.objects.filter(date_of_payment__lt=date.today(), status='in progress').count() != 0:
        allinteresttopay = ApprovedInvestmentRequests.objects.filter(date_of_payment__lt=date.today(), status='in progress')
        DL = []
        for i in allinteresttopay:
            DL.append(str(date.today() - i.date_of_payment).split(',')[0])
        context = {'all': allinteresttopay, 'dl': DL}
        return render(request, "totalinteresttopay.html", context)
    else:    
        return render(request, "totalinteresttopay.html")

def PendingAmount(request):
    if InvestmentRequests.objects.count() != 0:
        pendingamount = InvestmentRequests.objects.all()
        context = {'all': pendingamount}
        return render(request, "pendingamount.html", context)
    else:    
        return render(request, "pendingamount.html")

def AccountActivationRequests(request):
    if request.method == 'POST':
        List1 = SignUpRequests.objects.all() 
        for r in List1:    
            if 'approve_account'+str(r.username) in request.POST:
                newinv = SignUpRequests.objects.get(username=r.username)
                newinvemail = newinv.email
                newinvusername = newinv.username
                if User.objects.filter(username=newinv.username).exists() == False:
                    User.objects.create_user(username=newinv.username, password=newinv.password, email=newinv.email, is_superuser=False)
                    ApprovedSignUpRequests.objects.create(first_name=newinv.first_name, last_name=newinv.last_name, username=newinv.username, adress=newinv.adress, number_phone=newinv.number_phone, email=newinv.email, bank_name=newinv.bank_name, bank_account=newinv.bank_account, front_identity_card=newinv.front_identity_card, back_identity_card=newinv.back_identity_card)
                    SignUpRequests.objects.filter(username=newinv.username).delete()
                    sender_email = User.objects.get(is_superuser=True).email
                    receiver_email = newinvemail
                    password = "Replace_the_password_of_your_Gmai_here"
                    message = MIMEMultipart("alternative")
                    message["Subject"] = "Account Request Approval"
                    message["From"] = sender_email
                    message["To"] = receiver_email
                    activation_mail = """<html>
                                          <body>
                                           <p>Hello {},<br><br>
                                            We received a request to activate your account. Congratulations, your request has been approved and you have now access to it.<br><br>
                                            <a href="http://localhost:8000">http://localhost:8000</a><br><br> 
                                            You are most welcome to join us in our journey and as a new investor, we invite you to invest your money and gain more using our platform InvestionToday and don't hesitate to contact us for more detailed information or any kind of assistance.<br><br>
                                            Sincerely,<br>
                                            InvestingToday
                                           </p>
                                          </body>
                                         </html>
                                      """.format(newinvusername)
                    part = MIMEText(activation_mail, "html")
                    message.attach(part)      
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message.as_string())
                    SUR = SignUpRequests.objects.all()
                    context = {'sur': SUR}
                    return render(request, "adminaccountrequests.html", context)
            elif 'view_account'+str(r.username) in request.POST:
                AD = SignUpRequests.objects.get(username=r.username)
                context = {'ad': AD}
                return render(request, "adminaccountdetails.html", context)
            elif 'cancel_account'+str(r.username) in request.POST:   
                SignUpRequests.objects.filter(username=r.username).delete()      
                SUR = SignUpRequests.objects.all()
                context = {'sur': SUR}
                return render(request, "adminaccountrequests.html", context)
    else:             
        SUR = SignUpRequests.objects.all()
        context = {'sur': SUR}
        return render(request, "adminaccountrequests.html", context)   

def AdminChangePassword(request):
    if request.method == 'POST':
        admins = User.objects.filter(is_superuser=True)
        for adm in admins:
            if adm.username == request.POST['username']:        
                if adm.check_password(request.POST['password1']):
                    if request.POST['password2'] == request.POST['password3']:
                        adm.set_password(request.POST['password2'])
                        adm.save()
                        msg = "Admin password has been reset successfully"
                        context = {'message': msg}
                        return render(request, "adminchangepassword.html", context)
                    else:
                        if adm == admins[len(admins)-1]:
                            msg = "Password doesn't match !!!"
                            context = {'message': msg}
                            return render(request, "adminchangepassword.html", context)
                else:  
                    if adm == admins[len(admins)-1]:      
                        msg = "Old password is incorrect !!!"
                        context = {'message': msg}
                        return render(request, "adminchangepassword.html", context)  
            else:
                if adm == admins[len(admins)-1]:
                    msg = "There is no admin with this name !!!"
                    context = {'message': msg}
                    return render(request, "adminchangepassword.html", context)  
    else:
        return render(request, "adminchangepassword.html")         

def AdminList(request):
    admins = User.objects.filter(is_superuser=True)
    context = {'adm': admins}
    return render(request, "adminlist.html", context)

def AdminAddAdmin(request):
    if request.method == 'POST':   
        if User.objects.filter(username=request.POST['username']).exists():
            msg = "Username already taken !!!"
            context = {'message': msg}
            return render(request, "adminaddadmin.html", context)
        elif User.objects.filter(email=request.POST['email']).exists(): 
            msg = "Email already taken !!!"
            context = {'message': msg}
            return render(request, "adminaddadmin.html", context)    
        elif request.POST['password1'] != request.POST['password2']:
            msg = "Password doesn't match !!!"
            context = {'message': msg}
            return render(request, "adminaddadmin.html", context)
        else:
            User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password1'], is_superuser=True)
            msg = "Admin has been added successfully"
            context = {'message': msg}
            return render(request, "adminaddadmin.html", context)
    else:
        return render(request, "adminaddadmin.html")    

def AdminInvestorList(request):
    if request.method == 'POST':
        List = ApprovedSignUpRequests.objects.all()
        for l in List: 
            if 'viewall'+str(l.username) in request.POST:
                inv = ApprovedSignUpRequests.objects.get(username=l.username) 
                context = {'investor': inv}
                return render(request, 'admininvestordetails.html', context)
    else:
        investors = ApprovedSignUpRequests.objects.all()
        context = {'inv': investors}
        return render(request, "admininvestorlist.html", context)

def AdminAddInvestor(request):
    if request.method == 'POST':
        if ApprovedSignUpRequests.objects.filter(username=request.POST['username']).exists() or User.objects.filter(username=request.POST['username']).exists():
            msg = "Username already taken !!!"
            context = {'message': msg}
            return render(request, "adminaddinvestor.html", context)
        elif ApprovedSignUpRequests.objects.filter(number_phone=request.POST['number_phone']).exists():
            msg = "Number phone already taken !!!"
            context = {'message': msg}
            return render(request, "adminaddinvestor.html", context)  
        elif ApprovedSignUpRequests.objects.filter(email=request.POST['email']).exists() or User.objects.filter(email=request.POST['email']).exists():
            msg = "Email already taken !!!"
            context = {'message': msg}
            return render(request, "adminaddinvestor.html", context)  
        elif ApprovedSignUpRequests.objects.filter(bank_account=request.POST['bank_account']).exists():
            msg = "Bank account already taken !!!"
            context = {'message': msg}
            return render(request, "adminaddinvestor.html", context)   
        else:
            ApprovedSignUpRequests.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], username=request.POST['username'], adress=request.POST['adress'], number_phone=request.POST['number_phone'], email=request.POST['email'], bank_name=request.POST['bank_name'], bank_account=request.POST['bank_account'], front_identity_card=request.POST['front_identity_card'], back_identity_card=request.POST['back_identity_card'])
            User.objects.create_user(username=request.POST['username'], email=request.POST['email'], is_superuser=False)         
            new_investor = User.objects.get(username=request.POST['username'])
            sender_email = User.objects.get(is_superuser=True).email
            receiver_email = new_investor.email
            password = "Replace_the_password_of_your_Gmai_here"
            message = MIMEMultipart("alternative")
            message["Subject"] = "Approved Account"
            message["From"] = sender_email
            message["To"] = receiver_email
            uid = urlsafe_base64_encode(force_bytes(new_investor.pk))
            token = default_token_generator.make_token(new_investor)
            mail = """<html>
                       <body>
                        <p>Hello {} {},<br><br>
                         An account has been created for you. Click the link below to create your password.<br><br>
                         <a href="http://localhost:8000/newpassword/{}/{}">http://localhost:8000/newpassword/{}/{}</a><br><br>
                         You are most welcome to join us in our journey and as a new investor, we invite you to invest your money and gain more using our platform InvestionToday and don't hesitate to contact us for more detailed information or any kind of assistance.<br><br>
                         Sincerely,<br>
                         InvestingToday
                        </p>
                       </body>
                      </html>
                   """.format(request.POST['first_name'], request.POST['last_name'], uid, token, uid, token, uid, token)
            part = MIMEText(mail, "html")
            message.attach(part)      
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            msg = "Investor has been added successfully and an email has been sent to him to create his password"
            context = {'message': msg}
            return render(request, "adminaddinvestor.html", context) 
    else:
        return render(request, "adminaddinvestor.html")

def AdminActiveInvestList(request):
    if ApprovedInvestmentRequests.objects.count() != 0:
        AIL = ApprovedInvestmentRequests.objects.all()
        context = {'ail': AIL}
        return render(request, "adminactiveinvestlist.html", context)
    else:
        return render(request, "adminactiveinvestlist.html")

def AdminPendingList(request):
    if request.method == 'POST':
        List = InvestmentRequests.objects.all()
        for r in List:
            if 'approve_investment'+str(r.id) in request.POST:
                newinv = InvestmentRequests.objects.get(id=r.id)
                ApprovedInvestmentRequests.objects.create(username=newinv.username, amount_to_invest=newinv.amount_to_invest, amount_to_get=newinv.amount_to_get, interest=newinv.interest, date_of_investment=newinv.date_of_request, date_of_payment=newinv.date_of_payment, status='in progress')
                InvestmentRequests.objects.filter(id=newinv.id).delete()
                sender_email = User.objects.get(is_superuser=True).email
                receiver_email = User.objects.get(username=newinv.username).email
                password = "Replace_the_password_of_your_Gmai_here"
                message = MIMEMultipart("alternative")
                message["Subject"] = "Investment request approval"
                message["From"] = sender_email
                message["To"] = receiver_email
                mail = """<html>
                           <body>
                            <p>Hello {},<br><br>
                             We received a request to invest your money. Congratulations, your request has been approved.<br><br>
                             These are the details of your investment :<br><br>
                             Amount invested : {} $<br>
                             Interest : {} $<br>
                             Date of investment : {}<br>
                             Date of payment : {}<br><br>
                             Sincerely,<br>
                             InvestingToday
                            </p>
                           </body>
                          </html>
                       """.format(newinv.username, newinv.amount_to_invest, newinv.interest, newinv.date_of_request, newinv.date_of_payment)
                part = MIMEText(mail, "html")
                message.attach(part)      
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                if TopInvestors.objects.filter(username=r.username).exists():
                    last_amount = TopInvestors.objects.get(username=r.username).amount_invested
                    last_profit = TopInvestors.objects.get(username=r.username).net_profit
                    TopInvestors.objects.filter(username=r.username).update(amount_invested=round(last_amount+newinv.amount_to_invest,2), net_profit=round(last_profit+newinv.interest,2))    
                else:
                    TopInvestors.objects.create(username=r.username, amount_invested=newinv.amount_to_invest, net_profit=newinv.interest)                    
                return redirect('/adminpendinglist')
            elif 'cancel_investment'+str(r.id) in request.POST:         
                InvestmentRequests.objects.filter(id=r.id).delete()
                return redirect('/adminpendinglist') 
    else:    
        if InvestmentRequests.objects.count != 0:
            IR = InvestmentRequests.objects.all()
            context = {'ir': IR}  
            return render(request, "adminpendinglist.html", context)
        else:
            return render(request, "adminpendinglist.html")   

def AdminAddInvestment(request):
    if request.method == 'POST':
        if ApprovedSignUpRequests.objects.filter(username=request.POST['username']).exists():
            IP = InvestmentManagement.objects.last()
            amount_to_invest = request.POST['amount_to_invest']
            amount_to_get = round(float(request.POST['amount_to_invest']) + ((IP.profit/100)*float(request.POST['amount_to_invest'])),2)
            interest = round((IP.profit/100)*float(request.POST['amount_to_invest']),2)
            date_of_payment = date.today() + timedelta(IP.duration)
            ApprovedInvestmentRequests.objects.create(username=request.POST['username'], amount_to_invest=amount_to_invest, amount_to_get=amount_to_get, interest=interest, date_of_investment=date.today(), date_of_payment=date_of_payment, status='in progress')
            investor = User.objects.get(username=request.POST['username'])
            sender_email = User.objects.get(is_superuser=True).email
            receiver_email = investor.email
            password = "Replace_the_password_of_your_Gmai_here"
            message = MIMEMultipart("alternative")
            message["Subject"] = "Added Investment"
            message["From"] = sender_email
            message["To"] = receiver_email
            mail = """<html>
                       <body>
                        <p>Hello {},<br><br>
                         Your investment has been added successfully.<br><br>
                         These are the details of your investment :<br><br>
                         Amount invested : {} $<br>
                         Interest : {} $<br>
                         Date of investment : {}<br>
                         Date of payment : {}<br><br>
                         Sincerely,<br>
                         InvestingToday
                        </p>
                       </body>
                      </html>
                   """.format(investor.username, amount_to_invest, interest, date.today(), date_of_payment)
            part = MIMEText(mail, "html")
            message.attach(part)      
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            if TopInvestors.objects.filter(username=request.POST['username']).exists():
                last_amount = TopInvestors.objects.get(username=request.POST['username']).amount_invested
                last_profit = TopInvestors.objects.get(username=request.POST['username']).net_profit
                TopInvestors.objects.filter(username=request.POST['username']).update(amount_invested=round(last_amount+float(amount_to_invest),2), net_profit=round(last_profit+interest,2))    
            else:
                TopInvestors.objects.create(username=request.POST['username'], amount_invested=float(amount_to_invest), net_profit=interest)
            IP = InvestmentManagement.objects.last()
            msg = "New investment has been added successfully and an email has been sent to notify the new investor"
            context = {'ip': IP, 'success': msg}
            return render(request, "adminaddinvestment.html", context) 
    else:
        if InvestmentManagement.objects.count() != 0:
            IP = InvestmentManagement.objects.last()
            context = {'ip': IP}
            return render(request, "adminaddinvestment.html", context)
        else:
            msg = "Investment details are not yet available, you should provide them first !!!"
            context = {'message': msg}
            return render(request, "adminaddinvestment.html", context)

def AdminUpcomingPayment(request):
    UP = ApprovedInvestmentRequests.objects.filter(status='in progress').all()
    context = {'up': UP}
    return render(request, "adminupcomingpayment.html", context)

def AdminPendingPayment(request):
    if request.method == 'POST':
        List = ApprovedInvestmentRequests.objects.all()
        for r in List:
            if 'approve_payment'+str(r.id) in request.POST:
                newpay = ApprovedInvestmentRequests.objects.get(id=r.id)
                PaymentCompleted.objects.create(username=newpay.username, amount_paid=newpay.amount_to_get, date_of_payment=date.today())
                ApprovedInvestmentRequests.objects.filter(id=r.id).update(status='done')
                sender_email = User.objects.get(is_superuser=True).email
                receiver_email = User.objects.get(username=newpay.username).email
                password = "Replace_the_password_of_your_Gmai_here"
                message = MIMEMultipart("alternative")
                message["Subject"] = "Payment"
                message["From"] = sender_email
                message["To"] = receiver_email
                mail = """<html>
                           <body>
                            <p>Hello {},<br><br>
                             The payment for your investment which has the details below has been done.<br><br>
                             Amount invested : {} $<br>
                             Interest : {} $<br>
                             Date of investment : {}<br>
                             Date of payment : {}<br><br>
                             We hope sincerly that our collaboration will continue.<br>
                             InvestingToday
                            </p>
                           </body>
                          </html>
                       """.format(newpay.username, newpay.amount_to_invest, newpay.interest, newpay.date_of_investment, date.today())
                part = MIMEText(mail, "html")
                message.attach(part)      
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())  
                return redirect('/adminpendingpayment')
    else:
        if ApprovedInvestmentRequests.objects.filter(date_of_payment__lt=date.today(), status='in progress').count() != 0:
            PP = ApprovedInvestmentRequests.objects.filter(date_of_payment__lt=date.today(), status='in progress')
            DL = []
            for p in PP:
                DL.append(str(date.today() - p.date_of_payment).split(',')[0])
            context = {'pp': PP, 'dl': DL}      
            return render(request, "adminpendingpayment.html", context)
        else:
            return render(request, "adminpendingpayment.html")    

def AdminAlreadyPaid(request):
    if PaymentCompleted.objects.count() != 0:
        AP = PaymentCompleted.objects.all().order_by('id')
        context = {'ap': AP} 
        return render(request, "adminalreadypaid.html", context) 
    else:
        return render(request, "adminalreadypaid.html")       

def AdminInterestRateManagement(request):
    if request.method == 'POST':
        msg = "It's done"
        context = {'message': msg}
        if InvestmentManagement.objects.count() == 0:
            InvestmentManagement.objects.create(profit=request.POST['profit'], duration=request.POST['duration'])
            return render(request, "adminintersetmanagement.html", context) 
        else:
            InvestmentManagement.objects.update(profit=request.POST['profit'], duration=request.POST['duration'])      
            return render(request, "adminintersetmanagement.html", context) 
    else:
        return render(request, "adminintersetmanagement.html")

def AdminSendEmails(request):
    if request.method == 'POST':
        Lst = User.objects.filter(is_superuser=False)
        ListOfEmails = []
        for inv in Lst: 
            if 'box'+str(inv.username) in request.POST:
                ListOfEmails.append(inv.email) 
        if ListOfEmails:
            sender_email = User.objects.get(is_superuser=True).email
            receiver_email = ', '.join(ListOfEmails)
            password = "Replace_the_password_of_your_Gmai_here"
            message = MIMEMultipart("alternative")
            message["Subject"] = request.POST['subject']
            message["From"] = sender_email
            message["To"] = receiver_email 
            mail = request.POST['mail']
            msg_email = MIMEText(mail, "plain")
            message.attach(msg_email)      
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string()) 
            msg_success = "Mail has been sent successfully"
            List = ApprovedSignUpRequests.objects.all()  
            context = {'list': List, 'message': msg_success} 
            return render(request, "adminsendemails.html", context)                 
        else:    
            List = ApprovedSignUpRequests.objects.all() 
            context = {'list': List} 
            return render(request, "adminsendemails.html", context)     
    else:
        List = ApprovedSignUpRequests.objects.all()
        context = {'list': List} 
        return render(request, "adminsendemails.html", context)       

def AdminTerms(request):
    return render(request, "adminterms.html")

def Account(request, account):
    if request.method == 'POST':
        if 'invest' in request.POST:
            investor_username = urlsafe_base64_decode(account).decode()
            inv = ApprovedSignUpRequests.objects.get(username=investor_username)
            if InvestmentManagement.objects.last() == None:
                context = {'investor': inv}
            else:
                investmentmanagement = InvestmentManagement.objects.last()
                context = {'investor': inv, 'im': investmentmanagement} 
            return render(request, 'invest.html', context)    
        elif 'edit' in request.POST:
            return render(request, 'edit.html') 
        elif 'save' in request.POST:
            investor_username = urlsafe_base64_decode(account).decode()
            if request.POST['number_phone'] != '':
                ApprovedSignUpRequests.objects.filter(username=investor_username).update(number_phone=request.POST['number_phone'])
            if request.POST['adress'] != '':
                ApprovedSignUpRequests.objects.filter(username=investor_username).update(adress=request.POST['adress'])
            if request.POST['email'] != '':
                ApprovedSignUpRequests.objects.filter(username=investor_username).update(email=request.POST['email'])
                User.objects.filter(username=investor_username).update(email=request.POST['email'])
            if request.POST['bank_name'] != '':
                ApprovedSignUpRequests.objects.filter(username=investor_username).update(bank_name=request.POST['bank_name'])
            if request.POST['bank_account'] != '':
                ApprovedSignUpRequests.objects.filter(username=investor_username).update(bank_account=request.POST['bank_account'])
            return render(request, 'edit.html') 
        elif 'pay' in request.POST:
            if InvestmentManagement.objects.count() != 0:
                investor_username = urlsafe_base64_decode(account).decode()
                inv = ApprovedSignUpRequests.objects.get(username=investor_username) 
                IP = InvestmentManagement.objects.last()
                amount_to_invest = request.POST['amount_to_invest']
                amount_to_get = round(float(request.POST['amount_to_invest']) + ((IP.profit/100)*float(request.POST['amount_to_invest'])),2)
                interest = round((IP.profit/100)*float(request.POST['amount_to_invest']),2)
                date_of_request = date.today()
                date_of_payment = date.today() + timedelta(IP.duration)
                InvestmentRequests.objects.create(username=inv.username, amount_to_invest=request.POST['amount_to_invest'], amount_to_get=amount_to_get, interest=interest, date_of_request=date_of_request, date_of_payment=date_of_payment) 
                context = {'investor': inv, 'amount': amount_to_invest}    
                return render(request, 'pay.html', context) 
            else: 
                investor_username = urlsafe_base64_decode(account).decode()
                inv = ApprovedSignUpRequests.objects.get(username=investor_username) 
                msg = "investment details are not yet available, try again later"
                context = {'investor': inv, 'message': msg} 
                return render(request, 'invest.html', context)           
    else:
        investor_username = urlsafe_base64_decode(account).decode()
        inv = ApprovedSignUpRequests.objects.get(username=investor_username)
        amount_invested = ApprovedInvestmentRequests.objects.filter(username=inv.username).aggregate(sum=Sum('amount_to_invest'))['sum']
        investment_in_progress = ApprovedInvestmentRequests.objects.filter(username=inv.username, status='in progress').aggregate(sum=Sum('amount_to_invest'))['sum'] 
        net_profit = PaymentCompleted.objects.filter(username=inv.username).aggregate(sum=Sum('interest_paid'))['sum']
        if amount_invested == None:
            amount_invested =0
            L1 = ['$']
        elif amount_invested > 1000000:
            amount_invested = round(amount_invested/1000000,2)
            L1 = ['M']
        elif amount_invested > 1000:
            amount_invested = round(amount_invested/1000,2)
            L1 = ['k']
        else:
            amount_invested = round(amount_invested,2)
            L1 = ['$']
        if investment_in_progress == None:
            investment_in_progress = 0
            L2 = ['$']
        elif investment_in_progress > 1000000:
            investment_in_progress = round(investment_in_progress/1000000,2)
            L2 = ['M']
        elif investment_in_progress > 1000:
            investment_in_progress = round(investment_in_progress/1000,2)
            L2 = ['k']
        else:
            investment_in_progress = round(investment_in_progress,2)  
            L2 = ['$']
        if net_profit == None:
            net_profit =0
            L3 = ['$']
        elif net_profit > 1000000:
            net_profit = round(net_profit/1000000,2)
            L3 = ['M']
        elif net_profit > 1000:
            net_profit = round(net_profit/1000,2)
            L3 = ['k']
        else:
            net_profit = round(net_profit,2)
            L3 = ['$']                
        context = {'investor': inv, 'amount_invested': amount_invested, 'investment_in_progress': investment_in_progress, 'net_profit': net_profit, 'l1': L1, 'l2': L2, 'l3': L3}
        return render(request, 'account.html', context)
        
