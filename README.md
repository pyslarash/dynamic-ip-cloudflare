# Monitor Dynamic IP (with Cloudflare)

If you are running a home-based server, and Cloudflare is your DNS provider then this code is for you. Home internet providers have a tendency of using dynamic IPs, so you either need to make sure you are updating your IP or request a static one. I know I don't like to ask for anything, so I wrote this code that monitors for changes between my current IP and the IP listed on Cloudflare (it ignores mail A records since I host it on a server with a static IP). 

Here's what you need to do to setup this code:

## Step 1 - .env

Obtain an API token from Cloudflare:

Go to **'Profile Icon in Top Right' -> My Profile -> API Tokens -> Create Token -> Edit zone DNS -> Use Template**.

In **Zone Resources** select **All Zones** instead of a **Specific Zone**.

Click **Continue to Summary -> Create Token**

***Copy this token***

Create a **.env** file in the root directory of the project and add this line:

```
API_TOKEN = "Your Copied Token"
```

## Step 2 - Add Zones File

In the root directory add a file called **zones.txt**. In there list all of your zones (your websites from Cloudflare) on each separate line. For example:

```
zone1.com
zone2.com
zone3.com
```

## Step 3 - Time Interval

By default the script checks IPs every **15 mins** (900 seconds). You can modify it if needed.

In **app.py** on line **33** you'll find a **check_time** value set to 900. You can set it to whatever you want (in seconds).

## Step 4 - Setup Virtual Environment

I assume that you run linux, so just run

```
python -m venv vevn
source venv/bin/activate
```

## Step 5 - Install Requirements

```
pip install -r requirements.txt
```

## Step 6 - Build a Docker Container

```
docker-compose build
docker-compose up -d
```

Done, now your server is monitoring in changes of your IP and updates Cloudflare whenever needed (except mail records). I hope it will help someone. Feel free to give me a star if it worked for you.

### Technologies

<div>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" alt="Python" title="Python"/></code>
  <code><img width="50" src="https://user-images.githubusercontent.com/25181517/117207330-263ba280-adf4-11eb-9b97-0ac5b40bc3be.png" alt="Docker" title="Docker"/></code>
</div>
