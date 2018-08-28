from function_utils import *

def cpu( x ):
    return x

#def io( x ):
#    return x

coefs = [930.1500514651766, 0.8511402216771129, 4.5416094018889225e-06, -9.047522846488997e-11]
f = inverse( polynomial_function(coefs) )
g = create_scale( 51000 )
io = compose( int, zero_intercept( compose( f, g ) ) )
    
#def network( x ):
#    return x

network = create_scale( 940 )




cpu1 = cpu
cpu2 = cpu

network1 = network
network2 = network

coefs2 = [67.38385766106583, -0.008580231318839017, 1.2098420222488348e-06, -3.400708931638599e-11, 3.223888367370422e-16]
io1 = io
io2 = polynomial_function(coefs) 

net1 = network1
net2 = network2
