<h1 align="left">Information about the technical and creative process</h1>

<p align="center">
  <img src="https://cdn.discordapp.com/attachments/1091530117454499862/1101727135409897482/image.png" />
</p>

The project contains two services, one dedicated to the Backend connected to an API REST and another dedicated to the Frontend which through a series of configured routes makes requests to the API and brings the information requested by the user.

Project Structure:

![general-structure-img](https://user-images.githubusercontent.com/83615373/235558307-9898c514-7391-4b2d-82b1-5cc6ef543e7d.png)

Architecture graphic:
```mermaid
flowchart TD
User[/User\]
Frontend[Frontend]
Backend[Backend]
Database[(Database)]
User --> Frontend
Frontend -- request --> API-REST
API-REST -- works with --> Backend
Backend -- works with --> API-REST
Backend -- query --> Database
```

<h2 align="left">Making the Backend</h2>

The Backend consists of a Flask service connected to an API REST in which through a series of resources we access to the database that contains the credentials established in the project models.

![backend-structure-img](https://user-images.githubusercontent.com/83615373/235558591-1bbdc7be-1717-445d-af3a-05f09f32c73a.png)



<h3 align="left">Development process:</h3>

<h4 align="left">

* Creation of the App:

</h4>  

To create the application, an app.py file must be created where the application must be initialized along with its respective functionalities.

![image](https://user-images.githubusercontent.com/83615373/235561260-4ea2a253-883d-4251-a00d-e13306a64842.png)

An __init__.py is then created in the main folder, which allows the folder containing the app.py file to be converted to a Python package. This with the aim that modules and packages can be imported into the Flask application in an easier and more organized way.

![image](https://user-images.githubusercontent.com/83615373/235563710-93643402-35c3-4a57-902a-e2578d83822f.png)


<h4 align="left">
  
* Building Models:

</h4>

In order for the service to work, we must create the credentials that will contain the data in each Object of our application.

![image](https://user-images.githubusercontent.com/83615373/235566134-99b7ec37-1194-4010-92ca-9c181210f6f3.png)

<h4 align="left">

* Database connection and relationships:

</h4>

These data will be stored in our SQLite3 Database.

![image](https://user-images.githubusercontent.com/83615373/235567048-9ad8dad8-d4d1-40db-a385-ea89fb6153ed.png)

Relationships with the models.

![image](https://user-images.githubusercontent.com/83615373/235566585-d501ff99-d152-4028-b842-8ce53be19e38.png)

<h4 align="left">
  
* Building Resources:

</h4>

Next, we must build the resources that will operate the different HTTP methods in our API.

![image](https://user-images.githubusercontent.com/83615373/235563605-3526b62c-183d-4152-9f25-91d101ddae88.png)

Poem Resources structure and implementation.

![image](https://user-images.githubusercontent.com/83615373/235568539-3b6e8054-90f7-43ea-95e5-37b65009adc4.png)

<h4 align="left">
  
* Authentication:

</h4>

We need to implement authentication to prevent unauthorized users from accessing private views.

![image](https://user-images.githubusercontent.com/83615373/235572536-3974132b-7dc2-4111-a58f-6bc31c9b9ed3.png)

For this we use JWT (JSON Web Token), which consists of generating a Token that has three parts encoded in Base64, each separated by a dot.

![image](https://user-images.githubusercontent.com/83615373/235688411-f6631055-524f-4704-a053-b1eb2fe7a557.png)

We start with importing the Flask functionality for JWT.

![image](https://user-images.githubusercontent.com/83615373/235690785-e6d73957-e11f-4e4e-96da-7d51dd532628.png)

Then, we proceed to decorate the functions that require some kind of authentication.

![image](https://user-images.githubusercontent.com/83615373/235572319-40e6da90-e946-47a1-a1db-e90254460244.png)

<h4 align="left">
  
* Mail:

</h4>

Finally, we created an email service that can notify users when their poems are rated.

![image](https://user-images.githubusercontent.com/83615373/235692782-95cde848-8613-4c6a-8631-ed5e4f0c9157.png)

And we add it to the POST method of Rating resource.

![image](https://user-images.githubusercontent.com/83615373/235693278-e053ea91-859b-4561-9569-5b148904ad78.png)



<h2 align="left">Making the Frontend</h2>

The Frontend consists of a Flask service that connects to the Backend service. To do this, I use a series of functions and routes that execute HTTP methods and obtain the data from the website by making requests to the API REST. Finally I send them to an HTML template that is responsible for displaying the data on the page.

![frontend-structure-img](https://user-images.githubusercontent.com/83615373/235557921-c18d40fd-411b-462e-9041-86e83850e1f7.png)


More information in the coming weeks.
