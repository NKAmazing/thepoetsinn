<h1 align="center">Future functionalities</h1>

This section contains functionalities proposed as ideas that have not yet been implemented in the project.

<h3 align="left">

* URL Custom

</h3>

The idea is to change the url from <code>localhost:3000</code> to something like <code>thepoetsinn.com</code>

![image](https://cdn.discordapp.com/attachments/1091530117454499862/1103035354304491660/image.png)

To do this, the following steps must be followed:

- Buy a domain name from one of the many domain registration services available online, such as GoDaddy, Namecheap, HostGator, and more.

- Configure the IP address after acquiring a domain, this way it points to the server where the Flask application is hosted.

- Set up a web server like Nginx or Apache and set up a URL redirect.

- Update the Flask configuration so that the application runs in the new custom url. This way:

```python
app.run(host='thepoetsinn.com', port=80)

```
<h3 align="left">

* Notification system

</h3>

A new functionality in the Frontend that allow us to receive notificacions when someone rate your poems.
Similar to the send email configuration, this function would allow us to see a message with the same information in the Navbar section of the template, right next to the Logout button.

![image](https://user-images.githubusercontent.com/83615373/235813184-696be480-4fa8-4d69-9546-1986dd6d3733.png)

<h3 align="left">

* Edit rating

</h3>

Just as the method of Edit Poem, the Edit Rating method would allow us modify every rating we make. The new edit button would be located in the bottom right part of the rating. 

![image](https://user-images.githubusercontent.com/83615373/235813907-31757a47-67f3-4068-b61d-8cef92bd82c1.png)

<h3 align="left">

* Check profile of other users

</h3>

Until now the functionality to view user profile is only available with the authenticated user at that moment.
The idea would be to add a Details + button that shows us the option to visit that user's profile.

![image](https://user-images.githubusercontent.com/83615373/235814323-d2c15da5-59ea-4308-834b-56a3021004e2.png)

<h3 align="left">

* Updating Flask

</h3>

Looks like there's some vulnerability with Flask actual version of the project. We need to update Flask version of the requirements.txt to solve the problem.

![image](https://user-images.githubusercontent.com/83615373/235816205-75f375cd-4946-4d07-86d7-480d0fb69538.png)



