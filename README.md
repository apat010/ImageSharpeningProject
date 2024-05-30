The app.py file can be ran locally to deploy a shiny python web app to your local machine in which you can upload jpeg/jpg/pdf files and have the image sharpened. I decided to create this project while learning about CNN and what a convolution is. This 
sharpening effect is done by applying a simple convolutional filter using a gaussian kernel. Then the original image is subtracted from the blurred image and multiplied by scalar to enchance the shape of edges which will create a sharpening effect. 


I had issues deploying the file online to shinyio using shiny for python but the file is able to run locally if app.py is executed and numpy, pillow, matplotlib, and shiny are installed for Python in your enviornment. 
