# sirbarksalot

This application listens for barking based on my miniature dachshund, Cody.

![Cody](cody.jpg)


# v0
The first version is based on spectrogram template matching. A sample
clip is used to create a template and then each recorded clip is compared
to the template.

The core components are

* __Listener__: module for recording and creating spectrograms
* __Detector__: match template calculation
* __Messenger__: basic facebook messenger app

It's currently set up as a flask app, although that part isn't completely
necessary. Eventually, I will set up a way to record phone numbers so the
user can subscribe to barking notifactions.
