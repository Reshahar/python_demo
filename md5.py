# -*- coding:utf-8 -*-
import math

class Md5Hash(object):

    """变形md5类"""
    __shi_1 = (7,12,17,22)*4
    __shi_2 = (5,9,14,20)*4
    __shi_3 = (4,11,16,23)*4
    __shi_4 = (6,10,15,21)*4

    __m_1 = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
    __m_2 = (1,6,11,0,5,10,15,4,9,14,3,8,13,2,7,12)
    __m_3 = (5,8,11,14,1,4,7,10,13,0,3,6,9,12,15,2)
    __m_4 = (0,7,14,5,12,3,10,1,8,15,6,13,4,11,2,9)

    def __init__(self, A=0x67452301,B=0xefcdab89,C=0x98badcfe,D=0x10325476,size_32=True,upper=False):
        self.__A = '0x%x' %A
        self.__B = '0x%x' %B
        self.__C = '0x%x' %C
        self.__D = '0x%x' %D
        self.__F = lambda x,y,z:((x&y)|((~x)&z))
        self.__G = lambda x,y,z:((x&z)|(y&(~z)))
        self.__H = lambda x,y,z:(x^y^z)
        self.__I = lambda x,y,z:(y^(x|(~z)))
        self.__L = lambda x,n:(((x<<n)|(x>>(32-n)))&(0xffffffff))
        self.__Ti_count = 1
        self.__upper = upper
        self.__size = size_32


    def __T(self,i):
        result = (int(4294967296*abs(math.sin(i))))&0xffffffff
        return result


    def __shift(self,shift_list):
        shift_list = [shift_list[3],shift_list[0],shift_list[1],shift_list[2]]
        return shift_list

    def __fun(self,fun_list,f,m,shi):
        count = 0
        global Ti_count
        while count<16:
            xx = int(fun_list[0],16)+f(int(fun_list[1],16),int(fun_list[2],16),int(fun_list[3],16))+int(m[count],16)+self.__T(self.__Ti_count)
            xx = xx&0xffffffff
            ll = self.__L(xx,shi[count])
            fun_list[0] = hex((int(fun_list[1],16) + ll)&(0xffffffff))[:-1]
            fun_list = self.__shift(fun_list)
            count += 1
            self.__Ti_count += 1
        return fun_list

    def __genM16(self,order,ascii_list,f_offset):
        ii = 0
        m16 = [0]*16
        f_offset = f_offset*64
        for i in order:
            i = i*4
            m16[ii] = '0x'+''.join((ascii_list[i+f_offset]+ascii_list[i+1+f_offset]+ascii_list[i+2+f_offset]+ascii_list[i+3+f_offset]).split('0x'))
            ii += 1
        for c in m16:
            ind = m16.index(c)
            m16[ind] = self.__reverse_hex(c)
        return m16

    def __reverse_hex(self,hex_str):
        hex_str = hex_str[2:]
        hex_str_list = []
        for i in range(0,len(hex_str),2):
            hex_str_list.append(hex_str[i:i+2])
        hex_str_list.reverse()
        hex_str_result = '0x' + ''.join(hex_str_list)
        return hex_str_result

    def __show_result(self,f_list):
        result = ''
        f_list1 = [0]*4
        for i in f_list:
            f_list1[f_list.index(i)] = self.__reverse_hex(i)[2:]
            result = result + f_list1[f_list.index(i)]
        return result
        
    def get_md5(self,input_m):
        abcd_list = [self.__A,self.__B,self.__C,self.__D]
        
        ascii_list = map(hex,map(ord,input_m))
        msg_lenth = len(ascii_list)*8
        ascii_list.append('0x80')

        while (len(ascii_list)*8+64)%512 != 0:
            ascii_list.append('0x00')

        msg_lenth_0x = hex(msg_lenth)[2:]
        msg_lenth_0x = '0x' + msg_lenth_0x.rjust(16,'0')
        msg_lenth_0x_big_order = self.__reverse_hex(msg_lenth_0x)[2:]
        msg_lenth_0x_list = []
        for i in range(0,len(msg_lenth_0x_big_order),2):
            msg_lenth_0x_list.append('0x'+ msg_lenth_0x_big_order[i:i+2])         
        ascii_list.extend(msg_lenth_0x_list)

        for i in range(0,len(ascii_list)/64):

            aa,bb,cc,dd = abcd_list

            order_1 = self.__genM16(self.__m_1,ascii_list,i)
            order_2 = self.__genM16(self.__m_2,ascii_list,i)
            order_3 = self.__genM16(self.__m_3,ascii_list,i)
            order_4 = self.__genM16(self.__m_4,ascii_list,i)

            abcd_list = self.__fun(abcd_list,self.__F,order_1,self.__shi_1)
            abcd_list = self.__fun(abcd_list,self.__G,order_2,self.__shi_2)
            abcd_list = self.__fun(abcd_list,self.__H,order_3,self.__shi_3)
            abcd_list = self.__fun(abcd_list,self.__I,order_4,self.__shi_4)

            output_a = hex((int(abcd_list[0],16)+int(aa,16))&0xffffffff)[:-1]
            output_b = hex((int(abcd_list[1],16)+int(bb,16))&0xffffffff)[:-1]
            output_c = hex((int(abcd_list[2],16)+int(cc,16))&0xffffffff)[:-1]
            output_d = hex((int(abcd_list[3],16)+int(dd,16))&0xffffffff)[:-1]
            
            abcd_list = [output_a,output_b,output_c,output_d]

            self.__Ti_count = 1
        """
        长度 16 or 32 
        """
        if self.__size:
            result = self.__show_result(abcd_list)
        else:
            result = self.__show_result(abcd_list)[8:-8]
        """
        大小写
        """
        if self.__upper:
            return result.upper()   
        else:
            return result

if __name__ == '__main__':
    """
    正常md5测试
    """
    m = Md5Hash()
    result = m.get_md5("test") 
    print "md5(test) = "+result #098f6bcd4621d373cade4e832627b4f6

    """
    大小写测试
    """
    m = Md5Hash(upper=True)
    result = m.get_md5("test") 
    print "md5(test) upper = "+result #098F6BCD4621D373CADE4E832627B4F6 

    """
    16位测试
    """
    m = Md5Hash(size_32=False)
    result = m.get_md5("test") 
    print "md5(test) upper = "+result #4621D373CADE4E83

    """
    变形md5测试
    """
    m = Md5Hash(D=0x1234567)
    result = m.get_md5("test") 
    print "md5(test) D=0x1234567 = "+result #44e471e3b222c35571a61bd70ed59dd2
