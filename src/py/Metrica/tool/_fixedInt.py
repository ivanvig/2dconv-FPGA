##########################################################################
#  This file is part of the deModel library, a Python package for using
#  Python to model fixed point arithmetic algorithms.
#
#  Copyright (C) 2007 Dillon Engineering, Inc.
#  http://www.dilloneng.com
#
#  The deModel library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation; either version 2.1 of the
#  License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library. 
#  If not, see <http://www.gnu.org/licenses/>
##########################################################################

'''DeFixedInt class
'''

__author__ = "$Author: guenter $"
__revision__ = "$Revision: 431 $"
__date__ = "$Date: 2007-09-19 19:16:58 +0200 (Wed, 19 Sep 2007) $"


import math
import copy

import numpy

def arrayFixedInt(intWidth, fractWidth, N, signedMode='S', roundMode='round', saturateMode='saturate'):
  '''Create a Numpy array of length N with DeFixedInt instances of
  representation S(intWidth, fractWidth).
  If value is specified the instances are set with the specified value.

  @type   intWidth    : integer
  @param  intWidth    : used bit width for interger part

  @type   fractWidth  : integer
  @param  fractWidth  : used bit width for fractional part

  @type   N           : integer, list, or array
  @param  N           : if N is an integer the value specifies the length of the
                        array to be created. If N is a list or array, an
                        array of same length is created with the values
                        used to initialize the returned array.

  @rtype              : numpy array
  @return             : numpy array with N instances of DeFixedInt()
  '''

  

  if(isinstance(N, (list, numpy.ndarray))):
      retA=numpy.array([DeFixedInt(intWidth, fractWidth, signedMode, roundMode, saturateMode) for _ in N])
      for index in range(len(N)):
          retA[index].value=N[index]

  else:
    raise TypeError, "type(N) = '%s' not supported" %type(N)

  return retA



class DeFixedIntOverflowError(OverflowError):
  "Used to indicate that a set value exceeds the specified width of DeFixedInt."


class DeFixedInt(object):
  ''' 
  Fixed point fractional arithmetic data type
  ===========================================

  Introduction
  ------------

  The class is an abstract data type that can be used to perform fixed-
  point arithmetic. The data type keeps track of the decimal point and 
  arithmetic operations affect the position of the decimal point based
  on the fundamental rules of fixed-point arithmetic.

  The data type is for signed numbers. It can be initiated with an
  integer number, then the value is just assigned to the data type. It
  also can be initiated with a floating point number, which is scaled
  based on the fractional width.

  The data type always needs to be initiated with an integer width and
  a fractional width. The integer width specifies how many bits are used
  to represent the integer part of the value. The fractional width
  specifies how many bits represent the fractional part of the value. As
  the value is always considered a signed number, the overall width is
  M{width = integer width + fractional width + 1}.

  There are different nomenclatures used to specify fixed point
  fractional data types. One commonly used one is the s-number
  representation. For example s0.9 specifies a signed fixed point number
  with 0 bits being used to represent the integer width and 9 bits are
  used to represent the fractional width of the number. In this
  documentation we use a second type of representation which is
  S(0,9). The capital 'A' specifies the number to be a signed number,
  with the first number in the parenthesis being the integer bit width and
  the second number after the comma being the fractional bit width. Note
  that due to the fact that both representations show a signed number,
  the overall width of this number is 10 bit.


  Fundamental fixed point arithmetic operations
  ---------------------------------------------

  The class follows the fundamental fixed point arithmetic rules as
  described in the document "Fixed Point Arithmetic: An Introduction" by
  Randy Yates. Availble from this page: 
  
  http://www.digitalsignallabs.com/fp.pdf


  Basic usage 
  -----------

  This section describes the basic usage of the class. For further
  details refer to the respective documentation of member functions.

  >>> from deModel import DeFixedInt
  
  >>> a = DeFixedInt(8,2, 2.5)
  >>> print a
  <10 (2.500) S(8,2)>
  
  >>> b = DeFixedInt(8,2, 3.75)
  >>> print b
  <15 (3.750) S(8,2)>

  >>> c = a + b

  >>> print c
  <25 (6.250) S(9,2)>

  >>> d = a * b
  >>> print d
  <150 (9.375) S(17,4)>

  Here some examples in connection with numpy

  >>> from deModel import arrayFixedInt
  >>> a = arrayFixedInt(8,2, [4.5, 1.25, 3.75, 2.0])
  >>> print a
  [<18 (4.500) S(8,2)> <5 (1.250) S(8,2)> <15 (3.750) S(8,2)>
  <8 (2.000) S(8,2)>]

  >>> b = arrayFixedInt(8,2, [2.25, 3.0, 1.5, 3.75])
  >>> print b
  [<9 (2.250) S(8,2)> <12 (3.000) S(8,2)> <6 (1.500) S(8,2)>
  <15 (3.750) S(8,2)>]
  >>> c = a + b
  >>> print c
  [<27 (6.750) S(9,2)> <17 (4.250) S(9,2)> <21 (5.250) S(9,2)>
  <23 (5.750) S(9,2)>]
  
  Internals
  ---------

  The class specifies only a few private variables and to save memory
  they are fixed via the __slots__ member variable. There are two
  notable effects of this. One is that only assignments to member
  variables are allowed that are listed in the __slots__ variable.
  Another is that by default no weak reference is supported for an
  instance of this class. For further details on this refer to: 
  http://docs.python.org/ref/slots.html#l2h-218

  The stored data are all set as private data and if necessary can be
  accessed via properties. For example the actual value is stored in the
  variable self.__value and can be accessed via the value property. This
  allows for the set property for example to test the data type and in
  case of a float value to convert the float to integer, depending on
  the specified integer and fractional width.

  Integer and fractional width are values that can be specified when
  instantiating the class and their values are later read only. This is
  due to the fact that they are changed indirect by operations applied
  to the actual value of the class.

  The class supports the read only property width, which returns the
  used bit width. The bit width  is integer width + fractional width + 1. 
  

  '''

  __slots__ = ('__intWidth', '__fractWidth','__signedMode', '__roundMode','__saturateMode', '__value')

  def __init__(self, intWidth=0, fractWidth=15, signedMode='S', roundMode='trunc', saturateMode='saturate'):

    '''    
    @type   intWidth    : unsigned integer number
    @param  intWidth    : Number of bits used to store the integer part of the 
                          value. As the class stores signed numbers the resulting 
                          bit width is intWidth + fractWidth + 1

    @type   fractWidth  : unsigned integer number
    @param  fractWidth  : Number of bits that are used to store the fractional
                          part of the value. The fractional width determines
                          the scaling that is applied to floating point values.
                          The maximum value allowed is 1 bit smaller than width,
                          as DeFixedInt is storing signed numbers.
    
    @type   value       : integer or floating point number
    @param  value       : Assigns the initial value to the data type. If the value
                          is of integer type the value is just assigned as is. If 
                          the value is of float type the value is scaled up,
                          depending on the fractWidth value.

    @type   roundMode   : string
    @param  roundMode   : Specifies the way rounding is done for operations 
                          with this data type. The setting affects the rounding
                          done when converting a floating point value to fixed 
                          point representation
                          Possible settings:
                          'trunc'       - truncate the result
                          'round_even'  - round the result to the nearest even value
                          'round'       - round the result
                          
    '''
   
    # Test for proper parameter
    # Setting the value will be tested through the property function
    if(intWidth < 0):
        if(abs(intWidth)>=fractWidth):
            raise ValueError, "Integer width needs to be >= -fractWidth!"
    if(fractWidth < 0):
      raise ValueError, "Fractional width needs to be >= 0!"

    if( (roundMode != 'trunc') and
        (roundMode != 'round_even') and
        (roundMode != 'round')):
      raise ValueError, "Round mode '%s' not supported!" % roundMode

    if( (saturateMode != 'saturate') and 
        (saturateMode != 'wrap')):
      raise ValueError, "Saturate mode '%s' not supported!" % saturateMode
        
    if( (signedMode != 'S') and 
        (signedMode != 'U')):
      raise ValueError, "Signed mode '%s' not supported!" %signedMode
         

    self.__intWidth = intWidth - fractWidth-1  # Remove Sign Bit
    self.__fractWidth = fractWidth
    self.__roundMode = roundMode
    self.__saturateMode = saturateMode
    self.__signedMode= signedMode
    self._setValue(0)

    
    
    
   
  ###################################################################### 
  # properties
  ###################################################################### 

  

  def _getValue(self):
    '''
    Return the value
    '''
    return self.__value
  def _setValue(self, value):
    '''
    Allow to set the value
    @type     value : integer, long, or float
    @param    value : Set the value. An integer or long will be set as is. A
                      float value will be scaled based on the fractional
                      width
    '''
    if((self.signedMode == 'U') and (value<0)):
        raise ValueError, "While in Unsigned Mode, value must be greater than 0"
    
    if(isinstance(value, float)):
      #print "float value"
      self._fromFloat(value)

    elif(isinstance(value, (int, long, numpy.integer, numpy.float))): # 15/09/2017 Ivan: Agregado numpy.integer para aceptar enteros de un arreglo de numpy.
      #print "int value"
     self.__value = value
    else:
      print "unkown type: ", type(value)

    self._overflowCheck()
  value = property(_getValue, _setValue)

  def _getFloatValue(self):
    return self._toFloat()
  fValue = property(_getFloatValue)

  
  def _getIntWidth(self):
    return self.__intWidth+1 
  intWidth = property(_getIntWidth)

  def _getFractWidth(self):
    return self.__fractWidth
  fractWidth = property(_getFractWidth)

  def _getWidth(self):
    '''width property'''
    return  self.__intWidth + self.__fractWidth + 1 
  width = property(_getWidth)
  
  def _getSignedMode(self):
    return self.__signedMode
  signedMode = property(_getSignedMode) 

  def _getRep(self):
    '''Return the representation of the fixed point number as string'''
    if (self.signedMode=='S'):
        return "S(%d,%d)" % (self.intWidth+ self.fractWidth, self.fractWidth) ## Add fractional and sign
    elif (self.signedMode=='U'):
        return "U(%d,%d)" % (self.intWidth+ self.fractWidth, self.fractWidth)
  rep = property(_getRep)

#### NO TOCAR EL INTVALUE SOLO USAR PARA LOGUEO (Genaro)####
### MODIFICADO: SE TUVO EN CUENTA QUE INTWIDTH ES LA PARTE ENTERA + EL SIGNO----> SE SACO UN +1 QUE DEMAS###
  def _getIntValue(self):
    '''Return Int value without sign'''
    return int(int((self._toFloat()*2**self.fractWidth)+2**(self.intWidth+self.fractWidth))&(2**(self.intWidth+self.fractWidth)-1))
  intvalue = property(_getIntValue)

  ###################################################################### 
  # overloaded functions
  ###################################################################### 

#  def __copy__(self):
#    retValue = DeFixedInt(self.intWidth, self.fractWidth, self.value)
#    return retValue

#  def __getitem__(self, key):
#    '''Allow to access a bit or slice of bits
#
#    For bit access the respective bit is returned as integer type. For
#    slicing a DeFixedInt instance is returned with the value set to the
#    sliced bits and intWidth/fractWidth being adjusted based on the
#    slice.
#
#    When the slice includes the sign bit it is taken over to the return
#    value. If the sign bit is excluded the bits are taken as is with the
#    sign bit set to 0.
#
#    For example using the 4-bit number -6 = b1010, slicing bits 3:1 -->
#    b101 includes the sign bit, the result is -3.
#
#    Now using the 4-bit number -3 = b1101, slicing bits 2:1 --> b10,
#    however, the slice excludes the sign bit, hence the result is 2.
#
#    The same is true for a positive 4-bit number like 5 = b0101. Slicing
#    bits 2:1 --> b10. As the sign bit is not included in the slice the
#    result is again 2. Notice that even though the msb of the slice is 1
#    the result is not negative.
#
#    @type   key : Integer or slice
#    @param  key : Index value 0 ... len-1 will return bits lsb ... msb. 
#                  Negative numbers -1 ... -len will return the bits 
#                  msb ... lsb.
#
#                  For a slice the bits are specified in the order 
#                  [msb:lsb]. With msb > lsb. The msb bit is not included
#                  in the slice. For example, the slice [4:] will return
#                  4 bits, namely bits 3, 2, 1, and 0. The slice [4:2]
#                  will return 4-2=2 bits, namely bits 3 and 2.
#
#    @rtype  : Integer or DeFixedInt for slice
#    @return : Bit or slice specified by key
#    '''
#    if(isinstance(key, int)):
#      i = key
#      if(i >= self.width or i < (-self.width)):
#        raise IndexError, "list index %d out of range %d ... %d" % \
#                          (i, -self.width, (self.width-1))
#
#      if(i < 0):
#        shift = self.width + i
#      else:
#        shift = i
#    
#      return ((self.value >> shift) & 0x1)
#
#    elif(isinstance(key, slice)):
#      msb, lsb = key.start, key.stop
#
#      # first determine the new value
#      if(lsb == None):
#        lsb = 0
#      if(lsb < 0):
#        raise ValueError, "DeFixedInt[msb:lsb] requires lsb >= 0\n" \
#              "            lsb == %d" % lsb
#      if(msb == None or msb == self.width):
#        if(msb == None):
#          msb = self.width
#        newValue = (self.value >> lsb)
#      else:
#        newValue = None
#
#      if(msb <= lsb):
#        raise ValueError, "DeFixedInt[msb:lsb] requires msb > lsb\n" \
#              "            [msb:lsb] == [%d:%d]" % (msb, lsb)
#
#      if(msb > self.width):
#        raise ValueError, "DeFixedInt[msb:lsb] requires msb <= %d\n" \
#              "            msb == %d" % (self.width, msb)
#
#      if(not newValue):
#        newValue = (self.value & (1 << msb)-1) >> lsb
#
#
#      # then the new intWidth and fractWidth
#      if(lsb < self.fractWidth):
#        if(msb > self.fractWidth):
#          newFractWidth = self.fractWidth - lsb
#
#          if(msb > self.intWidth + self.fractWidth):
#            newIntWidth = self.intWidth
#          else:
#            newIntWidth = msb - self.fractWidth
#        
#        else:
#          newIntWidth = 0
#          newFractWidth = msb - lsb
#
#      else:
#        newFractWidth = 0
#
#        if(msb > (self.intWidth + self.fractWidth)):
#          newIntWidth = msb - lsb - 1
#        else:
#          newIntWidth = msb - lsb
#
#      # create new instance and return it
#      retValue = DeFixedInt(newIntWidth, newFractWidth, newValue)
#
#      return retValue
#
#    else:
#      raise TypeError, "DeFixedInt item/slice index must be integer"

    

  def __repr__(self):
    '''
    Se llama automaticamente cuando print objeto
    '''
    if (self.signedMode == 'S'):
        str = "<%d" % (self.__value)
        str += " (%.3f)" % (self.fValue)
        str += " S(%d,%d)>" % (self.__intWidth+self.__fractWidth+1, self.__fractWidth)
        return str
    elif (self.signedMode == 'U'):
        str = "<%d" % (self.__value)
        str += " (%.3f)" % (self.fValue)
        str += " U(%d,%d)>" % (self.__intWidth+self.__fractWidth+1, self.__fractWidth)
        return str

  def __str__(self):

    if (self.signedMode == 'S'):
        str = "<%d" % (self.__value)
        str += " (%.3f)" % (self.fValue)
        str += " S(%d,%d)>" % (self.__intWidth+self.__fractWidth+1, self.__fractWidth)
        return str
    elif (self.signedMode == 'U'):
        str = "<%d" % (self.__value)
        str += " (%.3f)" % (self.fValue)
        str += " U(%d,%d)>" % (self.__intWidth+self.__fractWidth+1, self.__fractWidth)
        return str
        
        
  def __hex__(self):
    '''Return the hex representation of the value.

    The number is represented with the minimum number of nibbles as 
    needed based on the width.
    Negative numbers are represented as two's complement.
    '''
    width = self.width
    mask = long(2L** width) -1
    fStr = '0x%%.%dX'%(int(math.ceil(width / 4)))
    return fStr % (self.value & mask)


  def __eq__(self, other):
      '''
      Funcion a==b
      '''
      return self.fValue==other.fValue
      
  def __lt__(self, other):
      '''
      Funcion a<b
      '''
      return self.fValue < other.fValue
      
  def __le__(self, other):
      '''
      Funcion a<=b
      '''
      return self.fValue <= other.fValue
      
  def __ne__(self, other):
      '''
      Funcion a!=b
      '''
      return self.fValue!=other.fValue
      
  def __gt__(self, other):
      '''
      Funcion a>b
      '''
      return self.fValue > other.fValue
      
  def __ge__(self, other):
      '''
      Funcion a>=b
      '''
      return self.fValue >= other.fValue
      
  ####REVISAR PARA NUMERO CHICOS Y HACER PARA UNSIGNED AND, OR Y XOR
  def __and__(self, other):
      '''
      Funcion a&b
      '''
      newIntWidth=max(self.intWidth, other.intWidth)
      newfractWidth=max(self.fractWidth, other.fractWidth)
  
      newWidth= newIntWidth + newfractWidth
   
      resp = DeFixedInt(newWidth, newfractWidth, signedMode=self.signedMode)
      
      aux=self.intvalue & other.intvalue
      
      if ((self.signedMode=='U')and(other.signedMode=='U')):
          resp.value=aux*2**(-self.fractWidth)
         
      if ((self.signedMode=='S')and(other.signedMode=='S')):
         
          if(aux>=2**(self.intWidth-1)):
              result=(aux-2**(self.width))/2**(self.fractWidth)
              print result
          else:
              result=aux*2**(-self.fractWidth)
              
          resp.value=result
      
      return resp
      
  def __xor__(self, other):
      '''
      Funcion a^b
      '''
      newIntWidth=max(self.intWidth, other.intWidth)
      newfractWidth=max(self.fractWidth, other.fractWidth)
  
      newWidth= newIntWidth + newfractWidth
   
      resp = DeFixedInt(newWidth, newfractWidth, signedMode=self.signedMode)
      
      aux=self.intvalue ^ other.intvalue
      
      if ((self.signedMode=='U')and(other.signedMode=='U')):
          resp.value=aux*2**(-self.fractWidth)
         
      if ((self.signedMode=='S')and(other.signedMode=='S')):
         
          if(aux>=2**(self.intWidth-1)):
              result=(aux-2**(self.width))/2**(self.fractWidth)
              print result
          else:
              result=aux*2**(-self.fractWidth)
              
          resp.value=result
      
      return resp
      
  def __or__(self, other):
      '''
      Funcion a|b
      '''
      newIntWidth=max(self.intWidth, other.intWidth)
      newfractWidth=max(self.fractWidth, other.fractWidth)
  
      newWidth= newIntWidth + newfractWidth
   
      resp = DeFixedInt(newWidth, newfractWidth, signedMode=self.signedMode)
      
      aux=self.intvalue | other.intvalue
      
      if ((self.signedMode=='U')and(other.signedMode=='U')):
          resp.value=aux*2**(-self.fractWidth)
         
      if ((self.signedMode=='S')and(other.signedMode=='S')):
         
          if(aux>=2**(self.intWidth-1)):
              result=(aux-2**(self.width))/2**(self.fractWidth)
              print result
          else:
              result=aux*2**(-self.fractWidth)
              
          resp.value=result
      
      return resp
      
      


  def __mul__(self, other):
    '''Fixed Point multiplication

    Fixed point representation is calculated based on:

    S(a1, b1) * S(a2, b2) = S(a1+a2+1, b1+b2)

    @type other   : - DeFixedInt
                    - int;        will be first converted to DeFixedInt based on 
                                  operand A intWidth/fractWidth
                    - float;      will be scaled and converted to DeFixedInt based
                                  on intWidth/fractWidth of operand A
                    
    @param other  : Operand B
    
    @rtype  : DeFixedInt
    @return : A * B
    '''
    newIntWidth=self.intWidth + other.intWidth
    newfractWidth=self.fractWidth + other.fractWidth
  
    newWidth= newIntWidth + newfractWidth
   
    retValue = DeFixedInt(newWidth, newfractWidth, signedMode=self.signedMode)
#    retValue = DeFixedInt()
#
#    if(isinstance(other, DeFixedInt)):
#      
#      #print "__mult__: other is DeFixedInt"
#      retValue.__intWidth = self.__intWidth + other.__intWidth + 1
#      retValue.__fractWidth = self.__fractWidth + other.__fractWidth
#      retValue.__roundMode = self.__roundMode
#      retValue.__saturateMode = self.__saturateMode
#
#      retValue.value = self.value * other.value
#
#    elif(isinstance(other, (int, long, float))):
#      
#      #print "__mult__: other is '%s' "% type(other)
#      b = DeFixedInt(self.__intWidth, self.__fractWidth, other, self.__roundMode, self.__saturateMode)
#      retValue = self * b
#    
#    else:
#      msg = "'%s' not supported as operator for DeFixedInt multiplication"%type(other)
#      raise TypeError, msg
    retValue.value = self.fValue * other.fValue

    return retValue


  #def __div__(self, other):
  #  '''Fixed point division

  #  Fixed pont representation is calculated based on:

  #  S(a1, b1) / S(a2, b2) = S(a1+b2+1, a2+b1)

  #  @type other   : - DeFixedInt
  #                  - int;        will be first converted to DeFixedInt based on 
  #                                operand A intWidth/fractWidth
  #                  - float;      will be scaled and converted to DeFixedInt based
  #                                on intWidth/fractWidth of operand A
                    
  #  @param other  : Operand B

  #  @rtype  : DeFixedInt
  #  @return : A / B
  #  '''
  #  retValue = DeFixedInt()

  #  if(isinstance(other, DeFixedInt)):

  #    retValue.__intWidth = self.__intWidth + other.fractWidth + 1
  #    retValue.__fractWidth = self.__fractWidth + other.__intWidth
  #    retValue.__roundMode = self.__roundMode

  #    retValue.value = self.value / other.value
    
  #  else:
  #    msg = "'%s' not supported as operator for DeFixedInt division"%type(other)
  #    raise TypeError, msg

  #  return retValue




  def __add__(self, other):
    '''Scale operand b to the representation of operand a and add them
    S(a, b) + S(a, b) = S(a+1, b)

    @type   other : DeFixedInt
    @param  other : Operand B

    @rtype  : DeFixedInt
    @return : A + B

    '''
    newIntWidth=max(self.intWidth,other.intWidth)+1
    newfractWidth=max(self.fractWidth,other.fractWidth)
  
    newWidth= newIntWidth + newfractWidth
   
    retValue = DeFixedInt(newWidth, newfractWidth, signedMode=self.signedMode)
    #print
    #print "before change: self: %s \n--> other: %s" %(self, other)
#    temp = copy.copy(other)
#    temp.newRep(newWidth, newfractWidth)
#    temp2=copy.copy(self)
#    temp2.newRep(newWidth, newfractWidth)

    #print "after change: self: %s \n--> other: %s"% (self, other)
    #print "after change: self: %s \n--> temp: %s"% (self, temp)
    retValue.value = self.fValue + other.fValue

    return retValue

  def assign(self,aux):
     self.value=aux.fValue

  def __sub__(self, other):
    '''Scale operand b to the representation of operand a and subtract them.
    S(a, b) - S(a, b) = S(a+1, b)

    @type   other : DeFixedInt
    @param  other : Operand B

    @rtype    : DeFixedInt
    @return   : A - B
    '''
    newIntWidth=max(self.intWidth,other.intWidth)+1
    newfractWidth=max(self.fractWidth,other.fractWidth)
  
    newWidth= newIntWidth + newfractWidth
    
    retValue = DeFixedInt(newWidth, newfractWidth, signedMode=self.signedMode)
    #print
    #print "before change: self: %s \n--> other: %s" %(self, other)
#    temp = copy.copy(other)
#    temp.newRep(newWidth-1, newfractWidth)
#    temp2=copy.copy(self)
#    temp2.newRep(newWidth-1, newfractWidth)
    
    #print "after change: self: %s \n--> other: %s"% (self, other)
    #print "after change: self: %s \n--> temp: %s"% (self, temp)
    retValue.value = self.fValue - other.fValue

    return retValue
    
    
#
#  def __lshift__(self, other):
#    '''Left shift operation
#    Shift left the value by the specified amount of bits, without 
#    changing intWidth/fractWidth
#
#    @type   other : Integer or long
#    @param  other : Number of bits to shift
#    '''
#    
#    # check for the other value, only support 'int' type
#    if(not isinstance(other, (int, long))):
#      msg = "unsupported operand type(s) for <<: 'DeFixedInt' and '%s'"% type(other)
#      raise TypeError, msg
#    
#    if(other < 0):
#      raise ValueError, "negative shift count"
#
#    retValue = DeFixedInt()
#
#    width = self.width
#
#    retValue.__intWidth = self.intWidth
#    retValue.__fractWidth = self.fractWidth
#    retValue.__roundMode = self.__roundMode
#    retValue.__saturateMode = self.__saturateMode
#
#    retValue.value = self.value << other
#    
#    return retValue
#    
#  
#  def __rshift__(self, other):
#    '''Right shift operation
#    Shift the value by the specified amount of bits, without changing
#    intWidth/fractWidth.
#
#    The result will be adjusted based on the selected rounding mode.
#
#    @type   other : integer or long
#    @param  other : Number of bits to shift the value right
#    '''
#    if(not isinstance(other, (int, long))):
#      msg = "unsupported operand type(s) for <<: 'DeFixedInt' and '%s'"% type(other)
#      raise TypeError, msg
#     
#    if(other < 0):
#      raise ValueError, "negative shift count"
#        
#    retValue = DeFixedInt()
#
#    width = self.width
#
#    retValue.__intWidth = self.intWidth 
#    retValue.__fractWidth = self.fractWidth
#    retValue.__roundMode = self.__roundMode
#    retValue.__saturateMode = self.__saturateMode
#
#    if(other > 0):
#      if(self.__roundMode == 'round'):
#        roundBit = self[other-1] # take the msb that would get lost
#        retValue.value = (self.value >> other) + roundBit # and add it
#        
#      elif(self.__roundMode == 'round_even'):
#        newBitZero = self[other]
#        msbTrunc = self[other-1]
#        remainTrunc = self[other-1:0]
#
#        # TODO: should the 'not' work just for DeFixedInt?
#        if(msbTrunc and not remainTrunc.value):  # truncing 100..-> round even
#          retValue.value =  (self.value >> other) + \
#                            (newBitZero & msbTrunc)
#
#        else: # not .500.. case, round normal
#          retValue.value =  (self.value >> other) + msbTrunc
#        
#      else:   # __roundMode == 'trunc'
#        retValue.value = self.value >> other
#
#    else:
#      retValue = self
#
#    return retValue


  ###################################################################### 
  # private methods
  ###################################################################### 

  def _fromFloat(self, value):
    '''Convert float value to fixed point'''
    aux = value * 2.0**self.__fractWidth 
    self.__value = self.round(aux)

  def _toFloat(self):
    '''Convert fixed point value to floating point number'''
    return (self.__value  / (2.0 ** self.__fractWidth))

  def _overflowCheck(self):
    '''Verify that the set value does not exceed the specified width'''
    
    if (self.signedMode == 'S'):
        maxNum = 2 ** (self.width - 1) - 1
        minNum = - 2 ** (self.width - 1)
        if self.__saturateMode == 'saturate':
          if self.value > maxNum:
            self.value = maxNum
          elif self.value < minNum:
            self.value = minNum   
    ######################SE AGREGO EL WRAP####################        
        elif self.__saturateMode == 'wrap': 
          if self.value > maxNum:
            self.value = self.value - maxNum + minNum -1
          elif self.value < minNum:
            self.value = self.value - minNum + maxNum + 1   
        else:
          if(self.value > maxNum or self.value < minNum):
            msg = "Value: %d exeeds allowed range %d ... %d" % \
                  (self.value, minNum, maxNum)
            raise DeFixedIntOverflowError, msg
            
    elif (self.signedMode == 'U'):
        maxNum = 2**(self.width)-1
        minNum = 0
        if self.__saturateMode == 'saturate':
            if self.value>maxNum:
                self.value=maxNum
        elif self.__saturateMode == 'wrap':
            if self.value>maxNum:
                self.value=self.value-maxNum-1+minNum
        else:
            if(self.value > maxNum or self.value < minNum):
                msg = "Value: %d exeeds allowed range %d ... %d" % \
                      (self.value, minNum, maxNum)
                raise DeFixedIntOverflowError, msg
        

  ###################################################################### 
  # public methods (interface)
  ###################################################################### 
#
#  def isOverflowing(self, intWidth, fractWidth):
#    '''Return True if the stored value exceeds the specified width
#    
#      This function allows to test whether a value would fit in an 
#      instance with different width.
#
#      @type   intWidth    : integer
#      @param  intWidth    : integer width
#      @type   fractWidth  : integer
#      @param  fractWidth  : fractional width
#
#      @rtype              : Boolean
#      @return             : True if self.__value is overflowing S(intWidth, fractWidth)
#                            False if self.__value is not overflowing the specified parameters.
#    '''
#    maxNum = 2 ** (intWidth + fractWidth) - 1
#    minNum = - 2 ** (intWidth + fractWidth)
#
#    retValue = False
#  
#    if(self.value > maxNum or self.value < minNum):
#      retValue = True
#
#    return retValue

#
#  def newRep(self, newWidth, fractWidth):
#    '''Change the fixed point representation to the specified representation.
#
#    The operation changes the intWidth and fractWidth based on the given
#    parameter. The value of the instance is changed by this operation,
#    however the representing floating point number stays the same,
#    except for rounding issues when reducing the fractional width.
#
#    If the number does not fit the new representation a DeFixedIntOverflowError
#    exception is called.
#
#    @type   intWidth    : integer
#    @param  intWidth    : new integer width
#    @type   fractWidth  : integer
#    @param  fractWidth  : new fractional representation
#    '''
#    intWidth= newWidth- fractWidth-1
# 
#    # first adjust the fractional width
#    if(fractWidth > self.fractWidth):
#      n = fractWidth - self.fractWidth
#      # need to grow first to avoid overflow
#      self.__fractWidth = fractWidth
#      self.value = self.value << n
#    elif(fractWidth < self.fractWidth):
#      # here we might loose precision
#      n = self.fractWidth - fractWidth
#      self.value = self.value >> n
#      self.__fractWidth = fractWidth
#      
#    # next adjust the integer width
#    if(intWidth > self.intWidth):
#      self.__intWidth = intWidth
#    elif(intWidth < self.intWidth):
#      
#      # in case of a smaller intWidth we need to check for possible overflow
#      if(self.isOverflowing(intWidth, self.fractWidth)):
#
#        ##Agrego saturacion al cambio de representacion
#        maxNum = 2 ** (intWidth + fractWidth) - 1
#        minNum = - 2 ** (intWidth + fractWidth)
#        if self.value > maxNum:
#          self.value = maxNum
#        elif self.value < minNum:
#          self.value = minNum 
#        ###################################################
#
#        #msg = "New intWidth: %d will overflow current value: %d" %\
#        #      (intWidth, self.value)
#        #raise DeFixedIntOverflowError, msg
#          
#      self.__intWidth = intWidth
#      


  def round(self, value):
    '''Return the floating point value as int, rounded depending on the 
    roundMode setting.

    @type   value : float
    @param  value : Value to be rounded based on the set self.__roundMode

    @rtype        : float
    @return       : Based on the set self.__roundMode rounded number
    '''
    if(self.__roundMode == 'trunc'):
        if(value<0):
            retVal = math.floor(value)
        else:
            retVal = int(value) 

    elif(self.__roundMode == 'round_even'):
      # if value is .50 round to even, if not, round normal
      fract, integer = math.modf(value)
      absIValue = int(abs(integer))
      if(int(integer) < 0):
        sign = -1
      else:
        sign = 1

      # TODO: look for a better way to compare here for 0.500
      # floating point compare does not seem to be so good
      if((abs(fract) - 0.5) == 0.0):
        if((absIValue%2) == 0):  # even
          retVal = absIValue * sign
        else:                 # odd
          retVal = (absIValue + 1) * sign
      else:
        retVal = round(value)

    elif(self.__roundMode == 'round'):
        if(value<0):
            fract, integer = math.modf(value)
            if((abs(fract) - 0.5) == 0.0):
              retVal = math.ceil(value)
            else:
              retVal = round(value)
            #retVal = math.ceil(value)
        else:
            retVal = round(value)
    else:
      raise "ERROR: DeFixedInt.round(): '%s' not supported round mode!" % \
          self.__roundMode

    return int(retVal)


  
  def showRange(self):
    '''
    Print out the possible value range of the number.
    '''
    if (self.signedMode=='S'):
        min = -2**(self.intWidth-1)
        max = 2**(self.intWidth-1) - 1.0 / 2.0**self.fractWidth
        print "S(%d, %d): " %(self.intWidth+self.fractWidth, self.fractWidth),
        print "%10.10f ... %10.10f" % (min, max)
    elif(self.signedMode=='U'):
        min = 0
        max = 2**(self.intWidth)-2**(-self.fractWidth)
        print "U(%d, %d): " %(self.intWidth+self.fractWidth, self.fractWidth),
        print "%10.10f ... %10.10f" % (min, max)
   
  def showValueRange(self):
    '''Print out the integer # and its floating point representation'''
    if (self.signedMode=='S'):
        fract = 2**self.fractWidth
        min = -2**(self.intWidth-1)
        for i in range(2**self.width):
          value=min+ i/ 2.0**self.fractWidth
          intval=int(int((value*2**self.fractWidth)+2**(self.intWidth+self.fractWidth))&(2**(self.intWidth+self.fractWidth)-1))
          print "i: %f --> %d" %(value, (intval))
    elif(self.signedMode=='U'):
        fract = 2**self.fractWidth
        min = 0
        for i in range(2**self.width):
          value=min + i/ 2.0**self.fractWidth
          intval=int(int((value*2**self.fractWidth)+2**(self.intWidth+self.fractWidth))&(2**(self.intWidth+self.fractWidth)-1))
          print "i: %f --> %d" %(value, (intval))


  def bit(self):
    '''Return number as bit string'''
    pass



###################################################################### 
# 
# main()
# 
#if __name__ == '__main__':
#
#  a = DeFixedInt()
#  a.value = 1
#
#  print "Showing range:"
#  a.showRange()
#  print "printing a: ", a
#
#  a = DeFixedInt(8, 0, 1)
#  print "Showing range:"
#  a.showRange()
#  print "printing a: ", a
#
#  a = DeFixedInt(8, 3, 1.2)
#  print "Showing range: "
#  a.showRange()
#  print "printig a: ", a
#  
#  a = DeFixedInt(8, 2)
#  print "Representation a: ", a.rep
#  
#  b = DeFixedInt(8, 0)
#  print "Representation b: ", b.rep
#
#  c = a + b
#  print "Representation c: ", c.rep
#
#  a = 1.25
#  b = 2.0
#  c = a + b
#  print c








