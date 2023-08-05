import numpy as np
from spatial_math_mini.base import Base
from spatial_math_mini.SO3 import SO3

class SE3(Base):
    """[summary]
    SE3 class
    """
    def __init__(self, *args):
        """[summary]

        Raises:
            Exception: [description]
        """
        try:
            if len(args) == 0:
                self._qtn = np.array([1,0,0,0])
                self._t = np.zeros(3)
            elif len(args) == 1 \
                    & (type(args[0]) is np.ndarray):
                if (args[0].shape == (4,4)):
                    # The input is Transformation matrix
                    self._qtn = self._R_to_quaternion(args[0][:3,:3]) 
                    self._t = args[0][:3,-1]
                elif (args[0].shape == (3,3)):
                    # The input is Rotation matrix
                    self._qtn = self._R_to_quaternion(args[0][:3,:3]) 
                    self._t = np.zeros(3)
                else:
                    raise Exception("SE3 Initialize Error! : The input should be transformation matrix or rotation matrix")
            elif len(args) == 2:
                if (args[0].shape == (3,3))   \
                        & (len(args[1]) == 3):
                    self._qtn = self._R_to_quaternion(args[0])
                    self._t = self._check_vector(3,args[1])
                elif (args[0].shape == (4,))   \
                        & (len(args[1]) == 3):
                    self._qtn = self._check_vector(4,args[0])
                    self._t = self._check_vector(3,args[1])
            else:
                raise Exception("SE3 Initialize Error! : The input parameter should be no more than 2")
        except:
            raise Exception("SE3 Initialize Error!")

    # -- properties --
    @property
    def R(self):
        return self._quaternion_to_R(self._qtn)
    
    @R.setter
    def R(self, R):
        self._qtn = self._R_to_quaternion(R)

    @property
    def t(self):
        return self._t
    
    @t.setter
    def t(self, t):
        self._t = self._check_vector(3, t)
    
    @property
    def T(self):
        return self._quaternion_trans_to_T(self._qtn, self._t)

    @property
    def quaternion(self):
        return self._qtn

    # --Construction of Transformation Matrix--
    @staticmethod
    def random(scale=1):
        """[summary]

        Returns:
            [type]: [description]
        """
        R, _ = np.linalg.qr(np.random.randn(3,3))
        t = np.random.uniform(-1,1, size=3) * scale
        return SE3(R, t)
    
    @staticmethod
    def twistangle(twist, angle):
        """[summary]
        Construction of Transformation Matrix
        using twist and angle

        Args:
            twist (size 3 np.ndarray): unit twist axis
            angle (float): angle

        Returns:
            [SE3]: SE3 Class
        """
        qtn, t = Base._twistangle_to_quaternion_trans(twist, angle)
        return SE3(qtn, t)

    @staticmethod
    def trans(t):
        """[summary]
        Construction of Transformation Matrix
        using translation vector
        Args:
            p (size 3 np.ndarray): translation

        Returns:
            [SE3]: SE3 Class
        """
        qtn = np.array([1,0,0,0])
        t = Base._check_vector(3, t)
        return SE3(qtn, t)

    @staticmethod
    def qtn_trans(qtn, trans):
        """[summary]
        Construction of Transformation Matrix
        using quaternion, translation vector
        Args:
            qtn (size 4 np.ndarray) : quaternion
            trans (size 3 np.ndarray): translation

        Returns:
            [SE3]: SE3 Class
        """
        qtn = Base._check_vector(4, qtn)
        t = Base._check_vector(3, trans)
        return SE3(qtn, t)

    @staticmethod
    def Rx(theta, unit='rad'):
        """[summary]
        Generate SE3 Class by rotating x axis.

        Args:
            theta (float): rotation angle along the x axis.
            unit (str, optional): [rad or deg]. Defaults to 'rad'.

        Returns:
            T [SE3]: SE3 Translation Class
        """
        qtn = Base._get_quaternion_by_axis(theta, "x", unit)
        t = np.zeros(3)
        return SE3(qtn, t)

    @staticmethod
    def Ry(theta, unit='rad'):
        """[summary]
        Generate SE3 Class by rotating y axis.

        Args:
            theta (float): rotation angle along the y axis.
            unit (str, optional): [rad or deg]. Defaults to 'rad'.

        Returns:
            T [SE3]: SE3 Translation Class
        """
        qtn = Base._get_quaternion_by_axis(theta, "y", unit)
        t = np.zeros(3)
        return SE3(qtn, t)

    @staticmethod
    def Rz(theta, unit='rad'):
        """[summary]
        Generate SE3 Class by rotating z axis.

        Args:
            theta (float): rotation angle along the z axis.
            unit (str, optional): [rad or deg]. Defaults to 'rad'.

        Returns:
            T [SE3]: SE3 Translation Class
        """
        qtn = Base._get_quaternion_by_axis(theta, "z", unit)
        t = np.zeros(3)
        return SE3(qtn, t)

    # --Conversion--  
    def inv(self):
        """[summary]
        Inversion of Transformation Matrix

        Returns:
            [SE3]: Inversion of SE3 Class
        """
        SO3_ = SO3.qtn(self._qtn)
        qtn = SO3_.inv().to_qtn()
        t = - (SO3_.inv()@self._t)
        return SE3(qtn, t)
    
    def to_qtn_trans(self):
        """[summary]
        Convert SE3 to unit quaternion and translation vector. 

        Returns:
            qtn [size=4 np.ndarray]: unit quaternion array.
            trans [size=3 np.ndarray] translation vector array.
        """
        return self._qtn, self._t
    
    def to_twistangle(self):
        """[summary]
        Convert SE3 to TwistAngle. 

        Returns:
            Twist [size=6 np.ndarray]: array.
            angle (float): angle.
        """
        return self._quaternion_trans_to_twistangle(self._qtn, self._t)
    
    def to_adjoint(self):
        """ adjoint representation : Ad_T
        """
        return np.block([[self.R, np.zeros([3,3])],[Base._skew(self.t)@self.R, self.R]])
        
    #--SE3 operators--
    def __matmul__(self, X):
        return self.dot(X)

    def dot(self, X):
        if type(X) is np.ndarray:
            if X.shape == (3,):
                X = np.hstack([X,1])[:,None]
            elif X.shape == (3,1):
                X = np.vstack([X,1])
            return self.T.dot(X)[:-1]
        
        elif type(X) is SE3:
            return SE3(self.T.dot(X.T))

    def __repr__(self):
        return "SE3 Class\n"+self.T.__repr__()