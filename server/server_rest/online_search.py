import argparse as ap
import cv2
import numpy as np
import os
from sklearn.externals import joblib
from scipy.cluster.vq import *

from sklearn import preprocessing
import numpy as np

from pylab import *
from PIL import Image


def online_search():
    # Get query image path
    image_path = "/home/decanter/PycharmProjects/Picture_Browser2/server/test.jpg"

    # Load the classifier, class names, scaler, number of clusters and vocabulary
    im_features, image_paths, idf, numWords, voc = joblib.load("bof_retr.pkl")

    # Create feature extraction and keypoint detector objects
    # List where all the descriptors are stored
    des_list = []
    sift = cv2.xfeatures2d.SIFT_create()

    im = cv2.imread(image_path)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    kp, des = sift.detectAndCompute(gray, None)

    des_list.append((image_path, des))

    # Stack all the descriptors vertically in a numpy array
    descriptors = des_list[0][1]

    #
    test_features = np.zeros((1, numWords), "float32")
    words, distance = vq(descriptors, voc)
    for w in words:
        test_features[0][w] += 1

        # Perform Tf-Idf vectorization and L2 normalization
    test_features = test_features * idf
    test_features = preprocessing.normalize(test_features, norm='l2')

    score = np.dot(test_features, im_features.T)
    rank_ID = np.argsort(-score)
    print(score)

    # Visualize the results
    figure()
    # gray()
    subplot(5, 4, 1)
    imshow(im[:, :, ::-1])
    axis('off')
    res = []
    for i, ID in enumerate(rank_ID[0][0:16]):
        if score[0][i] > 0.3:
            res.append(((image_paths[ID].replace("/home/decanter/PycharmProjects/Picture_Browser2/server/", "http://172.20.10.9:8000/")), score[0][i]))

    return res
