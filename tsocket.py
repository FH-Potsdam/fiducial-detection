import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import tornado.websocket
import json

import asyncio
import threading

import cv2

vid = cv2.VideoCapture(0)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
arucoParams = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, arucoParams)

classes = ["nature", "social", "garden", "water"]

id_mapping = {
   1: ["nature"],
   2: ["nature", "social"],
   3: ["nature"],
   4: ["garden"],
   5: ["water"],
   6: ["water"],
   7: ["nature"],
   8: ["garden"],
   9: ["garden", "social"],
   10: ["nature", "water"],
   11: ["social"],
   12: ["social"]
}

dimensions = {}
for c in classes:
    dimensions[c] = 0

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("client.html")

class MyWebSocket(tornado.websocket.WebSocketHandler):
    clients = []

    def check_origin(self, origin):
        return True
    
    def open(self):
        # clients must be accessed through class object!!!
        MyWebSocket.clients.append(self)
        print ("\nWebSocket opened")

    def on_message(self, message):
        print ("msg recevied", message)
        msg = json.loads(message) # todo: safety?

        # send other clients this message
        for c in MyWebSocket.clients:
          if c != self:
            c.write_message(msg)

    def on_close(self):
        print ("WebSocket closed")
        # clients must be accessed through class object!!!
        MyWebSocket.clients.remove(self)

# ['ArucoDetector', 'Board', 'CORNER_REFINE_APRILTAG', 'CORNER_REFINE_CONTOUR', 'CORNER_REFINE_NONE', 'CORNER_REFINE_SUBPIX', 'CharucoBoard', 'CharucoDetector', 'CharucoParameters', 'DICT_4X4_100', 'DICT_4X4_1000', 'DICT_4X4_250', 'DICT_4X4_50', 'DICT_5X5_100', 'DICT_5X5_1000', 'DICT_5X5_250', 'DICT_5X5_50', 'DICT_6X6_100', 'DICT_6X6_1000', 'DICT_6X6_250', 'DICT_6X6_50', 'DICT_7X7_100', 'DICT_7X7_1000', 'DICT_7X7_250', 'DICT_7X7_50', 'DICT_APRILTAG_16H5', 'DICT_APRILTAG_16h5', 'DICT_APRILTAG_25H9', 'DICT_APRILTAG_25h9', 'DICT_APRILTAG_36H10', 'DICT_APRILTAG_36H11', 'DICT_APRILTAG_36h10', 'DICT_APRILTAG_36h11', 'DICT_ARUCO_ORIGINAL', 'DetectorParameters', 'Dictionary', 'Dictionary_getBitsFromByteList', 'Dictionary_getByteListFromBits', 'GridBoard', 'RefineParameters', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'drawDetectedCornersCharuco', 'drawDetectedDiamonds', 'drawDetectedMarkers', 'extendDictionary', 'generateImageMarker', 'getPredefinedDictionary']
@asyncio.coroutine
def checkMarkers():
    while(True):
        print("checkMarkers")
        for c in classes:
            dimensions[c] = 0

        # Capture the video frame
        # by frame
        ret, image = vid.read()

        corners, ids, rejected = detector.detectMarkers(image)

        # verify *at least* one ArUco marker was detected
        if len(corners) > 0:
            # flatten the ArUco IDs list
            ids = ids.flatten()
            # loop over the detected ArUCo corners
            for markerID in ids:
            # draw the ArUco marker ID on the image
                if markerID in id_mapping:
                    for c in id_mapping[markerID]:
                        dimensions[c] += 1

        for c in MyWebSocket.clients:
            # c.write_message("markers")
            c.write_message(json.dumps({
                "type": "update",
                "data": dimensions
            }, separators=(',', ':')))

        yield from asyncio.sleep(1)

def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(checkMarkers())

def main():
    tornado_app = tornado.web.Application([
      (r"/assets/(.*)", tornado.web.StaticFileHandler, {"path": "assets"}),
      ('/', HelloHandler),
      ('/websocket', MyWebSocket),
      ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(8888)
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop,))
    t.start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()