import numpy as np
import matplotlib.pyplot as plt
from spatial_math_mini.SO3 import SO3
from spatial_math_mini.SE3 import SE3

class Viz:
    def __init__(self, axeslength=1, axeswidth=5, dims=None):
        self.axeslength = axeslength
        self.axeswidth = axeswidth
        self.dims = dims
        self.fig = None
        self.ax = None
        if dims is None:
            self.dims = [-1, 1]*3
        self.scale = self.dims[1] - self.dims[0]
        self.clear() #self._plot_init()
    
    def plot(self, obj, **kwargs):
        """[summary]
        """
        if self.fig is None:
            raise Exception("plot_init first")
        if type(obj) == SO3:
            R = obj.R
            t = np.zeros(3)
        elif type(obj) == SE3:
            R, t = obj.R, obj.t
        else:
            raise Exception("input is not plotable type")
        self._plot_frame(R, t, self.scale,
                    **kwargs)
        #plt.show()

    def _plot_frame(self, R, t, scale, name=None, color=None):
        """[summary]
        Draw Frame by R, t

        Args:
            R (3x3 np.ndarray): Rotation Matrix
            t (size 3 np.ndarray): Translation vector
            frame ('str', optional): the name of a frame. Defaults to None.
            dims (size 6 np.ndarray or list, optional): 
                view scope limit. Defaults to [0,10]*3.
            axeslength (int, optional): [description]. Defaults to 1.
            axeswidth (int, optional): [description]. Defaults to 5.
        """
        if color is None:
            if name is None:
                colors = ['gray']*3
            else:
                colors = ['r','g','b']
        else:
            colors = color*3

        for i in range(3):
            axis = np.vstack([t, t+R[:3,i]*self.axeslength]).T 
            self.ax.plot(axis[0], axis[1], axis[2], 
                color=colors[i], linewidth=self.axeswidth)

        frame_name_offset = [-0.01, -0.01, -0.01]
        frame_name_pos = R.dot(scale*np.array(frame_name_offset).T)+t
        if name is not None:
            self.ax.text(*frame_name_pos, "{{{}}}".format(name))
        

    def plot_frame_0(self):
        self._plot_frame(np.eye(3), np.zeros(3), self.scale,
                    color='k')

    def clear(self):
        if self.ax is None:
            self.fig = plt.figure()
            self.ax = plt.axes(projection='3d')
        self.ax.clear()
        self.ax.set_xlim3d(self.dims[:2])
        self.ax.set_ylim3d(self.dims[2:4])
        self.ax.set_zlim3d(self.dims[4:])
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')
    
        self.plot_frame_0()

# # Check if there is a 3d figure
# is_3d_plot = False
# if len(plt.get_fignums()) != 0:
#     fig = plt.gcf()
#     if len(fig.axes) != 0:
#         ax = plt.gca()
#         if ax.__class__.__name__ == "Axes3DSubplot":
#             is_3d_plot = True

# # if there is no 3d figure, make one.
# if not is_3d_plot:
#     plot3d_init(dims)

if __name__ == "__main__":
    SE3_1 = SE3.random(scale=0.1)
    SE3_2 = SE3.random(scale=0.1)
    v = Viz(axeslength=0.1, axeswidth=1)
    v.plot(SE3_1)
    v.plot(SE3_2)
    v.clear()

    #plt.show()
    input()
