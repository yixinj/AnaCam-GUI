import cv2 as cv
import numpy as np
import pandas as pd
import colorsys
from scipy import optimize


def analyze(src, num_contours=3, threshold=50):
    """Gets the mean RGB and hue of contours in device (jpg)

    Arguments:
        img {ndarray} -- Image to be analyzed

    Keyword Arguments:
        spots {int} -- Number of contours to be found (default: {3})
        threshold {int} -- Minimum threshold (default: {50})

    Returns:
        list<Object> -- [ndarray, (RGB), hue)*n]
    """
    if type(src) is str:
        img = cv.imread(src)
        if img is None:
            raise ValueError("path did not lead to an image")
    elif type(src) is np.ndarray:
        img = src
    else:
        raise TypeError("src was not a string or ndarray")
    # Finding contours in grayscale version
    print(img)
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, int(threshold), 255,
                               type=0)  # Type is binary thresh
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE,
                                          cv.CHAIN_APPROX_SIMPLE)

    # Find largest three areas
    contours.sort(reverse=True, key=len)
    selected_areas = contours[0:num_contours]

    # Mask and draw
    masks = [np.zeros(imgray.shape, np.uint8) for i in range(num_contours)]
    for i in range(num_contours):
        cv.drawContours(masks[i], selected_areas[i:i + 1], -1, 255, -1)
    img_overlayed = img
    cv.drawContours(img_overlayed, selected_areas, -1, (0, 0, 255), 1)

    # Number the contours
    for i in range(num_contours):
        M = cv.moments(contours[i])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv.putText(img_overlayed, str(i), (cX, cY), cv.FONT_HERSHEY_SIMPLEX,
                   1, (0, 0, 255), 2)

    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # Return array of HSV values
    res = [img_overlayed]
    for i in range(num_contours):
        rgb = cv.mean(img_rgb, mask=masks[i])  # RGB mean of each spot
        rgb_scaled = np.divide(rgb, 255)
        hsv = colorsys.rgb_to_hsv(*rgb_scaled[0:3])
        res.append((rgb[0:3], hsv[0]))

    return res  # Returns: [ndarray, ((RGB), hue)*n]


def tenda(x, d_h_max, c_50):
    """Calculates theoretical hue using Tenda's equation, without the h_0

    Arguments:
        x {number} -- hue
        d_h_max {number} -- constant
        c_50 {number} -- constant
        h_0 {number} -- constant; obtained from actual data

    Returns:
        {number} -- Theoretical hue
    """
    return (d_h_max * x) / (c_50 + x)


def fit_curve(data, params):
    """Returns a tuple of optimized values of d_h_max and c_50

    Arguments:
        data {list} -- list of lists that stores sample data for calibration

    Returns:
        tuple -- Optimal tuple of (d_h_max, c_50)
    """

    # Import csv to df ######
    df = pd.DataFrame(data)
    df.columns = ['x', 'h']
    # d_h_max = params[0]
    # c_50 = params[1]

    # Initial values ######

    # Optimize theoretical curve (fit curve) ######
    params, params_covariance = optimize.curve_fit(tenda,
                                                   df.x.tolist(),
                                                   df.h.tolist(),
                                                   p0=params)

    return params


# TODO: add a method for reoptimizing

# data = [(0, 173.501), (10, 172.8135), (25, 175.1297505), (50, 173.7564841),
#         (100, 175.6190177), (250, 178.2062588), (500, 182.1548396),
#         (1000, 185.1032287), (5000, 187.5903869), (10000, 187.5659567)]
# d_h_max = 50
# c_50 = 25
# params = (d_h_max, c_50)

# params = fit_curve(data, params)

# a = analyze("./input/sample.jpg")
# a = analyze(1)
