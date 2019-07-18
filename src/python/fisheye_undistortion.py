
# python fisheye_undistortion.py
import json
import numpy as np
import cv2,time, sys

# # EkenleftCam
K = np.array([[1115.0132057585097, 0.0, 986.8091187443332], [0.0, 1109.3256894822719, 620.2772004158973], [0.0, 0.0, 1.0]])
D = np.array([[-0.10799579902203954], [-0.042908673497024374], [0.106029956400218], [-0.07717675104779038]])

DIM = (1920, 1080)
 
def undistort(img, map1,map2):
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img #cv2.imshow("undistorted", undistorted_img)

def getUndistortionMaps(K,D,balance=0.0):
    global dim1#img.shape[:2][::-1]  # dim1 is the dimension of input image to un-distort
    # Except that K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, dim1, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, dim1, cv2.CV_16SC2)
    return map1,map2
    
map1,map2 =getUndistortionMaps(K,D,balance=0.1)


 
filename = 'testvideo.avi'
# Opens the video import and sets parameters
video = cv2.VideoCapture(filename)
# Checks to see if a the video was properly imported
status = video.isOpened()


if status == True:
    FPS = video.get(cv2.CAP_PROP_FPS)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size = (int(width), int(height))
     
    frame_lapse = (1 / FPS) * 1000
    # print(width,height)

    # # Initializes the export video file
    codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')  # cv2.VideoWriter_fourcc(*'DIVX')
    video_out = cv2.VideoWriter(str(filename[:-4]) + '_undistored_f.avi', codec, FPS, size, 1)
    #
    # Initializes the frame counter
    current_frame = 0
    start = time.clock()

    #cv2.namedWindow("undistorted", cv2.WINDOW_NORMAL)

    while True:

            success, image = video.read()
            current_frame = video.get(cv2.CAP_PROP_POS_FRAMES)

            undistorted_img =undistort(image, balance=0.1)

            video_out.write(undistorted_img)

            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                    break

    video.release()
     # video_out.release()
    duration = (time.clock() - float(start)) / 60


    print('Finished undistorting the video')
    print('This video took:' + str(duration) + ' minutes')
else:
        print("Error: Video failed to load")
        sys.exit()

