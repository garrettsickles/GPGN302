from rsf.proj import *

# ------------------------------------------------------------
# model parameters
def paramwin():
    par = dict(
        nx=1201, ox=18.000,dx=0.025,  lx='x', ux='km', # X axis
        nz=601,  oz=4.5,   dz=0.025,  lz='z', uz='km', # Z axis
        nt=4001, ot=0,     dt=0.001,  lt='t', ut='s'   # T axis
        )
    
    par['ft2km']=0.3048    # conversion from ft to km
    par['ox']=par['ox']*par['ft2km']
    par['dx']=par['dx']*par['ft2km']
    par['oz']=par['oz']*par['ft2km']
    par['dz']=par['dz']*par['ft2km']

    par['jsnap']=150       # snapshot jump
    par['kt']=100          # wavelet delay (samples) 
    par['nb']=100          # boundary (grid points)
    par['verb']='y'

    par['nqz']=par['nz']; par['oqz']=par['oz']; par['dqz']=par['dz']
    par['nqx']=par['nx']; par['oqx']=par['ox']; par['dqx']=par['dx']
    return par

# ------------------------------------------------------------
# model parameters
def param():
    par = dict(
        nx=3201,  ox=10.000, dx=0.025,  lx='x', ux='km',
        ny=1,     oy=0.000,  dy=0.025,  ly='y', uy='km',
        nz=1201,  oz=0,      dz=0.025,  lz='z', uz='km',
        nt=1500,  ot=0,      dt=0.008,  lt='t', ut='s'
        )

    par['ft2km']=0.3048

    par['ox']=par['ox']*par['ft2km']
    par['dx']=par['dx']*par['ft2km']
    par['oy']=par['oy']*par['ft2km']
    par['dy']=par['dy']*par['ft2km']
    par['oz']=par['oz']*par['ft2km']
    par['dz']=par['dz']*par['ft2km']

    par['nb']=250

    # source coordinates
    par['os']=10.95*par['ft2km']
    par['ds']=0.150*par['ft2km']
    # source index: o=39, d=6, n=500

    # receiver coordinates
    par['or']=10.95*par['ft2km']
    par['dr']=0.075*par['ft2km']

    par['nzdtm']=244 # number of redatuming steps through water
    par['nzpad']=143

    # all shots parameters
    par['nsall']=500
    par['dsall']=0.04572
    par['osall']=3.33756

    return par

# ------------------------------------------------------------
def modpar(par):

    par['kt']=100
    par['nt']=12001
    par['dt']=0.001
    par['nb']=150
    par['jsnap']=1000
    par['jdata']=1
    par['wweight']=50
    par['wclip']=0.5

# ------------------------------------------------------------
def migpar(par):

    par['verb']='y'
    par['eps']=0.1
    par['nrmax']=5
    par['dtmax']=0.00005
    par['tmx']=16

    par['fw']=36
    par['jw']=1
    par['dw']=1/(par['nt']*par['dt'])
    par['kw']=par['nt']/2+1
    par['ow']=par['fw']*par['dw']
    par['nw']=240
    par['eic']='itype=o'

# ------------------------------------------------------------
def getstrvelwin(velo,par):
    strvelfile = 'DATA/sigsbee/sigsbee2a_stratigraphy.sgy'

    Flow(velo+'-raw',strvelfile,'segyread read=data')
    Flow(velo,
         velo+'-raw',
         '''
         scale rscale=0.001 |
         scale rscale=%g |
         put 
         o1=%g d1=%g label1=%s unit1=%s
         o2=%g d2=%g label2=%s unit2=%s |
         window n1=%d min1=%g n2=%d min2=%g
         ''' % (par['ft2km'],
                0.0                ,0.0250*par['ft2km'],par['lz'],par['uz'],
                10.000*par['ft2km'],0.0250*par['ft2km'],par['lx'],par['ux'],
                par['nz'],par['oz'],
                par['nx'],par['ox']
                ))

# ------------------------------------------------------------
def getstrvel(velo,par):

    strvelfile = 'DATA/sigsbee/sigsbee2a_stratigraphy.sgy'
    #Fetch(velo,'sigsbee')

    Flow([velo+'-raw',velo+'-t','./'+velo+'-h','./'+velo+'-b'],
         strvelfile,
         '''
         segyread
         tape=$SOURCE
         tfile=${TARGETS[1]}
         hfile=${TARGETS[2]}
         bfile=${TARGETS[3]}
         ''',stdin=0)

    Flow(velo,
         velo+'-raw',
         '''
         scale rscale=0.001 |
         scale rscale=%g |
         put
         o1=%g d1=%g label1=%s unit1=%s
         o2=%g d2=%g label2=%s unit2=%s
         ''' % (par['ft2km'],
                0.0                ,0.0250*par['ft2km'],par['lz'],par['uz'],
                10.000*par['ft2km'],0.0250*par['ft2km'],par['lx'],par['ux']
                ))



# ------------------------------------------------------------
def getdata(data,par):

    datafile = 'DATA/sigsbee/sigsbee2a_nfs.sgy'
   
    Flow([data,data+'-t','./'+data+'-h','./'+data+'-b'],
         datafile,
         '''
         segyread
         tape=$SOURCE
         tfile=${TARGETS[1]}
         hfile=${TARGETS[2]}
         bfile=${TARGETS[3]}
         ''',stdin=0)


# ------------------------------------------------------------
def makedensity(dens,d1,d2,d3,par):

    Flow(dens+'1',None,
         '''
         spike nsp=1 mag=1
         n1=%(nz)d o1=%(oz)g d1=%(dz)g k1=251 l1=255
         n2=%(nx)d o2=%(ox)g d2=%(dx)g
         '''%par)

    Flow(dens+'2',None,
         '''
         spike nsp=1 mag=1
         n1=%(nz)d o1=%(oz)g d1=%(dz)g k1=345 l1=355
         n2=%(nx)d o2=%(ox)g d2=%(dx)g k2=495 l2=505
         '''%par)

    Flow(dens+'3',None,
         '''
         spike nsp=1 mag=1
         n1=%(nz)d o1=%(oz)g d1=%(dz)g k1=451 l1=455
         n2=%(nx)d o2=%(ox)g d2=%(dx)g
        '''%par)

    Flow(dens,[dens+'1',dens+'2',dens+'3'],
         '''
         add ${SOURCES[1:3]} scale=%g,%g,%g |
         add add=1
         '''%(d1,d2,d3))

# ------------------------------------------------------------
def makeshots(shot,data,par):

    Flow(shot+'-ss',data+'-t','dd type=float | headermath output="10925+fldr*150" | window')
    Flow(shot+'-oo',data+'-t','dd type=float | headermath output="offset"         | window')

    # create sraw(t,o,s): o=full offset
    Flow(shot+'-si',shot+'-ss','math output=input/150')
    Flow(shot+'-oi',shot+'-oo','math output=input/75')
    Flow(shot+'-os',[shot+'-oi',shot+'-si'],
         'cat axis=2 space=n ${SOURCES[1]} | transp | dd type=int')
    Flow(shot+'-raw',[data,shot+'-os'],
         '''
         intbin head=${SOURCES[1]} xkey=0 ykey=1 |
         put d2=0.075 d3=0.150 o3=10.95 label1=t label2=o label3=s
         ''')
    Flow(shot,shot+'-raw',
         '''
         mutter half=false t0=1.0 v0=6 |
         put label1=t unit1=s
         o2=%g d2=%g unit2=%s
         o3=%g d3=%g unit3=%s
         ''' % ( 0.000*par['ft2km'],0.075*par['ft2km'],par['ux'],
                 10.95*par['ft2km'],0.150*par['ft2km'],par['ux']
                 ))

# ------------------------------------------------------------
def getreflectwin(ref,par):

    reflectfile = 'DATA/sigsbee/sigsbee2a_reflection_coefficients.sgy'
    #Fetch(velo,'sigsbee')

    Flow([ref+'-raw',ref+'-t','./'+ref+'-h','./'+ref+'-b'],
         reflectfile,
         '''
         segyread
         tape=$SOURCE
         tfile=${TARGETS[1]}
         hfile=${TARGETS[2]}
         bfile=${TARGETS[3]}
         ''',stdin=0)

    Flow(ref,
         ref+'-raw',
         '''
         scale rscale=0.001 |
         scale rscale=%g |
         put
         o1=%g d1=%g label1=%s unit1=%s
         o2=%g d2=%g label2=%s unit2=%s |
         window n1=%d min1=%g n2=%d min2=%g
         ''' % (par['ft2km'],
                0.0                ,0.0250*par['ft2km'],par['lz'],par['uz'],
                10.000*par['ft2km'],0.0250*par['ft2km'],par['lx'],par['ux'],
                par['nz'],par['oz'],
                par['nx'],par['ox']
                ))
