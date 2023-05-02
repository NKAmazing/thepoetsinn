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
