
# Flask app

---

In this project a website was developed using Flask library (a web application framework written in Python). The objective was: elaborate from scratch a community website where students and specialists could post information about any programming language or development subject they want.

The main objective was improve knowledge in Python through the use of libraries that help web development, as well as integration with local and remote databases.

The website has validations during login and in all forms inside navigation and operations with posts, as well as screen restrictions if the user is not logged in.

## Funcionalities

---

- User creation 
- Post creation
- Post edition
- Login
- User's profile edition

The development was done using mainly:

- Python (back-end)
- Bootstrap (front-end)

Main Pyhton libraries used:

- Flask Login
- Flask Forms
- Login Manager
- WTF Forms (field validators)
- Blueprint (used for code organization and structure)

## Project Structure

---

```shell
flask-app/
├── models
│   ├── class_post.py
│   ├── class_usuario.py
│   ├── forms.py
├── posts
│   ├── templates
│   │   └── ...
│   ├── __init__.py
│   ├── posts.py
├── profiles
│   ├── templates
│   │   └── ...
│   ├── __init__.py
│   ├── profiles.py
├── public_pages
│   ├── templates
│   │   └── ...
│   ├── __init__.py
│   ├── public_pages.py
├── static
│   ├── profile_pictures
│   │   └── ...
│   ├── readme_pictures
│   │   └── ...
│   ├── main.css
├── users
│   ├── templates
│   │   └── ...
│   ├── __init__.py
│   ├── users.py
├── __init__.py
├── app.py
├── extensions.py
├── local_database.db
├── README.md
```


## Screenshots

---
All posts are shown on the homepage (from all users) containing the creation dates, user's photo and courses information.

![home.png](myproject%2Fstatic%2Freadme_pictures%2Fhome.png)

The site has access restrictions to some pages (only for registered members), for which the flask login manager library was used.

![login.png](myproject%2Fstatic%2Freadme_pictures%2Flogin.png)
![create_account.png](myproject%2Fstatic%2Freadme_pictures%2Fcreate_account.png)

The connection to the DB is performed with SQLAlchemy, and a SQLITE DB locally or POSTGRESQL on the server was used.

![users.png](myproject%2Fstatic%2Freadme_pictures%2Fusers.png)

It is possible to edit the user profile, adding a profile picture, registering courses in which he specializes, changing the user name, e-mail and password.

![profile.png](myproject%2Fstatic%2Freadme_pictures%2Fprofile.png)
![profile_update.png](myproject%2Fstatic%2Freadme_pictures%2Fprofile_update.png)

Only the user who created the post is able to edit or delete it by accessing the post page.

![create_post.png](myproject%2Fstatic%2Freadme_pictures%2Fcreate_post.png)
![post.png](myproject%2Fstatic%2Freadme_pictures%2Fpost.png)
![edit_post.png](myproject%2Fstatic%2Freadme_pictures%2Fedit_post.png)
![delete_post.png](myproject%2Fstatic%2Freadme_pictures%2Fdelete_post.png)