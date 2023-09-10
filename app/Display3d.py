import cv2
import OpenGL.GL as gl
import pangolin
import numpy as np
from multiprocessing import Process, Queue


# please check the following link for more details
# https://github.com/geohot/twitchslam/blob/master/display.py
class Display3D(object):
    def __init__(self):
        self.state = None
        self.q = Queue()
        self.vp = Process(target=self.viewer_thread, args=(self.q,))
        self.vp.daemon = True
        self.vp.start()

    def viewer_thread(self, q):
        self.viewer_init(1024, 768)
        while not pangolin.ShouldQuit():
            self.viewer_refresh(q)

    def viewer_init(self, w, h):
        pangolin.CreateWindowAndBind('Map Viewer', w, h)
        gl.glEnable(gl.GL_DEPTH_TEST)

        self.scam = pangolin.OpenGlRenderState(
            pangolin.ProjectionMatrix(w, h, 420, 420, w // 2, h // 2, 0.2, 10000),
            pangolin.ModelViewLookAt(0, -10, -8,
                                     0, 0, 0,
                                     0, -1, 0))
        self.handler = pangolin.Handler3D(self.scam)

        # Create Interactive View in window
        self.dcam = pangolin.CreateDisplay()
        self.dcam.SetBounds(0.0, 1.0, 0.0, 1.0, w / h)
        self.dcam.SetHandler(self.handler)
        # hack to avoid small Pangolin, no idea why it's *2
        self.dcam.Resize(pangolin.Viewport(0, 0, w * 2, h * 2))
        self.dcam.Activate()
        # Add axes rendering
        self.axis = pangolin.Renderable()
        self.axis.Add(pangolin.Axis())

    def viewer_refresh(self, q):
        while not q.empty():
            self.state = q.get()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.dcam.Activate(self.scam)

        if self.state is not None:
            if self.state[0].shape[0] != 0:
                # draw keypoints
                gl.glPointSize(5)
                gl.glColor3f(1.0, 0.0, 0.0)
                pangolin.DrawPoints(self.state[0], self.state[1])
        # Draw axes
        self.axis.Render()
        pangolin.FinishFrame()

    def paint(self, pts: list, clrs: list):

        if self.q is None:
            return

        points = np.concatenate(pts, axis=0)
        colors = np.concatenate(clrs, axis=0)
        self.q.put((points, colors))

    def close(self):
        if self.q is not None:
            self.q.close()
            self.q.join_thread()
        self.vp.terminate()
        self.vp.join()


# if __name__ == '__main__':
#     import time
#     d = Display3D()
#     corners1 = np.array([[10, 0, 0],  # bottom left
#                         [20, 0, 0],  # top left
#                         [10, 10, 0],  # bottom right
#                         [20, 20, 0],  # top right
#                         ])
#     corners2 = np.array([[-10, 0, 0],  # bottom left
#                         [-20, 0, 0],  # top left
#                         [-10, 10, 0],  # bottom right
#                         [-20, 20, 0],  # top right
#                         ])
#     print(corners1.shape)
#     colors1=np.array([[1,1,0],
#                     [1,1,0],
#                     [1,1,0],
#                     [1,1,0]])
#     colors2=np.array([[0,1,0],
#                     [0,1,0],
#                     [0,1,0],
#                     [0,1,0]])
#     while 1:
#         d.paint([corners1,corners2], [colors1 ,colors2 ])
#         time.sleep(1)
#     d.close()

if __name__ == '__main__':
    import time

    d = Display3D()
    while 1:
        corners1 = np.random.random((1000, 3)) * 10
        corners2 = np.random.random((1000, 3)) * 10
        colors1 = np.random.random((1000, 3))
        colors2 = np.random.random((1000, 3))
        d.paint([corners1, corners2], [colors1, colors2])
        time.sleep(0.1)
