
import pyqtgraph as pg
import numpy as np
pg.mkQApp()
w = pg.GraphicsLayoutWidget()
w.show()
vb = w.addViewBox()
img = pg.ImageItem(np.random.normal(size=(100,100)))
vb.addItem(img)


def mouse_moved(pos):
    print("Image position:", img.mapFromScene(pos))


w.scene().sigMouseMoved.connect(mouse_moved)
