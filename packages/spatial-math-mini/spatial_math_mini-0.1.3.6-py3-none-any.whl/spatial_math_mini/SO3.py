import numpy as np
from spatial_math_mini.base import Base

class SO3(Base):
    """[summary]
    SO3 class
    """
    def __init__(self, *args):
        """[summary]
        Initialize SO3 Class
        Raises:
            Exception: [description]
        """
        if len(args) == 0:
            self._qtn = np.array([1,0,0,0])
            
        elif (len(args) == 1) \
                & (type(args[0]) is np.ndarray):
            if args[0].shape == (3,3):
                self.R = args[0] #input is 3x3 matrix
            elif args[0].shape == (4,):
                self._qtn = args[0] / np.linalg.norm(args[0])
            else:
                Exception("SO3 Initialize Error! : input is not R or qtn")
        else:
            raise Exception("SO3 Initialize Error! : the number of input should be one")
        
        # this is just for compatibility for plotting.
        #self.p = np.zeros(3) 
    
    # -- properties --
    @property
    def R(self):
        return self._quaternion_to_R(self._qtn)
    
    @R.setter
    def R(self, R):
        self._qtn = self._R_to_quaternion(R)

    # --Construction of Rotation Matrix--
    @staticmethod
    def random(dist="uniform"):
        """[summary]
        Uniform Random Generation of SO3
        ref : "Effective Sampling and Distance Metrics for 3D Rigid Body Path Planning", ICRA 2004

        Returns:
            R [SO3]: SO3 Rotation Class
        """
        if dist == "uniform":
            qtn = SO3._uniform_sampling_quaternion()
        return SO3(qtn)

    @staticmethod
    def axisangle(axis, angle):
        """[summary]
        Generate SO3 Class using an AxisAngle.

        Args:
            axis (size=3, np.ndarray or list): 
                Axis
            angle (float): Angle

        Returns:
            R [SO3]: SO3 Rotation Class
        """
        qtn = SO3._axisangle_to_quaternion(axis, angle)
        return SO3(qtn)
    
    @staticmethod
    def qtn(qtn):
        """[summary]
        Generate SO3 Class using an unit quaternion.

        Args:
            qtn (size=4, np.ndarray or list): 
                unit quaternion. 

        Returns:
            R [SO3]: SO3 Rotation Class
        """
        qtn = Base._check_vector(4,qtn)
        return SO3(qtn)
    
    @staticmethod
    def Rx(theta, unit='rad'):
        """[summary]
        Generate SO3 Class by rotating x axis.

        Args:
            theta (float): rotation angle along the x axis.
            unit (str, optional): [rad or deg]. Defaults to 'rad'.

        Returns:
            R [SO3]: SO3 Rotation Class
        """
        return SO3(SO3._get_quaternion_by_axis(theta, "x", unit))

    @staticmethod
    def Ry(theta, unit='rad'):
        """[summary]
        Generate SO3 Class by rotating y axis.

        Args:
            theta (float): rotation angle along the y axis.
            unit (str, optional): [rad or deg]. Defaults to 'rad'.

        Returns:
            R [SO3]: SO3 Rotation Class
        """
        return SO3(SO3._get_quaternion_by_axis(theta, "y", unit))

    @staticmethod
    def Rz(theta, unit='rad'):
        """[summary]
        Generate SO3 Class by rotating z axis.

        Args:
            theta (float): rotation angle along the z axis.
            unit (str, optional): [rad or deg]. Defaults to 'rad'.

        Returns:
            R [SO3]: SO3 Rotation Class
        """
        return SO3(SO3._get_quaternion_by_axis(theta, "z", unit))
    
    # --Conversion--   
    def inv(self):
        """[summary]
        Inverse of SO3. It's just transpose.

        Returns:
            R [SO3]: SO3 Rotation Class
        """
        w, x, y, z = self._qtn
        return SO3(np.array([w, -x, -y, -z]))
 
    def to_qtn(self):
        """[summary]
        Convert SO3 to unit quaternion. 

        Returns:
            qtn [size=4 np.ndarray]: unit quaternion array.
        """
        return self._qtn
    
    def to_axisangle(self):
        """[summary]
        Convert SO3 to AxisAngle. 

        Returns:
            axis [size=3 np.ndarray]: array.
            angle (float): angle.
        """
        return self._quaternion_to_axisangle(self._qtn)

    #--math--
    @staticmethod
    def _uniform_sampling_quaternion():
        raise NotImplementedError("No use uniform sampling quaternion")
        s = np.random.random()
        sigma1, sigma2 = np.sqrt(1-s), np.sqrt(s)
        theta1, theta2 = np.random.uniform(size=2)
        s1, c1 = np.sin(theta1), np.cos(theta1)
        s2, c2 = np.sin(theta2), np.cos(theta2)
        qtn = np.array([c2*sigma2, s1*sigma1, c1*sigma1, s2*sigma2])
        return qtn

    @staticmethod
    def _uniform_sampling_rpy():
        rnd = np.random.random(4)
        roll = 2*np.pi*rnd[0] - np.pi
        pitch = np.arccos(1 - 2*rnd[1]) + np.pi/2
        if rnd[2] < 1/2:
            if pitch < np.pi:
                pitch += np.pi
            else:
                pitch -= np.pi
        if pitch > np.pi:
            pitch -= np.pi*2
        yaw = 2*np.pi*rnd[3] - np.pi
        return np.array([roll, pitch, yaw])

    #--SO3 operators--
    def __matmul__(self, X):
        return self.dot(X)

    def dot(self, X):
        if type(X) is np.ndarray:
            if len(X) == 3:
                return self.R @ X
                
        elif type(X) is SO3:
            w1, v1 = self._qtn[0], self._qtn[1:]
            w2, v2 = X._qtn[0], X._qtn[1:]
            qtn = np.array([w1*w2-v1@v2, *(w1*v2 + w2*v1 + np.cross(v1, v2))])
            return SO3(qtn)

    def __repr__(self):
        return "SO3 Class\n"+self.R.__repr__()