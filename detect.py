import cv2

vid = cv2.VideoCapture(0)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
arucoParams = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, arucoParams)

# ['ArucoDetector', 'Board', 'CORNER_REFINE_APRILTAG', 'CORNER_REFINE_CONTOUR', 'CORNER_REFINE_NONE', 'CORNER_REFINE_SUBPIX', 'CharucoBoard', 'CharucoDetector', 'CharucoParameters', 'DICT_4X4_100', 'DICT_4X4_1000', 'DICT_4X4_250', 'DICT_4X4_50', 'DICT_5X5_100', 'DICT_5X5_1000', 'DICT_5X5_250', 'DICT_5X5_50', 'DICT_6X6_100', 'DICT_6X6_1000', 'DICT_6X6_250', 'DICT_6X6_50', 'DICT_7X7_100', 'DICT_7X7_1000', 'DICT_7X7_250', 'DICT_7X7_50', 'DICT_APRILTAG_16H5', 'DICT_APRILTAG_16h5', 'DICT_APRILTAG_25H9', 'DICT_APRILTAG_25h9', 'DICT_APRILTAG_36H10', 'DICT_APRILTAG_36H11', 'DICT_APRILTAG_36h10', 'DICT_APRILTAG_36h11', 'DICT_ARUCO_ORIGINAL', 'DetectorParameters', 'Dictionary', 'Dictionary_getBitsFromByteList', 'Dictionary_getByteListFromBits', 'GridBoard', 'RefineParameters', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'drawDetectedCornersCharuco', 'drawDetectedDiamonds', 'drawDetectedMarkers', 'extendDictionary', 'generateImageMarker', 'getPredefinedDictionary']

while(True):
      
    # Capture the video frame
    # by frame
    ret, image = vid.read()

    corners, ids, rejected = detector.detectMarkers(image)

    # verify *at least* one ArUco marker was detected
    if len(corners) > 0:
      # flatten the ArUco IDs list
      ids = ids.flatten()
      # loop over the detected ArUCo corners
      for (markerCorner, markerID) in zip(corners, ids):
        # extract the marker corners (which are always returned in
        # top-left, top-right, bottom-right, and bottom-left order)
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        # convert each of the (x, y)-coordinate pairs to integers
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))

        # draw the bounding box of the ArUCo detection
        cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
        # compute and draw the center (x, y)-coordinates of the ArUco
        # marker
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
        # draw the ArUco marker ID on the image
        cv2.putText(image, str(markerID),
          (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
          0.5, (0, 255, 0), 2)
        print("[INFO] ArUco marker ID: {}".format(markerID))
        # show the output image
  
    # Display the resulting frame
    cv2.imshow("Image", image)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()