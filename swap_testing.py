from PIL import Image
import os
from kmeans.kmeans import kmeanss

__author__ = "Sethuraman Ramanathan"
__email__ = "iramshiv@gmail.com"


#  construct the argument parser and parse the arguments

def color_centers(image, mink, maxk):
    # Duplicate image name
    init_image = image

    # image name
    head, tail = os.path.split(init_image)

    # generating centers of a cluster
    cluster_centers_ = kmeanss(init_image, mink, maxk)

    # Exit / Redo Variable
    satisfied = 1

    while satisfied > 0:
        print(init_image)

        # input target cluster
        for i in range(len(cluster_centers_)):
            print(f"Color {i}: {list(map(int, cluster_centers_[i]))}")

        target_cluster = input("Enter the color number to change: ")
        target_cluster = int(target_cluster)

        target_rgb = input("Enter RBG code as 0 0 0: ")
        target_rgb = target_rgb.split()
        # print(target_rgb[0])

        shade_range = input("Enter the shades range, skip for default. (Default = 5):")
        if shade_range == "":
            shade_range = int("5")
        else:
            shade_range = int(shade_range)

        tint_range = input("Enter the tint range, skip for default. (Default = 5):")
        if tint_range == "":
            tint_range = int("5")
        else:
            tint_range = int(tint_range)

        src_img = Image.open(init_image)
        # src_img.show()

        img_width = src_img.size[0]
        img_height = src_img.size[1]

        # shades ::: to find the nearest dark color range
        # shade_range = args["shades_range"]
        # tint ::: to find the nearest light color range
        # tint_range = args["tint_range"]

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

        """
        t = min(a) - 15
        t1 = max(a) + 15

        t2 = min(b) - 6
        t3 = max(b) + 6

        t4 = min(c) - 6
        t5 = max(c) + 6
        print(t,t1,t2,t3,t4,t5)

        """

        def zerooff(ttt, ttt1, ttt2):
            if ttt == 0 or ttt1 == 0 or ttt2 == 0:
                tttt = 0
                return tttt
            else:
                tttt = int((ttt / (100 / ((ttt1 / ttt2) * 100))))
                return tttt

        # process all pixels
        for x in range(0, img_width):
            for y in range(0, img_height):
                data = src_img.getpixel((x, y))
                # logic for target and result colors swap with texture formula
                if data[0] in range(roundoff(t), roundoff(t1)) and data[1] in range(roundoff(t2), roundoff(t3)) and \
                        data[
                            2] in range(roundoff(t4), roundoff(t5)):
                    src_img.putpixel((x, y), (
                        zerooff(int(str(target_rgb[0]).replace(",", "")), data[0], roundoff(t1)),
                        zerooff(int(str(target_rgb[1]).replace(",", "")), data[1], roundoff(t3)),
                        zerooff(int(str(target_rgb[2]).replace(",", "")), data[2], roundoff(t5))))

        print("save")
        new_name = "result_" + tail
        src_img.save(new_name)

        # User entry/exit
        satisfied = input("Enter 'Y' to save and continue , 'N' to redo or 'E' to finish: ")
        if satisfied == 'Y' or satisfied == 'y':
            satisfied = 2
            init_image = new_name
        elif satisfied == 'N' or satisfied == 'n':
            satisfied = 1
        else:
            satisfied = 0


color_centers("20SWVWX7_3009_X.jpg", 1, 5)
