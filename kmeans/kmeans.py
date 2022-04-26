import os

import matplotlib.pyplot as plt
import matplotlib.image as img
import cv2
import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from os import path
from matplotlib.pyplot import ion
from sklearn.cluster import KMeans
from joblib import Parallel, delayed

def kmeanss(simage, min_k, max_k):
    src_image = cv2.imread(simage)
    image = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
    # plt.figure()
    # plt.axis("off")
    # plt.imshow(image)

    # reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    # cluster the pixel intensities
    k_range = range(min_k, max_k)
    print("------Initiating Clustering!!!")
    best_k = choose_best_k_parallel(simage, k_range)
    # print(best_k)
    clt = KMeans(n_clusters=best_k)
    clt.fit(image)
    print("------Clustering Finished!!!")

    # build a histogram of clusters and then create a figure
    # representing the number of pixels labeled to each color
    hist = centroid_histogram(clt)
    bar = plot_colors(hist, clt.cluster_centers_)

    # show our color bar
    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    ion()
    plt.show()

    """ --- Calculating cluster data min and max ----

    target_cluster = input('Enter the target cluster:')
    target_cluster = int(target_cluster)

    a = []
    b = []
    c = []

    for i in image[clt.labels_ == target_cluster]:
        a.append(i[0])
        b.append(i[1])
        c.append(i[2])

    return clt.cluster_centers_, a, b, c
    
    """
    return clt.cluster_centers_


def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()
    # return the histogram
    return hist


def plot_colors(hist, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0
    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar


def choose_best_k_parallel(data, k_range):
    """
    Returns
    -------
    best_k: int
        chosen value of k out of the given k range.
        chosen k is k with the minimum inertia value.
    results: (int) best k
    """
    data = img.imread(data)
    r = []
    g = []
    b = []

    for row in data:
        for pixel in row:
            # A pixel contains RGB values
            r.append(pixel[0])
            g.append(pixel[1])
            b.append(pixel[2])

    df = pd.DataFrame({'red': r, 'green': g, 'blue': b})

    # choose features
    data_for_clustering = df.copy()

    # create data matrix
    data_matrix = np.asarray(data_for_clustering).astype(float)

    # scale the data
    mms = MinMaxScaler()
    data = mms.fit_transform(data_matrix)

    ans = Parallel(n_jobs=-1, verbose=10)(delayed(kmeansres)(data, k) for k in k_range)
    ans = list(zip(k_range, ans))
    results = pd.DataFrame(ans, columns=['k', 'Scaled Inertia']).set_index('k')
    best_k = results.idxmin()[0]
    return best_k


def kmeansres(data, k, alpha_k=0.02):
    """
    alpha_k: float
        manually tuned factor that gives penalty to the number of clusters
    Returns
    -------
    scaled_inertia: float
        scaled inertia value for current k
    """

    inertia_o = np.square((data - data.mean(axis=0))).sum()
    # fit k-means
    kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
    inertia = kmeans.inertia_ / inertia_o + alpha_k * k
    return inertia
