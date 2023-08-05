import numpy as np
from abc import ABC

class Base(ABC):
    """[summary]
    Collection of Basic functions.
    """
    def __init__(self):
        pass

    @staticmethod
    def _check_vector(vector_len, v):
        """[summary]
        Check if vector is specified shape.
        List will be converted to a np.ndarray
        Args:
            vector_len (int): The length of a vector.
            v (list or np.ndarray): target vector.

        Returns:
            v [np.ndarray]: vector.
        """
        if (type(v) is list) | (type(v) is tuple):
            v = np.array(v)
        elif (type(v) is np.ndarray)\
                & (v.shape == (vector_len,1)):
            v = v.flatten()
        assert v.shape == (vector_len,)
        return v

    @staticmethod
    def _check_matrix(matrix_len, m):
        """[summary]
        Check if matrix is specified shape.

        Args:
            matrix_len (int): The one-side length of a matrix.
            m (list or np.ndarray): target matrix.

        Returns:
            m [np.ndarray]: matrix.
        """
        assert m.shape == (matrix_len, matrix_len)
        return m
    
    @staticmethod
    def _skew(x):
        """[summary]
        Make a skew-symmetric matrix of a vector.
        Args:
            x (list or np.ndarray): vector

        Returns:
            [np.ndarray]: skew-symmetric matrix of a vector.
        """
        x = Base._check_vector(3, x)
        return np.array([[0    , -x[2], x[1] ],
                        [x[2] , 0    , -x[0]],
                        [-x[1], x[0] , 0    ]])
    
    @staticmethod
    def _quaternion_to_R(qtn):
        """[summary]
        Convert Quaternion to Rotation matrix 
        Args:
            qtn (size3 np.ndarray): quaternion

        Returns:
            [3x3 np.ndarray]: Rotation Matrix
        """
        qtn = Base._check_vector(4, qtn)
        qtn_norm = np.linalg.norm(qtn)
        if qtn_norm != 1:
            w, x, y, z = qtn/qtn_norm
        else:
            w, x, y, z = qtn
        return np.array([[1-2*y**2-2*z**2, 2*x*y-2*w*z, 2*x*z+2*w*y],
                         [2*x*y+2*w*z, 1-2*x**2-2*z**2, 2*y*z-2*w*x],
                         [2*x*z-2*w*y, 2*y*z+2*w*x, 1-2*x**2-2*y**2]])
    
    @staticmethod
    def _R_to_quaternion(R):
        """[summary]
        Convert rotation matrix to unit quaternion

        Args:
            R (3x3 np.ndarray): Rotation matrix.

        Returns:
            qtn [size 3 np.ndarray]: Unit quaternion.
        """
        tr = np.trace(R)
        if tr > 0.:
            s = np.sqrt(tr+1.)*2
            w = 0.25*s
            x = (R[2,1] - R[1,2])/s
            y = (R[0,2] - R[2,0])/s
            z = (R[1,0] - R[0,1])/s
        elif (R[0,0]>R[1,1]) & (R[0,0] > R[2,2]):
            s= np.sqrt(1. + R[0,0] - R[1,1] - R[2,2]) * 2
            w = (R[2,1] - R[1,2]) / s
            x = 0.25 * s
            y = (R[0,1] + R[1,0]) / s; 
            z = (R[0,2] + R[2,0]) / s; 
        elif R[1,1] > R[2,2]:
            s= np.sqrt(1. + R[1,1] - R[0,0] - R[2,2]) * 2 
            w = (R[0,2] - R[2,0]) / s
            x = (R[0,1] + R[1,0]) / s
            y = 0.25 * s
            z = (R[1,2] + R[2,1]) / s
        else:
            s = np.sqrt(1. + R[2,2] - R[1,1] - R[0,0]) * 2
            w = (R[1,0] - R[0,1]) / s
            x = (R[0,2] + R[2,0]) / s
            y = (R[1,2] + R[2,1]) / s
            z = 0.25 * s
        return np.array([w,x,y,z])
    
    @staticmethod
    def _axisangle_to_R(axis, angle):
        """[summary]
        Convert AxisAngle to Rotation Matrix.
        (Exponential of SO3)
        Args:
            axis (size3 np.ndarray or list): unit vector of rotation axis
            angle (float): rotation angle

        Returns:
            R [3x3 np.ndarray]: rotation matrix
        """
        axis = Base._check_vector(3, axis)

        if angle == 0.:
            return np.eye(3)
        axis_norm = np.linalg.norm(axis)
        if axis_norm != 1.:
            axis = axis/axis_norm
        
        theta = angle
        omega_hat = axis
        return np.eye(3) \
           + np.sin(theta)*Base._skew(omega_hat) \
           + (1-np.cos(theta))*Base._skew(omega_hat).dot(Base._skew(omega_hat))

    @staticmethod
    def _R_to_axisangle(R):
        """[summary]
        Convert rotation matrix to unit quaternion
        (logarithm of SO3)

        Args:
            R (3x3 np.ndarray): Rotation matrix.

        Returns:
            axis [size 3 np.ndarray]: Unit axis.
            angle (float): rotation angle
        """
        R = Base._check_matrix(3, R)

        if np.allclose(R, np.eye(3)):
            # no rotation
            axis = np.array([1., 0., 0.])
            angle = 0.
        elif np.trace(R) == -1:
            # angle is 180 degrees
            angle = np.pi
            if R[0,0] != -1:
                axis = 1/np.sqrt(2*(1+R[0,0])) * np.array([1+R[0,0], R[1,0], R[2,0]])
            elif R[1,1] != -1:
                axis = 1/np.sqrt(2*(1+R[1,1])) * np.array([R[0,1], 1+R[1,1], R[2,1]])
            else:
                axis = 1/np.sqrt(2*(1+R[2,2])) * np.array([R[0,2], R[1,2], 1+R[2,2]])
        else:
            angle = np.arccos(1/2*(np.trace(R)-1))
            axis = 1/(2*np.sin(angle))*np.array([R[2,1]-R[1,2], R[0,2]-R[2,0], R[1,0]-R[0,1]])
        return axis, angle

    @staticmethod
    def _quaternion_to_axisangle(qtn):
        """[summary]
        Convert quaternion to axisangle

        Args:
            qtn (np.ndarray(4)): unit quaternion

        Returns:
            axis [size 3 np.ndarray]: Unit axis.
            angle (float): rotation angle
        """
        qtn = Base._check_vector(4, qtn)
        if qtn[0] > 1:
            qtn = qtn/np.linalg.norm(qtn) #normalize
        w, x, y, z = qtn
        angle = 2 * np.arccos(w)
        s = np.sqrt(1-w**2)
        if s < 0.00001:
            axis = np.array([x, y, z])
            return axis, angle
        else:
            axis = np.array([x, y, z])
            axis = axis/np.linalg.norm(axis)
            return axis, angle
        
    @staticmethod
    def _axisangle_to_quaternion(axis, angle):
        """[summary]
        Convert axisangle to quaternion

        Args:
            axis [size 3 np.ndarray]: Unit axis.
            angle (float): rotation angle

        Returns:
            qtn (np.ndarray(4)): unit quaternion
            
        """
        axis = Base._check_vector(3, axis)
        s = np.sin(angle/2)
        w = np.cos(angle/2)
        x, y, z = axis * s
        return np.array([w,x,y,z])

    @staticmethod    
    def _Rt_to_T(R, t):
        """[summary]

        Args:
            R ([type]): [description]
            p ([type]): [description]

        Returns:
            [type]: [description]
        """
        R = Base._check_matrix(3, R)
        t = Base._check_vector(3, t)
        return np.block([[R,       t[:,None]],
                         [np.zeros((1,3)), 1]])

    @staticmethod              
    def _T_to_Rt(T):
        """[summary]

        Args:
            T ([type]): [description]

        Returns:
            [type]: [description]
        """
        T = Base._check_matrix(4, T)
        R, t = T[:3,:3], T[:3,3]
        return R, t
    
    @staticmethod    
    def _quaternion_trans_to_T(qtn, t):
        """[summary]

        Args:
            qtn ([type]): [description]
            t ([type]): [description]

        Returns:
            [type]: [description]
        """
        R = Base._quaternion_to_R(qtn)
        t = Base._check_vector(3, t)
        return np.block([[R,       t[:,None]],
                         [np.zeros((1,3)), 1]])

    @staticmethod
    def _Rt_to_twistangle(R, t):
        """[summary]

        Args:
            T ([type]): [description]

        Returns:
            [type]: [description]
        """
        T = Base._Rt_to_T(R, t)
        if np.allclose(T, np.eye(4)):
            tw = np.array([1.,0.,0.,0.,0.,0])
            theta = 0
        elif np.allclose(R, np.eye(3)):
            # pure translation
            omega = np.zeros(3)
            theta = np.linalg.norm(t)
            v = t/theta
            tw = np.hstack([omega, v])
        else:
            omega, theta = Base._R_to_axisangle(R)
            Ginv = 1/theta*np.eye(3) \
                - 1/2*Base._skew(omega) \
                + (1/theta-1/2/np.tan(theta/2))*Base._skew(omega).dot(Base._skew(omega))
            v = Ginv.dot(t)
            tw = np.hstack([omega, v])
        return tw, theta
    
    @staticmethod
    def _twistangle_to_Rt(tw, angle):
        """[summary]
        Convert Twist-angle to R, p

        Args:
            tw (size:6 np.ndarray): twist
            angle (float) : angle

        Returns:
            [type]: [description]
        """
        tw = Base._check_vector(6, tw)
        omega, v = tw[:3], tw[3:]
        theta = angle
        G = np.eye(3)*theta \
            + (1-np.cos(theta))*Base._skew(omega) \
            + (theta-np.sin(theta))*Base._skew(omega).dot(Base._skew(omega))

        if np.linalg.norm(omega) == 0:
            R = np.eye(3)
            t = v*theta
        else:
            R = Base._axisangle_to_R(omega, theta)
            t = G.dot(v)
        
        return R, t

    @staticmethod
    def _quaternion_trans_to_twistangle(qtn, t):
        """[summary]

        Args:
            T ([type]): [description]

        Returns:
            [type]: [description]
        """
        qtn = Base._check_vector(4, qtn)
        t = Base._check_vector(3, t)

        if np.allclose(qtn, [1,0,0,0]):
            if np.allclose(np.linalg.norm(t),0):
                #identity
                tw = np.array([1.,0.,0.,0.,0.,0.])
                theta = 0
            else:
                # pure translation
                omega = np.zeros(3)
                theta = np.linalg.norm(t)
                v = t/theta
                tw = np.hstack([omega, v])
        else:
            omega, theta = Base._quaternion_to_axisangle(qtn)
            Ginv = 1/theta*np.eye(3) \
                - 1/2*Base._skew(omega) \
                + (1/theta-1/2/np.tan(theta/2))*Base._skew(omega).dot(Base._skew(omega))
            v = Ginv.dot(t)
            tw = np.hstack([omega, v])
        return tw, theta
    
    @staticmethod
    def _twistangle_to_quaternion_trans(tw, angle):
        """[summary]
        Convert Twist-angle to R, p

        Args:
            tw (size:6 np.ndarray): twist
            angle (float) : angle

        Returns:
            [type]: [description]
        """
        R, t = Base._twistangle_to_Rt(tw, angle)
        qtn = Base._R_to_quaternion(R)
        return qtn, t
    
    #--private functions--
    @staticmethod
    def _get_quaternion_by_axis(theta, axis, unit="rad"):
        """[summary]
        private function to make quaternion
        using a specified axis and an angle.

        Args:
            theta (float): rotation angle
            axis (str): ["x", "y", "z"] axis name string
            unit (str, optional): ["rad", "deg"]. Defaults to "rad".

        Raises:
            Exception: if unit is neither "rad" nor "deg".

        Returns:
            qtn [np.ndarray(4)]: quaternion
        """
        if unit == "rad":
            pass
        elif unit == "deg":
            theta = theta/180.*np.pi
        else: 
            raise Exception("Wrong unit!")
        
        if axis == "x":
            omega = np.array([1,0,0]) 
        elif axis == "y":
            omega = np.array([0,1,0]) 
        elif axis == "z":
            omega = np.array([0,0,1])
        return Base._axisangle_to_quaternion(omega, theta)