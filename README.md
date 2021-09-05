# InvestingToday_Web_App
InvestingToday is a web application that I developed for money online investment in return of some interests. This application was developed using Django Web framework and it provides an Admin interface for viewing some key statistics and managing parameters of investments, approving new accounts and  investments requests, adding new Admins and investors manually, paying investors and sending bulk emails to them. Flutterwave is the payment service implemented in this application, it is a fintech company that provides a payment infrastructure for global merchants and payment service providers.
### What do you need to use this application ?
- First of all, install Django and all the necessary libraries (if they are missing). 
```
pip install django
```
```
pip install Pillow
```
- Configure the database in Django's settings file, you can ignore this step if you want to use SQLite3 because it is chosen by default. 
- Open the folder above in Command Prompt (CMD) and commit the initial migration.
```
python manage.py makemigrations
```
```
python manage.py migrate
```
- Create the superuser (Admin) 
```
python manage.py createsuperuser
```
- Run the server and start testing the application.
```
python manage.py runserver
```
- When you make sure that everything works fine, deploy the application on a Web server and start your journey.

Finally, as always, I remain at your entire disposal, just contact me at my personal Gmail hamzataous847@gmail.com if you have any questions or if you need any kind of assistance.
