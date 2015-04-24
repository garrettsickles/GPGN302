from rsf.proj import *

def param(par):

    # ------------------------------------------------------------
    # (half) offset
    par['oh']=0.5*par['oo']
    par['dh']=0.5*par['do']
    par['uh']=par['uo']
    par['lh']='h'
    par['nh']=par['no']
    
    # ------------------------------------------------------------
    # midpoint
    par['om']=par['os']
    par['dm']=0.5*par['do']
    par['um']=par['us']
    par['lm']='m'
    par['nm']=par['ns']+par['nh']
    
    par['dsdm']=par['ds']/par['dm']
    par['nsnm']=par['ns']*par['dsdm']
    par['nob2']=par['no']*2
    
    # ------------------------------------------------------------
    # compute min and max along all axes
    par['smin']=par['os']
    par['smax']=par['os']+(par['ns']-1)*par['ds']
    
    par['omin']=par['oo']-par['dh']/2
    par['omax']=par['oo']+(par['no']-1)*par['do']+par['dh']/2
    
    par['hmin']=par['oh']-par['dh']/2
    par['hmax']=par['oh']+(par['nh']-1)*par['dh']+par['dh']/2

    par['dx']=par['dh']
    par['nx']=(par['smax']+par['omax']/2-par['ox'])/par['dx']+1
    
    par['xmin']=par['ox']-par['dx']/2
    par['xmax']=par['ox']+(par['nx']-1)*par['dx']+par['dx']/4
    
    # ------------------------------------------------------------
    # plot ratios
    par['osratio']=(par['omax']-par['omin'])/(par['xmax']-par['xmin'])
    par['hmratio']=(par['hmax']-par['hmin'])/(par['xmax']-par['xmin'])
    
    # plot heights
    par['osheight']=12*par['osratio']
    par['hmheight']=12*par['hmratio']
    # ------------------------------------------------------------


# ------------------------------------------------------------
def osall(par):
    return '''
    transp plane=23 | pad n2out=2        | transp plane=12 | put n1=%(nob2)d n2=1 d1=%(dh)d d2=1 | window |  
    pad n3out=%(dsdm)d | transp plane=23 | put n2=%(nsnm)d n3=1 d2=%(dm)g d3=%(dm)g  |
    pad n2out=%(nx)d |
    grey title="" color=j allpos=y
    screenratio=%(osratio)g screenht=%(osheight)g
    label1=%(lo)s unit1=%(uo)s min1=%(omin)g max1=%(omax)g 
    label2=%(ls)s unit2=%(us)s min2=%(xmin)g max2=%(xmax)g
    %(labelattr)s %(labelrot)s
    '''%par

def hmall(par):
    return '''
    pad n2out=%(nx)d |
    grey title="" color=j allpos=y
    screenratio=%(hmratio)g screenht=%(hmheight)g
    label1=%(lh)s unit1=%(uh)s
    label2=%(lm)s unit2=%(um)s min2=%(xmin)g max2=%(xmax)g
    %(labelattr)s %(labelrot)s
    '''%par

def mco(mid,sou,off,par):
    Flow(mid,[off,sou],
         'math s=${SOURCES[1]} output="s+0.5*input"')

def hco(hof,off,par):
    Flow(hof,[off],
         'math output="0.5*input"')
