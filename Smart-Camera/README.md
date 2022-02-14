# Smart-Camera
IoT Raspberry Pi security camera running open-cv for object detection. The camera will send an email with an image of any objects it detects. It also runs a server that provides a live video stream over the internet.


## Setup

This project uses a Raspberry Pi Camera to stream video. Before running the code, make sure to configure the raspberry pi camera on your device.

Open the terminal and run

```
sudo raspi-config
```

Select `Interface Options`, then `Pi Camera` and toggle on. Press `Finish` and exit.

You can verify that the camera works by running

```
raspistill -o image.jpg
```
which will save a image from the camera in your current directory. You can open up the file inspector and view the image.

## Installing Dependencies

This project uses openCV to detect objects in the video feed. You should install opencv on Raspberry Pi. Look for a tuturial in Google. 


Next, navigate to the repository directory

```
cd Smart-Camera
```

and install the dependencies for the project

```
pip3 install -r requirements.txt
```

* Use only python 3 version

## Customization

To get emails when objects are detected, you'll need to make a couple modifications to the `mail.py` file.

Open `mail.py` with nano `nano mail.py`. Scroll down to the following section

```
# Email you want to send the update from (only works with gmail)
fromEmail = 'myemail@gmail.com'
fromEmailPassword = 'password1234'

# Email you want to send the update to
toEmail = 'anotheremail@gmail.com'
```
and replace with your own email/credentials. The `mail.py` file logs into a gmail SMTP server and sends an email with an image of the object detected by the security camera. 

Press save and exit.

You can also modify the `main.py` file to change some other properties.

```
object_classifier = cv2.CascadeClassifier("haarcascades/fullbody_recognition_model.xml") # an opencv classifier
```
Notably, you can use a different object detector by changing the path `"haarcascades/fullbody_recognition_model.xml"` in `object_classifier = cv2.CascadeClassifier("haarcascades/fullbody_recognition_model.xml")`.
to a new model in the haarcascades directory.

```
facial_recognition_model.xml
fullbody_recognition_model.xml
upperbody_recognition_model.xml
```

## Running the Program

Run the program

```
python main.py
```

You can view a live stream by visiting the ip address of your pi in a browser on the same network. You can find the ip address of your Raspberry Pi by typing `ifconfig` in the terminal and looking for the `inet` address. 

Visit `<raspberrypi_ip>:5000` in your browser to view the stream.

Note: To view the live stream on a different network than your Raspberry Pi, you can use [ngrok](https://ngrok.com/) to expose a local tunnel. Once downloaded, run ngrok with `./ngrok http 5000` and visit one of the generated links in your browser.
