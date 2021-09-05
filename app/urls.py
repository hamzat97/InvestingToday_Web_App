from django.urls import path
from . import views

urlpatterns = [  
  path('', views.Home),
  path('signin', views.SignIn),
  path('signup', views.SignUp),
  path('resetpassword', views.ResetPassword),
  path('resetpasswordcheckinbox', views.CkeckYourInbox),
  path('newpassword/<uid>/<token>', views.ChangePassword),
  path('admindashboard', views.AdminDashboard),
  path('totalamountinvested', views.TotalAmountInvested),
  path('totalinterestpaid', views.TotalInterestPaid),
  path('activeinvestedamount', views.ActiveInvestedAmount),
  path('totalinteresttopay', views.TotalInterestToPay),
  path('pendingamount', views.PendingAmount),
  path('adminaccountrequests', views.AccountActivationRequests),
  path('adminchangepassword', views.AdminChangePassword),
  path('adminlist', views.AdminList),
  path('adminaddadmin', views.AdminAddAdmin),
  path('admininvestorlist', views.AdminInvestorList),
  path('adminaddinvestor', views.AdminAddInvestor),
  path('adminactiveinvestlist', views.AdminActiveInvestList),
  path('adminpendinglist', views.AdminPendingList),
  path('adminaddinvestment', views.AdminAddInvestment),
  path('adminupcomingpayment', views.AdminUpcomingPayment),
  path('adminpendingpayment', views.AdminPendingPayment),
  path('adminalreadypaid', views.AdminAlreadyPaid),
  path('admininterestmanagement', views.AdminInterestRateManagement),
  path('adminsendemails', views.AdminSendEmails),
  path('adminterms', views.AdminTerms),
  path('investingtoday/<account>', views.Account)
]