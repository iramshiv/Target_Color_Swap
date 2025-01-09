# ENDPOINT 1 User inputs image -> clustering -> Returns Image Colors -> DB Store
# ENDPOINT 2 User Selects a color and swap color -> Color swap algo -> returns the image
# ENDPOINT 3 user redo (2) / save / continue (Endpoint 3)  -> # 2 / exit -> DB Store

from typing import Annotated
from fastapi import FastAPI, HTTPException, Query
from color_swaper_v1 import get_colors, swapper, save

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Color_Swapper"}


@app.post("/predict/", status_code=200)
async def color_cluster(id1: str, img1: str, mink: int = 2, maxk: int = 5):
    try:
        colors_rgb = get_colors(id1, img1, mink, maxk)
    except:
        raise HTTPException(status_code=400, detail="Error! Try again.")

    # return target cluster rgb values to user
    response_object = {}

    for i in range(len(colors_rgb)):
        response_object[i] = colors_rgb[i]
    return response_object

    # print(f"Color {i}: {list(map(int, colors_rgb[i]))}")


@app.post("/swap/", status_code=200)
async def color_swapper(id1: str, img1: str, tgt_color: int, shade: int = 5, tint: int = 5, rgb: Annotated[list[int] | None, Query()] = None):
    try:
        swap_image = swapper(img1, shade, tint, tgt_color, rgb, id1)
    except:
        raise HTTPException(status_code=400, detail="Error! Try again.")

    return swap_image


@app.post("/save/", status_code=200)
async def save_color(id1: str, tgt_color: int, rgb: Annotated[list[int] | None, Query()] = None):
    try:
        save(id1, tgt_color, rgb)
    except:
        raise HTTPException(status_code=400, detail="Error! Try again.")


"""async def color_cluster(img1: str, img2: str, wt1: Union[float, None] = None, wt2: Union[float, None] = None,
                        inf1: Union[float, None] = None, inf2: Union[float, None] = None, sd: Union[int, None] = None,
                        img3: Union[str, None] = None, img4: Union[str, None] = None,
                        wt3: Union[float, None] = None, wt4: Union[float, None] = None, inf3: Union[float, None] = None,
                        inf4: Union[float, None] = None, count: int = 2, mode: str = "Simple"):"""
