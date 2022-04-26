from PIL import Image
import argparse

#  construct the argument parser and parse the arguments
from kmeans.kmeans import kmeanss

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True)
ap.add_argument("-o", "--output", required=True)
ap.add_argument("-rgb", "--target_rgb", required=True, nargs='+', type=int, default=[0, 0, 0])
ap.add_argument("-k", "--mink", default=2, type=int)
ap.add_argument("-k1", "--maxk", default=7, type=int)
ap.add_argument("-s", "--shades_range", default=5, type=int)
ap.add_argument("-t", "--tint_range", default=5, type=int)
args = vars(ap.parse_args())

print(args["target_rgb"][0])
print(args["target_rgb"][1])
print(args["target_rgb"][2])

# generating centers of a cluster
cluster_centers_ = kmeanss(args["image"], args["mink"], args["maxk"])

# input target cluster
target_cluster = input("Enter the target cluster from the plot generated (clusters starts from '0'):")
target_cluster = int(target_cluster)

src_img = Image.open(args["image"])
# src_img.show()

img_width = src_img.size[0]
img_height = src_img.size[1]

# shades ::: to find the nearest dark color range
shade_range = args["shades_range"]
# tint ::: to find the nearest light color range
tint_range = args["tint_range"]

# generate target colour range (RGB values)
t = round(int(cluster_centers_[target_cluster][0])) - (shade_range * 10)
t1 = round(int(cluster_centers_[target_cluster][0])) + (tint_range * 10)

t2 = round(int(cluster_centers_[target_cluster][1])) - (shade_range * 13)
t3 = round(int(cluster_centers_[target_cluster][1])) + (tint_range * 7)

t4 = round(int(cluster_centers_[target_cluster][2])) - (shade_range * 7)
t5 = round(int(cluster_centers_[target_cluster][2])) + (tint_range * 13)


def roundoff(tt):
    tt = int(tt)
    if tt > 255:
        tt = 255
    elif tt < 0:
        tt = 0
    else:
        tt = tt
    return tt
    print(tt)


"""
t = min(a) - 15
t1 = max(a) + 15

t2 = min(b) - 6
t3 = max(b) + 6

t4 = min(c) - 6
t5 = max(c) + 6
print(t,t1,t2,t3,t4,t5)

"""

# process all pixels
for x in range(0, img_width):
    for y in range(0, img_height):
        data = src_img.getpixel((x, y))
        # logic for target and result colors swap with texture formula
        if data[0] in range(roundoff(t), roundoff(t1)) and data[1] in range(roundoff(t2), roundoff(t3)) and data[
            2] in range(roundoff(t4), roundoff(t5)):
            src_img.putpixel((x, y), (
                int((args["target_rgb"][0] / (100 / ((data[0] / t1) * 100)))), int((args["target_rgb"][1] / (100 / ((data[1] / t3) * 100)))),
                int((args["target_rgb"][2] / (100 / ((data[2] / t5) * 100))))))

src_img.save(str(args["output"]) + '/result.jpg')
res_img = Image.open(str(args["output"]) + '/result.jpg')
res_img.show()
