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

![image](https://user-images.githubusercontent.com/83615373/235817838-4e5662c9-6766-4123-9b50-408e01c2cf1f.png)

<h3 align="left">

* Edit rating

</h3>

Just as the method of Edit Poem, the Edit Rating method would allow us modify every rating we make. The new edit button would be located in the bottom right part of the rating. 

![image](https://user-images.githubusercontent.com/83615373/235817814-530117b2-cf6f-4479-8d30-934e9c9dd400.png)

<h3 align="left">

* Check profile of other users

</h3>

Until now the functionality to view user profile is only available with the authenticated user at that moment.
The idea would be to add a __Details +__ button that shows us the option to visit that user's profile.

![image](https://user-images.githubusercontent.com/83615373/235817743-0cd74da4-2e28-469f-b0b3-3c3ac4cfa3fe.png)

<h3 align="left">
