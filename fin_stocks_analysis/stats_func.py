import numpy as np
import pandas as pd


try:



    def DataNorm(x):
        
        y = x.copy()
        y = ( x - x.mean() )/( x.max()-x.min() )
        return y


    def DataStand(x):
            
        y = x.copy()
        y = (x-x.mean())/(x.std())
        return y


    def DataStat(x):
        
        return pd.Series(x.to_numpy()).copy()


    def RangeOf(x):
        
        return ( x.max() - x.min() )


except Exception as exp:
    
    print(exp)
    input()
