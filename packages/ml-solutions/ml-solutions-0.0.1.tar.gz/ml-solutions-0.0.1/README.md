# Ml-Solutions

A Python Pacakage for Ready Made Machine Learning Solutions.

# Installation
To install this package, you have to run this command on your terminal
```
pip install ml-solutions
```

# Quick Start Guide
```
from ml_solutions import solutions

# Spam Message Detector

spam_message_detector = solutions.SpamMessageDetector()
spam_message_detector.train()
detected = spam_message_detector.detect_spam('Please subscribe my youtube channel for 100 years of good luck!')

if detected == True:
    print("Message is Spam!")
else:
    print("The message is not Spam!")

# House Price Prediction

house_price_predictor = solutions.HousePricePrediction()
house_price_predictor.train()
Price = house_price_predictor.get_price(rooms=2, bathrooms=1, landsize=230, lattidute=-346.876, longtitude=347.378)
print(Price)

# Image Classification

# Training and Saving The Model
image_classifier = solutions.ImageClassification()
image_classifier.train()
image_classifier.save_model('image_classifier')

# After that you will see your training of the model has been started!
# When training is complete, then remove all the code and write:

# Loading the Model
image_classifier = solutions.ImageClassification()
image_classifier.load_model('image_classifier')
# For image classification, you need a 32*32 px image, to convert your image into a 32*32 px image, go into this website: https://www.privatedaddy.com/resize-to-32x32
# After you converted your image, give the path to the 32*32 image
recognized = image_classifier.recognize_image('image.jpg')
print(recognized)

# You will see the name of the thing in the image :)
# This supports with 'Plane', 'Car', 'Bird', 'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck'

# And we have more Ml Solutions :)

# In the next version, you can see for Machine Learning solutions.
```