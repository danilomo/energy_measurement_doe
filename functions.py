from function_utils import *

def cpu( x ):
    return x

def io( x ):
    return x

coefs = [930.1500514651766, 0.8511402216771129, 4.5416094018889225e-06, -9.047522846488997e-11]
f = inverse( polynomial_function(coefs) )
g = create_scale( 51000 )
io = compose( int, zero_intercept( compose( f, g ) ) )
    
def network( x ):
    return x
