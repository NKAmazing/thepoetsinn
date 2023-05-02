<h1 align="center">Installation Process</h1>

<h3 align="left">

* Clone the repository

</h3>

First, we have to copy the https url of the repository.

![image](https://user-images.githubusercontent.com/83615373/235744026-b220b6e5-114b-426f-9739-b70c72e4811c.png)

Then, we need to open a terminal. In case of not having git installed in our system, we must install it first.

```bash
sudo apt update
sudo apt install git
```
Now, we proceed to clone the repository in our workspace.

```bash

git clone https://github.com/NKAmazing/Programacion-I.git

```

<h3 align="left">

* Give execute permissions to our shell script files

</h3>

In order to execute our __.sh__ files, we have to give it the execution permissions.

```bash

chmod +x ./install.sh

```

```bash

chmod +x ./boot.sh

```



<h2 align="left">Backend</h2>

<h3 align="left">

* Env file creation

</h3>

We create an __.env__ file and fill it with the correct data from our workspace. To do this we take the data from our __.env-example__.

![image](https://cdn.discordapp.com/attachments/1091530117454499862/1103003269837619221/image.png)

<h3 align="left">

* Install Requirements

</h3>

In the terminal, we must execute our __install.sh__ file. This will allow us to install all the requirements of the project that are stored in the __requirements.txt__ file.

```bash

./install.sh

```

<h3 align="left">

* Run Backend Service

</h3>

Finally, we run the backend service with our __boot.sh__ file.

```bash

./boot.sh

```
Flask Backend server running:

![image](https://user-images.githubusercontent.com/83615373/235750040-fa2cf5bd-f561-44c8-b9aa-bcd14cc9e1cb.png)


<h2 align="left">Frontend</h2>

<h3 align="left">

* Env file creation

</h3>

We create an __.env__ file and fill it with the correct data from our workspace. To do this we take the data from our __.env-example__.

![image](https://user-images.githubusercontent.com/83615373/235751143-5a75e057-f36b-4a96-8368-a0a321b2973c.png)

<h3 align="left">

* Install Requirements

</h3>

In the terminal, we must execute our __install.sh__ file. This will allow us to install all the requirements of the project that are stored in the __requirements.txt__ file.

```bash

./install.sh

```

<h3 align="left">

* Run Frontend Service

</h3>

Finally, we run the frontend service with our __boot.sh__ file.

```bash

./boot.sh

```
Flask Frontend server running:

![image](https://user-images.githubusercontent.com/83615373/235750800-7dede5dc-a76b-419c-9898-2816ffbf4a91.png)

