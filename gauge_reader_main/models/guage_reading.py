import cv2
import numpy as np
import pandas as pd


def avg_circles(circles, b):
    avg_x = 0
    avg_y = 0
    avg_r = 0
    for i in range(b):
        # optional - average for multiple circles (can happen when a gauge is at a slight angle)
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    avg_x = int(avg_x / (b))
    avg_y = int(avg_y / (b))
    avg_r = int(avg_r / (b))
    return avg_x, avg_y, avg_r


def dist_2_pts(x1, y1, x2, y2):
    # print np.sqrt((x2-x1)^2+(y2-y1)^2)
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def get_gauge_value(file_path, min_value, max_value, scale_width=0.25, scale_height=0.25):
    # read image file
    img_original = cv2.imread(file_path)
    img = cv2.resize(img_original, None, fx=scale_width, fy=scale_height)

    # replicated image
    output = img.copy()
    output1 = img.copy()
    output2 = img.copy()
    output3 = img.copy()
    output4 = img.copy()
    output5 = img.copy()
    output6 = img.copy()

    # turn BGR to GRAY
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    width, height = gray.shape[:2]
    circle_img = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, np.array([]), 100, 50, int(height * 0.35),
                                  int(height * 0.50))
    a, b, c = circle_img.shape

    # all possible circle detections
    # for (x,y,r) in circle_img[0,:]:
    #     cv2.circle(output2, (x,y), r, (0,255,0), 3)
    #     cv2.circle(output2, (x,y), 2, (0,255,0), 3)

    # Averaging out nearby circles incase
    x, y, r = avg_circles(circle_img, b)
    cv2.circle(output3, (x, y), r, (0, 255, 0), 3)
    cv2.circle(output3, (x, y), 2, (0, 255, 0), 3)

    # Draw scale of degree on image
    separation = 10  # in degrees
    interval = int(360 / separation)
    p1 = np.zeros((interval, 2))  # set empty arrays
    p2 = np.zeros((interval, 2))
    p_text = np.zeros((interval, 2))

    for i in range(0, interval):
        for j in range(0, 2):
            if (j % 2 == 0):
                p1[i][j] = x + 0.9 * r * np.cos(separation * i * np.pi / 180)  # point for lines
            else:
                p1[i][j] = y + 0.9 * r * np.sin(separation * i * np.pi / 180)

    text_offset_x = 10
    text_offset_y = 5

    for i in range(0, interval):
        for j in range(0, 2):
            if (j % 2 == 0):
                p2[i][j] = x + r * np.cos(separation * i * np.pi / 180)
                p_text[i][j] = x - text_offset_x + 1.2 * r * np.cos(
                    (separation) * (i + 9) * np.pi / 180)  # point for text labels, i+9 rotates the labels by 90 degrees
            else:
                p2[i][j] = y + r * np.sin(separation * i * np.pi / 180)
                p_text[i][j] = y + text_offset_y + 1.2 * r * np.sin(
                    (separation) * (i + 9) * np.pi / 180)  # point for text labels, i+9 rotates the labels by 90 degrees

    # add the lines and labels to the image
    for i in range(0, interval):
        cv2.line(output3, (int(p1[i][0]), int(p1[i][1])), (int(p2[i][0]), int(p2[i][1])), (0, 255, 0), 2)
        cv2.putText(output3, '%s' % (int(i * separation)), (int(p_text[i][0]), int(p_text[i][1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1, cv2.LINE_AA)

    # Edge detection
    separation = 10  # in degrees
    interval = int(360 / separation)
    p3 = np.zeros((interval, 2))  # set empty arrays
    p4 = np.zeros((interval, 2))

    for i in range(0, interval):
        for j in range(0, 2):
            if (j % 2 == 0):
                p3[i][j] = x + 0.8 * r * np.cos(separation * i * np.pi / 180)  # point for lines
            else:
                p3[i][j] = y + 0.8 * r * np.sin(separation * i * np.pi / 180)

    canny = cv2.Canny(gray, 200, 20)
    region_of_interest_vertices = p3
    cropped_image = region_of_interest(canny, np.array([region_of_interest_vertices], np.int32))

    contours, heirarchy = cv2.findContours(cropped_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    int_cnt = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 15:
            cv2.drawContours(output3, cnt, -1, (255, 0, 0), 3)
            int_cnt.append(cnt)

            # Estimate Angle min and max
    frth_quad_index = []
    thrd_quad_index = []
    reference_zero_angle = 35
    reference_end_angle = 330
    min_angle = 90
    max_angle = 270

    for i in range(len(int_cnt)):
        a = int_cnt[i]
        a = a.reshape(len(a), 2)
        a = pd.DataFrame(a)
        x1 = a.iloc[:, 0].mean()
        y1 = a.iloc[:, 1].mean()

        xlen = x1 - x
        ylen = y - y1

        # Taking arc-tan of ylen/xlen to find the angle
        # res= np.arctan(np.divide(float(ylen), float(xlen)))
        # res= np.rad2deg(res)
        if xlen < 0 and ylen < 0:
            res = np.arctan(np.divide(float(abs(ylen)), float(abs(xlen))))
            res = np.rad2deg(res)
            final_start_angle = 90 - res
            # print(i , final_angle)
            frth_quad_index.append(i)
            if final_start_angle > reference_zero_angle:
                if final_start_angle < min_angle:
                    min_angle = final_start_angle

        elif xlen > 0 and ylen < 0:
            res = np.arctan(np.divide(float(abs(ylen)), float(abs(xlen))))
            res = np.rad2deg(res)
            final_end_angle = 270 + res
            thrd_quad_index.append(i)
            # print(i , res)
            if final_end_angle < reference_end_angle:
                if final_end_angle > max_angle:
                    max_angle = final_end_angle

    # Trial and error to see which threshold function performs best
    thresh = 150
    maxValue = 255

    th, dst2 = cv2.threshold(gray, thresh, maxValue, cv2.THRESH_BINARY_INV)

    # Line detection approach
    minLineLength = 10
    maxlineGap = 0

    lines = cv2.HoughLinesP(image=dst2, rho=3, theta=np.pi / 180, threshold=100, minLineLength=minLineLength,
                            maxLineGap=0)

    for line in lines:
        x1, x2, y1, y2 = line[0]
        cv2.line(output1, (x1, y1), (x2, y2), (0, 255, 0), 2)

    final_line_list = []
    diff1LowerBound = 0.15  # diff1LowerBound and diff1UpperBound determine how close the line should be from the center
    diff1UpperBound = 0.35
    diff2LowerBound = 0.5  # diff2LowerBound and diff2UpperBound determine how close the other point of the line should be to the outside of the gauge
    diff2UpperBound = 1.0
    for i in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            diff1 = dist_2_pts(x, y, x1, y1)  # x, y is center of circle
            diff2 = dist_2_pts(x, y, x2, y2)  # x, y is center of circle
            # set diff1 to be the smaller (closest to the center) of the two), makes the math easier
            if (diff1 > diff2):
                temp = diff1
                diff1 = diff2
                diff2 = temp
            # check if line is within an acceptable range
            if (((diff1 < diff1UpperBound * r) and (diff1 > diff1LowerBound * r) and (
                    diff2 < diff2UpperBound * r)) and (diff2 > diff2LowerBound * r)):
                line_length = dist_2_pts(x1, y1, x2, y2)
                # add to final list
                final_line_list.append([x1, y1, x2, y2])

    x1 = final_line_list[0][0]
    y1 = final_line_list[0][1]
    x2 = final_line_list[0][2]
    y2 = final_line_list[0][3]
    cv2.line(output6, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Determine final angle
    dist_pt0 = dist_2_pts(x, y, x1, y1)
    dist_pt1 = dist_2_pts(x, y, x2, y2)

    if (dist_pt0 > dist_pt1):
        xlen = x1 - x
        ylen = y - y1
    else:
        xlen = x2 - x
        ylen = y - y2

    # Taking arc-tan of ylen/xlen to find the angle
    res = np.arctan(np.divide(float(abs(ylen)), float(abs(xlen))))
    res = np.rad2deg(res)

    if xlen < 0 and ylen > 0:  # Quadrant 1
        final_angle = res + 90
    if xlen > 0 and ylen > 0:  # Quadrant 2
        final_angle = 270 - res
    if xlen > 0 and ylen < 0:  # Quadrant 3
        final_angle = 270 + res
    if xlen < 0 and ylen < 0:  # Quadrant 4
        final_angle = 90 - res

    # Read current value
    old_min = float(min_angle)
    old_max = float(max_angle)

    new_min = float(min_value)
    new_max = float(max_value)

    old_value = final_angle

    old_range = (old_max - old_min)
    new_range = (new_max - new_min)
    new_value = (((old_value - old_min) * new_range) / old_range) + new_min
    #   print(f"Reading of the Gauge is {new_value}")
    return new_value

#   cv2.rectangle(output6, (x-(r+10), y-(r+10)), (x+(r+10),y+(r+10)), (0,255,0), 3)
#   cv2.putText(output6, ('Gauge Reading: {}'.format(new_value)), (int(x-(r+14)),int(y-(r+14))), 
#                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 1, cv2.LINE_AA ) 
#   cv2.circle(output6, (x,y), 2, (0,255,0), 3)

# get_gauge_value(file_path=r"D:\DATASCI\Computer_vision\work\gauge_reader_model\value_reading\chiller_gauge.jpg",
#                 min_value=-1,
#                 max_value=3)
