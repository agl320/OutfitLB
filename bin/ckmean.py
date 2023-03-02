import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans



class CKmean():
  """
  UNSUPERVISED LEARNING ALGORITHM; given unlabelled data, and task is to find structures or patterns
  - specify clusters k
  - initialize centroids by randomly selecting data points w/o replacement
  - keep iterating until no change in centroids
  """
  def __init__(self, imagepath):
    # Reading image into array
    img=cv2.imread(imagepath)
    # Conversion from BGR to RGB
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # Reshaping into flat array [R G B] of MxN size
    img=img.reshape((img.shape[1]*img.shape[0],3))

    # Kmeans algorithm
    kmeans=KMeans(n_clusters=5)
    s=kmeans.fit(img)

    # Each point assigned a label (cluster)
    labels=kmeans.labels_
    labels=list(labels)

    # Average position
    centroid=kmeans.cluster_centers_

    # For each centroid size, take proportion 
    percent=[]
    for i in range(len(centroid)):
      # Number of points within pertaining to a cluster
      j=labels.count(i)
      # Dividing by total number of points
      j=j/(len(labels))
      # Average out of 100
      percent.append(j)

    plt.pie(percent,colors=np.array(centroid/255),labels=np.arange(len(centroid)))
    plt.savefig('clothing_pie', bbox_inches='tight')