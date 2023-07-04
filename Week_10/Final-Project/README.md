Gionet Vendor  
Video Demo: https://www.youtube.com/watch?v=CDDvZ4ZmHB4  
Description: Inventory Management System

# Overview:
Gionet Vendor is a replica of an inhouse Inventory Management System.
The main purpose of this creation is to centralize and ease small vendor/business owners having to manually track client's subscription status on paper/excelsheet.

```
This software has the functions as below:
1. Inserting new clients to the list
2. Displaying whole client list
3. Inserting client's order
4. To monitor and track client's order status
```

Below are the detailed technical aspects of the functionality:

### Register _navbar_ - Account Registration
```
- Register an account to login and use the website
```

### Login _navbar_ - Login
```
- Login with the account credentials that was created from Register
```  

### Gionet Vendor _navbar_ - Dashboard/Home Page
```
- A view of all client's order sorted by days left to expiration on "Expired in" column. (sorted based on ascending order)
- Main purpose of this dashboard is to have a view on which order is expiring so staff's can do the needful (e.g. follow up client on contract renewal, etc.)
```

```
EDIT FUNCTION
- Displays the previous information to edit and update the entry upon submit
```  
  
### Onboarding _navbar_ - Record new clients information
```
- All columns is compulsory to be filled
```
  
### Clients _navbar_ - List of Clients
```
- Displays all client in a list from database
```
  
### Insert _navbar_ - Record new order placed by client
```
- All columns is compulsory to be filled
- S/N (Serial Number) is a unique number generated with Luhn's Algorithm (Algorithm that is used for generating bank credit card numbers)
- Insert and store client's order into the system for tracking
- "Expiration Date" MUST be a future date
- "Client" dropdown list display from client list
```
  
### History _navbar_ - History Logs
```
- Displays the list of all client's order with the User column
- Able to identify who created the entry
```
  
### Account _navbar_ - Account Settings
```
- Displays the account username
- Change password function
```

```
CHANGE PASSWORD
Insert old password, new password and retype new password for correctness
```
  
### Log out _navbar_ Log out user
```
- logs out user and redirect to login page
```