__author__ = "Sethuraman Ramanathan"
__email__ = "iramshiv@gmail.com"

import base64
import io
import os
import re
import urllib.request
import sqlalchemy
from PIL import Image
from kmeans.kmeans_1 import kmeanss


# DB operation
def db_connect(stmt, id1, cid, rgb):
    # create connection pool
    pool = sqlalchemy.create_engine(
        url="mysql+pymysql://swapper:r&k%f.o0_|4asvTo@34.72.203.129:3306/swap-id"
    )

    if stmt == 1:
        # insert statement
        insert_stmt = sqlalchemy.text(
            "INSERT INTO colors (id, c_id, rgb_code) VALUES (:id, :c_id, :rgb_code)",
        )

        with pool.connect() as db_conn:
            db_conn.execute(insert_stmt, parameters={"id": id1, "c_id": cid, "rgb_code": rgb})
            db_conn.commit()
            db_conn.close()

    # Retreive statement
    elif stmt == 2:
        result = ""
        # create connection pool
        pool = sqlalchemy.create_engine(
            url="mysql+pymysql://swapper:r&k%f.o0_|4asvTo@34.72.203.129:3306/swap-id"
        )

        select_stmt = sqlalchemy.text(
            f'select rgb_code from colors where id = "{id1}" and c_id = {cid}'
        )

        with pool.connect() as db_conn:
            rgb_code = db_conn.execute(select_stmt).fetchall()
            db_conn.close()
            for row in rgb_code:
                result = row[0]
                result = str(result).split()
                result = [int(s) for s in result]
                print(result)
        return result
    elif stmt == 3:

        # create connection pool
        pool = sqlalchemy.create_engine(
            url="mysql+pymysql://swapper:r&k%f.o0_|4asvTo@34.72.203.129:3306/swap-id"
        )

        st = re.sub('[^A-Za-z0-9 ]+', '', str(list(map(int, rgb))))

        tbl = sqlalchemy.Table('colors', sqlalchemy.MetaData(), autoload_with=pool)
        update_stmt = sqlalchemy.update(tbl).where(tbl.c.id == id1).where(tbl.c.c_id == cid).values(rgb_code=st)
        print(update_stmt)

        with pool.begin() as db_conn:
            db_conn.execute(update_stmt)
            db_conn.commit()
            db_conn.close()


# save rgb
def save(id1, tgt_color, rgb):
    sav = db_connect(3, id1, tgt_color, rgb)


# Get color centers / cluster -> Kmeans
def get_colors(id1, image1, mink, maxk):
    color_code = []

    head, tail = os.path.split(image1)
    urllib.request.urlretrieve(image1, tail)
    im1 = tail

    cluster_centers_ = kmeanss(im1, mink, maxk)
    print(cluster_centers_)

    for i in range(len(cluster_centers_)):
        st = re.sub('[^A-Za-z0-9 ]+', '', str(list(map(int, cluster_centers_[i]))))
        color_code.append(st)
        db_connect(1, id1, i, st)

    remove_image(im1)

    return color_code


# remove downloaded image function
def remove_image(name):
    if os.path.exists(name):
        os.remove(name)
    else:
        print("The file does not exist")
        pass


# cut-off thershold -> 0 to 255 (Min & Max RGB Values)
def roundoff(tt):
    tt = int(tt)
    if tt > 255:
        tt = 255
    elif tt < 0:
        tt = 0
    else:
        tt = tt
    return tt


# Zero-off threshold cut-off -> when either 0, terminate the calculation and return 0
def zerooff(ttt, ttt1, ttt2):
    if ttt == 0 or ttt1 == 0 or ttt2 == 0:
        tttt = 0
        return tttt
    else:
        tttt = int((ttt / (100 / ((ttt1 / ttt2) * 100))))
        return tttt


# Swap colors
def swapper(image, shade_range, tint_range, target_color_id, target_rgb, id2):
    # image name
    head, tail = os.path.split(image)
    urllib.request.urlretrieve(image, tail)
    src_img = Image.open(tail)
    img_width = src_img.size[0]
    img_height = src_img.size[1]
    # src_img.show()

    # retrive target color rgb code from DB
    color_center = db_connect(2, id2, target_color_id, 0)
    print("SWAP", color_center)

    # generate target colour range to swap (RGB values)
    t = color_center[0] - (shade_range * 10)
    t1 = color_center[0] + (tint_range * 10)

    t2 = color_center[1] - (shade_range * 13)
    t3 = color_center[1] + (tint_range * 7)

    t4 = color_center[2] - (shade_range * 7)
    t5 = color_center[2] + (tint_range * 13)

    # swap target color pixels
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

    new_name = "result_" + tail
    src_img.save(new_name)

    with open(new_name, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    remove_image(tail)
    remove_image(new_name)

    return encoded_string


# get_colors("demo1", "https://dej6x0vqs54ie.cloudfront.net/stylemix/output/Leonardo_Diffusion_XL_Shirts_0-c0923a1a-be21-11ef-966a-522477d38882.jpg", 2, 5)
# swapper("https://dej6x0vqs54ie.cloudfront.net/stylemix/output/Leonardo_Diffusion_XL_Shirts_0-c0923a1a-be21-11ef-966a-522477d38882.jpg", 9, 3, 3, [83, 115, 36], "demo1")
# https://dej6x0vqs54ie.cloudfront.net/stylemix/output/Leonardo_Diffusion_XL_Shirts_0-c0923a1a-be21-11ef-966a-522477d38882.jpg
# https://i.ibb.co/R0cndKH/18-SWVK56-2000-60.jpg
# save("demo1", 3, [33, 9, 7])
