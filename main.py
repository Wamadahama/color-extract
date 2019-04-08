import numpy as np
from sklearn.cluster import KMeans
import cv2
from jinja2 import Template

def get_hex_at_pos(img, x, y):
    color = img[x,y]
    return tuple([color[2], color[1], color[0]])

def get_matrix(filename):
    img = cv2.imread(filename)
    x_len = len(img)
    y_len = len(img[0])
    points = []
    for i in range(0, x_len):
        for j in range(0, y_len):
            points.append(get_hex_at_pos(img, i, j))
    return(points)

def get_cluster_values(kmeans, i):
    return np.where(kmeans.labels_ == i)[0]

def comp_avg(cluster,matrix):
    pixels = [matrix[pixel_pos] for pixel_pos in cluster]
    col_totals = [sum(x) for x in zip(*pixels)]
    return [total / cluster.size for total in col_totals]

def rbg_to_hex(rgb_list):
    return "{0:02x}{1:02x}{2:02x}".format(*rgb_list)

CLUSTERS = 9
matrix = get_matrix("ryuuko.jpg")
kmeans = KMeans(n_clusters=CLUSTERS, random_state=0).fit(matrix)

average_colors = [rbg_to_hex(comp_avg(get_cluster_values(kmeans, i), matrix))
                  for i in range(CLUSTERS)]

html = open("template.html", "r").read()
template = Template(html)
text = template.render(color_list = average_colors)


f = open("pallete.html", "w")
f.write(text)
f.close()
