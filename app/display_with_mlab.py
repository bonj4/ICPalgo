import numpy as np 
from multiprocessing import Process, Queue
from mayavi import mlab 

class Display3D(object):
    def __init__(self):
        self.state = None
        self.q = Queue()
        self.vp = Process(target=self.viewer_thread, args=(self.q,))
        self.vp.daemon = True
        self.vp.start()

    def viewer_thread(self, q):
        self.viewer_init(1024, 768)
        while True:
            self.viewer_refresh(q)

    def viewer_init(self, w, h):
        self.fig = mlab.figure(bgcolor=(0, 0, 0))

    def viewer_refresh(self, q):
        while not q.empty():
            self.state = q.get()

        # self.fig.scene.close()

    def paint(self, mapp):
        if self.q is None:
            return

        poses, pts = [], []
        # for f in mapp.frames:
        #     poses.append(f.pose)
        for p in mapp.points:
            pts.append(p)
        self.q.put((np.array(poses), np.array(pts)))

        if self.state is not None:
            self.update_points()

    def update_points(self):
        pts = self.state
        x = pts[:, 0]
        y = pts[:, 1]
        z = pts[:, 2]

        if hasattr(self, 'point'):
            self.point.mlab_source.set(x=x, y=y, z=z)
        else:
            self.point = mlab.points3d(x, y, z, color=(1, 0, 0), scale_factor=0.5)

        mlab.draw()
        