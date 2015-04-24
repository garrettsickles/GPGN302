from rsf.proj import *

# ------------------------------------------------------------
def param():
    par = dict(
        nt=1000,ot=0,     dt=0.004,  lt='t', ut='s',
        nx=250, ox=7.705, dx=0.0335, lx='x', ux='km',
        ny=1,   oy=0,     dy=0.0335, ly='y', uy='km',
        nz=350, oz=0,     dz=0.01,   lz='z', uz='km',
        nm=250, om=7.705, dm=0.0335, lm='m', um='km',  # midpoints
        nh=24,  oh=0.262, dh=0.1340, lh='h', uh='km',  # offset
	nw=200, jw=1,      ow=5,
    	verb='y',eps=0.01,nrmax=5,dtmax=0.00005,
    	tmx=16,tmy=0,pmx=16,pmy=0
        )
    return par

def cmpgrey(custom,par):
    return '''
    grey title="" pclip=100
    label1=%s unit1=%s
    label2=%s unit2=%s
    screenratio=2 screenht=10 xll=2
    %s
    '''%(par['lt'],par['ut'],par['lh'],par['uh'],par['labelattr']+par['labelrot']+' '+custom)
def cmpwigl(custom,par):
    return '''
    wiggle title="" pclip=100
    poly=y transp=y yreverse=y seemean=y wherexlabel=t
    label1=%s unit1=%s
    label2=%s unit2=%s
    screenratio=2 screenht=10 xll=2
    %s
    '''%(par['lt'],par['ut'],par['lh'],par['uh'],par['labelattr']+par['labelrot']+' '+custom)

def smbgrey(custom,par):
    return '''
    grey title="" pclip=100
    label1=%s unit1=%s
    label2=p unit2="s/km"
    screenratio=2 screenht=10 xll=2
    %s
    '''%(par['lt'],par['ut'],par['labelattr']+par['labelrot']+' '+custom)
def smbplot(custom,par):
    return '''
    graph title="" pad=n transp=y yreverse=y
    min2=0.25 max2=0.75
    plotcol=0 plotfat=12 wantaxis=n
    screenratio=2 screenht=10 xll=2
    %s
    ''' % (par['labelattr']+par['labelrot']+' '+custom)

def intplot(custom,par):
    return '''
    graph title="" pad=n transp=y yreverse=y
    plotcol=0 plotfat=12 wantaxis=y wherexlabel=t
    min2=1.25 max2=2.75
    label1=%s unit1=%s
    label2=v unit2="km/s"
    screenratio=2 screenht=10 xll=2
    %s
    ''' % (par['lt'],par['ut'],par['labelattr']+par['labelrot']+' '+custom)

def velplot(custom,par):
    return '''
    graph title="" pad=n transp=y yreverse=y
    plotcol=0 plotfat=12 wantaxis=y wherexlabel=t
    min2=1.25 max2=2.75
    label1=%s unit1=%s
    label2=v unit2="km/s"
    screenratio=2 screenht=10 xll=2
    %s
    ''' % (par['lz'],par['uz'],par['labelattr']+par['labelrot']+' '+custom)

def secgrey(custom,par):
    return '''
    grey title="" pclip=100
    label1=%s unit1=%s
    label2=%s unit2=%s
    screenratio=0.6 screenht=8.17
    %s
    ''' % (par['lt'],par['ut'],par['lm'],par['um'],par['labelattr']+par['labelrot']+' '+custom)
