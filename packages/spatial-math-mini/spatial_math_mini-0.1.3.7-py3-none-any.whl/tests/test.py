import unittest
import numpy as np
from spatial_math_mini.SO3 import SO3
from spatial_math_mini.SE3 import SE3
from spatial_math_mini.base import Base

class BaseTest(unittest.TestCase):
    def test_quaternion_R(self):
        qtn = np.random.random(4)
        qtn = qtn/np.linalg.norm(qtn)
        R = Base._quaternion_to_R(qtn)
        qtn_ = Base._R_to_quaternion(R)
        R_ = Base._quaternion_to_R(qtn_)
        is_same = np.allclose(R, R_)
        self.assertTrue(is_same)

    def test_axisangle_R(self):
        qtn = np.random.random(4)
        qtn = qtn/np.linalg.norm(qtn)
        R = Base._quaternion_to_R(qtn)
        axis, angle = Base._R_to_axisangle(R)
        R_ = Base._axisangle_to_R(axis,angle)
        is_same = np.allclose(R, R_)
        self.assertTrue(is_same)
    
    def test_quaternion_axisangle(self):
        qtn = np.random.random(4)
        qtn = qtn/np.linalg.norm(qtn)
        axis, angle = Base._quaternion_to_axisangle(qtn)
        qtn_ = Base._axisangle_to_quaternion(axis, angle)
        axis_, angle_ = Base._quaternion_to_axisangle(qtn_)
        self.assertTrue(np.allclose(angle_, angle))
        self.assertTrue(np.allclose(axis_, axis))
    
    def test_twistangle_to_qtn_trans(self):
        qtn = np.random.random(4)
        qtn = qtn/np.linalg.norm(qtn)
        t = np.random.random(3)
        tw, angle = Base._quaternion_trans_to_twistangle(qtn, t)
        qtn_, t_ = Base._twistangle_to_quaternion_trans(tw, angle)
        tw_, angle_ = Base._quaternion_trans_to_twistangle(qtn_, t_)
        self.assertTrue(np.allclose(angle_, angle))
        self.assertTrue(np.allclose(tw_, tw))

    def test_rpy_to_qtn(self):
        qtn = SO3.random()._qtn
        rpy = Base._quaternion_to_rpy(qtn)
        qtn_ = Base._rpy_to_quaternion(rpy)
        self.assertTrue(np.allclose(qtn, qtn_), True)


class SO3Test(unittest.TestCase):
    def isSO3(self, SO3_):
        #it also tests @ operator
        I = np.eye(3)
        I_ = (SO3_ @ SO3_.inv()).R
        return np.allclose(I,I_)

    def test_construct_random(self):
        SO3_ = SO3.random()
        self.assertTrue(self.isSO3(SO3_))
    
    def test_construct_axisangle(self):
        axislist = np.eye(3)
        for omega in axislist:
            SO3_ = SO3.axisangle(omega,1)
        self.assertTrue(self.isSO3(SO3_))

    def test_construct_quaternion(self):
        sqrt2 = np.sqrt(2)
        SO3_ = SO3.qtn([sqrt2,sqrt2, 0, 0])
        self.assertTrue(self.isSO3(SO3_))

    def test_construct_Rxyz(self):
        SO3_ = SO3.Rx(np.pi/2)
        self.assertTrue(self.isSO3(SO3_))
        SO3_ = SO3.Ry(np.pi/2)
        self.assertTrue(self.isSO3(SO3_))
        SO3_ = SO3.Rx(np.pi/2)
        self.assertTrue(self.isSO3(SO3_))

    def test_inv(self):
        SO3_1 = SO3.random()
        SO3_2 = SO3_1.inv().inv()
        isEqual = np.allclose(SO3_1.R, SO3_2.R)
        self.assertTrue(isEqual)
    

class SE3Test(unittest.TestCase):
    def isSE3(self, SE3_):
        I = np.eye(4)
        R = SE3_.R
        t = SE3_.t
        SE3_inv = SE3(R, t).inv()
        I_ = (SE3_ @ SE3_inv).T
        return np.allclose(I, I_)

    def test_construct_random(self):
        SE3_ = SE3.random()
        self.assertTrue(self.isSE3(SE3_))

    def test_construct_twistangle(self):
        Slist = np.eye(6)
        for S in Slist:
            T = SE3.twistangle(S, 1)
            self.assertTrue(self.isSE3(T))
    
    def test_construct_qtn_trans(self):
        qtn = [0.7071,0.7071, 0, 0]
        trans = np.random.rand(3)
        T = SE3.qtn_trans(qtn, trans)
        self.assertTrue(self.isSE3(T))

    def test_construct_Rxyz(self):
        SE3_x = SE3.Rx(np.pi/2)
        self.assertTrue(self.isSE3(SE3_x))
        SE3_y = SE3.Ry(np.pi/2)
        self.assertTrue(self.isSE3(SE3_y))
        SE3_z = SE3.Rz(np.pi/2)
        self.assertTrue(self.isSE3(SE3_z))
    
    def test_adjoint(self):
        SE3_x = SE3.Rx(np.pi/2)
        self.assertTrue(SE3_x.to_adjoint().shape == (6,6))#

    def test_construct_trans(self):
        TransList = np.random.rand(5,3)
        for trans in TransList:
            SE3_trans = SE3.trans(trans)
            self.assertTrue(self.isSE3(SE3_trans))

    def test_inv(self):
        SE3_1 = SE3.random()
        SE3_2 = SE3_1.inv().inv()
        isEqual = np.allclose(SE3_1.T, SE3_2.T)
        self.assertTrue(isEqual)
    
    def test_dot(self):
        vlist = []
        vlist.append(np.random.rand(4,1))
        vlist.append(np.random.rand(3))
        vlist.append(np.random.rand(3,1))
        vlist.append(np.random.rand(4,4))
        vlist.append(SE3())
        for v in vlist:
            SE3().dot(v)
    
    def test_print(self):
        print(SE3())

if __name__ == '__main__':
    unittest.main()