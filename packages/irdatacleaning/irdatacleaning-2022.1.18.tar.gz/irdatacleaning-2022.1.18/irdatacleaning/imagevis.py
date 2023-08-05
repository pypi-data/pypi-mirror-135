import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
class Images:
    def __init__(self):
        self.image_bool = False
        self.image_size = 0
        ''' this module is dessigened to allow for you to have an easy way to convert images to numpy array.
        there are four methods in this module.
        the first one is image_to_array(self,image_location,image_size = None,grayscale=False)
        image_location: the folder location of all the images you would like
        single_image_to_array(image_location,image_size=None,grayscale=False)
        thhis model is dessigned to handle one image at a time a good example of this when you need to convert the image you want to predict into an array
        image_location: this is the path to the exact image you want to convert
        image_size: this is the size of the image you want it to be. keep in mind if you have  created an instance of
        image_to_array this argument will default to that value.
        grayscaleq: this allows to convert the images to grayscale with out an extra step to convert'''
        self.image_size = None
    def single_image_to_array(self, image_location,image_size=None, grayscale=False, labels=False):
        if grayscale:
            image = cv2.imread(image_location,cv2.IMREAD_GRAYSCALE)
        else:
            image = cv2.imread(image_location,cv2.IMREAD_COLOR)
        if self.image_bool is False:
            if image.shape[0] >image.shape[1]:
                self.image_size= image.shape[0]
            else:
                self.image_size= image.shape[1]
        image = cv2.resize(image,(self.image_size,self.image_size))
        image = image/255.0
        return image
    def _grayscale(self,image_location):
        image = cv2.imread(image_location,cv2.IMREAD_GRAYSCALE)
    def image_to_array(self,image_location,image_size = None,grayscale=False,labels=False):
        image_array_1 = []
        image_label = []
        equl = False
        # if image_location[-1] !="/":
        #     print("yes")
        #     image_location= f"{image_location}/"
        for i in os.listdir(image_location):
            if grayscale==True:
                image_array_1.append(cv2.imread(os.path.join(image_location,i),cv2.IMREAD_GRAYSCALE))

            elif grayscale==False:
                # print("yes")
                image_array_1.append(cv2.imread(os.path.join(image_location,i),cv2.IMREAD_COLOR))
            image_label.append(i)

        max_seconds_dem = np.array([i.shape[0] for i in image_array_1])
        max_third_dem = np.array([i.shape[1] for i in image_array_1])
        final_image_data = []
        if self.image_bool is False:
            if max_seconds_dem.mean()< max_third_dem.mean():
                self.image_size = round(max_seconds_dem.mean()/2)
            elif max_third_dem.mean()<=max_seconds_dem.mean():
                self.image_size = round(max_third_dem.mean()/2)
            self.image_bool = True
        for i in image_array_1:
            final_image_data.append(cv2.resize(i,(self.image_size,self.image_size)))
        if grayscale:
            print("yes")
            X = np.array(final_image_data).reshape(-1,self.image_size,self.image_size)
        else:
            X = np.array(final_image_data).reshape(-1,self.image_size,self.image_size,3)
        X = X/255.0
        y = np.array([i.split(".")[0] for i in image_label])
        if labels:
            return X,y
        return X
    def pixel(self,image_location,grayscale=False):
        if isinstance(image_location,str):
            if grayscale:
                image_location = cv2.imread(image_location,cv2.IMREAD_GRAYSCALE)
            else:
                image_location = cv2.imread(image_location, cv2.IMREAD_COLOR)


        plt.figure()
        plt.imshow(image_location)
        plt.colorbar()
        plt.grid(False)
        plt.show()
    def picture_grid(self, image_location, image_label,class_name = [], grayscale=False):
        plt.figure(figsize=(10,10))
        for i in range(25):
            for  j in range(10):
                plt.subplot(5,5,i+1)
                plt.xticks([])
                plt.yticks([])
                plt.grid(False)
                if grayscale:
                    plt.imshow(cv2.imread(image_location,cv2.IMREAD_GRAYSCALE), cmap=plt.cm.binary)
                else:
                    plt.imshow(cv2.imread(image_location), cmap=plt.cm.binary)
                if (len(class_name)==0):
                    plt.xlabel(image_label[i])
                else:
                    plt.xlabel(image_label[class_name[i]])
                    # print("yess")
        plt.show()

if __name__ == "__main__":
    import tensorflow as tf
    from tensorflow import keras
    import irdatacleaning as ird

    mnist = keras.datasets.mnist

    (X_train,X_test),(y_train,y_test) = mnist.load_data()

    image = Images()

    # image.pixel(image_location="/Users/williammckeon/Downloads/cats_and_dogs/cat_dog/cat.0.jpg",grayscale=True)
    X,y = image.image_to_array(image_location="/Users/williammckeon/Downloads/train_transformed",grayscale=True,labels= True)
    print(X.shape,y.shape)