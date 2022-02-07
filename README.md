# Final Project: Agro C.R.M.
---
`Author: Marcos Raimondi`

### Agro Customer Relationship Management Web Application

This is a web application for land owners who are seeking a more efficient way to communicate with their respective tenants. This is not a space for selling, but for information; keeping track key elements of these business relationships.

## Index

1. [Requirements](#requirements)
2. [Description](#description)
3. [File Contents](#file-contents)
4. [Getting Started](#getting-started)
	- [Dependencies](#dependencies)
	- [Executing the app](#executing-the-app)
5. [Screenshots](#screenshots) 
6. [Acknowledgments](#acknowledgments)

## Requirements

I strongly believe this project satisfies all requirements, it is based in Django for the back-end and Javascript for the front-end, it is original since the idea came from real needs I see in the industry moreover I feel it can be a real advantage in the area. With the knowledge acquired in this course I have managed to build an application far more complex than any other project forcing me to read the docs much more than before (a real skill that I started to value). With multiple pages and views, forms, many models (which include defining and overiding some methods), the dilemma of how to manage different types of users, fetching an external api and making all kind of security validations (users credentials, csrf with the fetch library). And of course the app is mobile-responsive.
	

## Description

This project is a Costumer Relationship Management aplication adapted to handle the needs of landlords and their tenants.

Before the specifications, here is my process for Completing the final project:

1. First of all, I started a brainstorming stage looking for some original ideas for web applications, discarding those unsuitable for the project. I was most interested in this CRM idea because of my relation with this field of the agricultural business furthermore the lack of web software around this specific area.

2. Once the project idea had been chosen, I started the app in Django and structured the basics views, which I already knew I would need:
	-Login -Register -Index. Not worrying to much on the design but on the structure.

3. After that I, started to think about the structure of my database, which models should I create, how to differenciate between users, what information to store, etc. Due to some research I decided that authentication should be handled by one model only (the user model) and created another model to distinguish between users (landlord and tenants) creating the tenant profile model, obtaining a higher flexibility. This way I could add fields that where specific to tenants moreover I could create relations (Many-to-many) between this two types of users.

4. My next step was to draw some sketches of how I wanted the app to look like, what pages there should be, etc. 
  The result:
	- login/register page
	- index page for displaying lands
	- a page for each land showing it's details
	- a page for creating and editing the lands (only for landlords)
	- a billing page 
	- a profile page

5. After that I created some model objects with Django's admin interface to start displaying them in the index view with a simple design using bootsrap also worrying more for the actual functionalities and backend than for design.

6. Handled pagination with django's paginator for the backend and bootstrap pagination for the frontend.

7. For displaying each land information and details I used javascript without creating a new page and fetching to a specific route previously coded to receive requests and return a specific land information.

8. For creating a new Land I used django's modelForm, since later for the editing it would come handy for updating existing land objects; this functionality is only available for landlords users so not only tenant users cannot access this page in the frontend, but there are also backend validators. For deleting a land I used javascript fetch library.

9. I created the billing model to handle everything related to billing for each land adding the respective forms and validators.

10. A very important functionality that I wanted my aplication to have was the ability to inform the user of the current weather conditions of a specific land. To accomplish this goal I searched for available online APIS. I came across OpenWeather api that delivers this information to it's users using the latitude and longitude of the location. Link: https://openweathermap.org/api . You can register and get an api key for free. Calling this api with javascript and displaying it the land view was the following step.

11. As a consequence of the need of an api key came the need of environmental variables to protect this sensitive information from getting published in the github repository. The solution for this problem was utilizing django environ library.

12. Following, I started giving style to the templates and making the app more mobile-responsive.

13. Then I created the profile page to display some minimum information as well as a very simple messaging system (created a message model that relates a landlord and a tenant) furthermore I developed the ability for landlords and tenants to create relations between them via messages/requests that can be accepted or rejected. 

14. At this point I only wanted landlords to be able to communicate with tenants and viceversa, requiring the compliance of both to create the relation. This was a key functonality since landlords can only associate their lands to tenant users who are related in this way with their own accounts. 

15. Communication are kept clean by creating messeages that link a landlord user and a tenant user. This is a very elementary communication system that it is not intended to be used as a mailing system, just for simple notifications. For requests/messages you need to know the other users id that he has to share with you via mail or other way; since it is not expected for random users to see which other users are registered.

16. At last I gave the app it's final looks, nice animations to smooth the user experience, made every javascript request csrf compliant and corrected the lasting minor bugs.

When viewing, fetching, creating, deleting lands it was always necessary to check for users credentials (user had to be a landlord to create a land and furthermore to delete, it had to be his land), so that no one can delete, or change other users' lands.


## File Contents

* CRM main directory:
	- views.py: file containing views and api routes for displaying templates and returning information
	- models.py: file defining models
	- urls.py: file containing available urls
	- forms.py: file where Django ModelForms are created from billing and land models and used in views.py

* In the static\crm directory:
	- index.js: for toggling land views and fetching its information in the index template, also handles fetching weather api
	- bills.js: creates listeners to toggle dropdowns in the billing template
	- newLand.js: handles deleting lands in the newLand template
	- profile.js: handles accepting requests, deleting messages in the profile template
	- styles.css: stylesheet for all my custom style
	- jpeg image used for background
	
* In the templates\crm directory:
	- layout.html: contains main structure from which all other templates extend (navigation bar, header)
	- index.html: displays list of all lands
	- land-view.html: land specific information, template included in index template, toggled by the index.js listeners
	- pagination.html: pagination included in index template
	- bills.html: displays list of all bills
	- newLand.html: displays land form and billing form for creating or editing lands.
	- profile: displays profile information
	- login.html: login form
	- register.html: register form
	
* In the templatetags directory:
	- customTags.py: custom django tags used for giving certain style according the billing status

* In the screenshots directory:
	- app screenshots

## Getting Started

### Dependencies

You should find all needed packages and libraries in the requirements.txt file.

To install them run `pip install -r requirements.txt` on your terminal.

Also for using the weather api you have to first register in the page and get an api key. Then go to the views.py file and asign the global variable API_KEY your key.

### Executing the app

Run `python manage.py runserver` if you downloaded the project or visit: https://agro-crm-project.herokuapp.com .

When running the app this is how it is meant to be used:

* Register (register as a landlord using the checkbox)
* At first you will not see any lands
* Create the lands with the NewLand navigation item (if landlord user)
* Complete the required fields and save
* Once saved you should be able to see a new card with the title of your land
* You can edit it with the edit link
* You can see more details of it by clicking the see link
* In this land view you will see all information available including the weather in the area!!
* You can see that depending on how much time is left from the billing deadline a different badge will be displayed
* In the billing view you can visually and rapidly see what are all your billings status
* Now accesing the profile page you will see some personal information and also a messaging system.
* To link your landlord/tenant user with a tenant/landlord user click the add tenant/landlord link 
* A small form should appear, for adding a new user you should know their user ID.
* Send the request and wait for their response. Once they accepted you should see one more tenant/landlord added in your list.
* Normal Messages work the same way

## Screenshots

![capture 1](/CRM/screenshots/Login.png)
![capture 2](/CRM/screenshots/Lands%20View.png)
![capture 3](/CRM/screenshots/land%20view.png)
![capture 4](/CRM/screenshots/new%20land.png)

## Acknowledgments

API, Style and Icons
* [open-weather](https://openweathermap.org/api)
* [bootstrap](https://getbootstrap.com)
* [fontawesome](https://fontawesome.com)
