from rsf.proj import *

# ------------------------------------------------------------
def param():
    par = dict(
        nt=1500,ot=0,     dt=0.004, lt='t', ut='s',   # t
        nz=400, oz=0,     dz=0.010, lz='z', uz='km',  # z
        nx=1072,ox=0,     dx=0.025, lx='x', ux='km',  # x
        ns=1012,os=0,     ds=0.025, ls='s', us='km',  # shots
        no=120, oo=0.262, do=0.025, lo='o', uo='km'   # offset
        )

    # (half) offset
    par['oh']=0.5*par['oo']
    par['dh']=0.5*par['do']
    par['uh']=par['uo']
    par['lh']='h'
    par['nh']=par['no']

    # midpoint
    par['om']=par['os']
    par['dm']=0.5*par['do']
    par['um']=par['us']
    par['lm']='m'
    par['nm']=par['ns']+par['nh']

    par['xwin']=par['oo']+(par['no']-1)*par['do']
    
    return par

# ------------------------------------------------------------
def cmpgrey(custom,par):
    return '''
    grey title="" pclip=100 min2=0 
    %s
    '''%(par['labelattr']+par['labelrot']+' '+custom)
def cmpwigl(custom,par):
    return '''
    wiggle title="" pclip=100
    poly=y transp=y yreverse=y seemean=n wherexlabel=t
    %s
    '''%(par['labelattr']+par['labelrot']+' '+custom)

def smbgrey(custom,par):
    return '''
    grey title="" pclip=100
    label2=p unit2="s/km"
    %s
    '''%(par['labelattr']+par['labelrot']+' '+custom)
def smbplot(custom,par):
    return '''
    graph title="" pad=n transp=y yreverse=y
    min2=0.55 max2=0.75 
    plotcol=0 plotfat=12 wantaxis=n
    %s
    ''' % (par['labelattr']+par['labelrot']+' '+custom)

def secgrey(custom,par):
    return '''
    grey title="" pclip=100
    %s
    ''' % (par['labelattr']+par['labelrot']+' '+custom)
def secwigl(custom,par):
    return '''
    wiggle title="" pclip=100
    poly=y transp=y yreverse=y seemean=n wherexlabel=t
    %s
    ''' % (par['labelattr']+par['labelrot']+' '+custom)

# ------------------------------------------------------------
#def oswin(par):
#    return '''
#    window max2=%(xwin)g |
#    grey title="" screenratio=1 screenht=10 color=e
#    label1=%(lo)s unit1=%(uo)s
#    label2=%(ls)s unit2=%(us)s min2=%(xmin)g max2=%(xwin)g
#    %(labelattr)s %(labelrot)s
#    '''%par

def osall(par):
    return '''
    grey title="" screenratio=0.5 screenht=7 color=e
    label1=%(lo)s unit1=%(uo)s min1=0
    label2=%(ls)s unit2=%(us)s min2=%(xmin)g max2=%(xmax)g
    %(labelattr)s %(labelrot)s
    '''%par

#def hmwin(par):
#    return '''
#    window max2=%(xwin)g |
#    grey title="" screenratio=0.5 screenht=5 color=e
#    label1=%(lh)s unit1=%(uh)s
#    label2=%(lm)s unit2=%(um)s min2=%(xmin)g max2=%(xwin)g
#    %(labelattr)s %(labelrot)s
#    '''%par

def hmall(par):
    return '''
    grey title="" screenratio=0.25 screenht=3.5 color=e
    label1=%(lh)s unit1=%(uh)s min1=0
    label2=%(lm)s unit2=%(um)s min2=%(xmin)g max2=%(xmax)g
    %(labelattr)s %(labelrot)s
    '''%par

# ------------------------------------------------------------
def gettraces(traces,par):
    
    datafile = 'DATA/vikingGraben/seismic.sgy'
    data=traces+'raw'
    Flow([data,data+'-t','./'+data+'-h','./'+data+'-b'],
         None,
         '''
         segyread tape=%s
         tfile=${TARGETS[1]}
         hfile=${TARGETS[2]}
         bfile=${TARGETS[3]} |
         put n2=120 d2=1 o2=0 n3=1001 d3=1 o3=101 
         '''%datafile,stdin=0)
    
    # insert missing shots
    missing = ['180',      '181',
               '188','189','190',
               '549','550','551',
               '859','860','861']
    Flow(data+'mis2',data,'window n3=2 | math output=0')
    Flow(data+'mis3',data,'window n3=3 | math output=0')
    
    numA= 180-101
    numB= 188-181-1
    numC= 549-190-1
    numD= 859-551-1
    numE=1112-861
    
    Flow(data+'A',data,'window f3=0  n3=%d'%(numA))
    Flow(data+'B',data,'window f3=%d n3=%d'%(numA,numB))
    Flow(data+'C',data,'window f3=%d n3=%d'%(numA+numB,numC))
    Flow(data+'D',data,'window f3=%d n3=%d'%(numA+numB+numC,numD))
    Flow(data+'E',data,'window f3=%d n3=%d'%(numA+numB+numC+numD,numE))
    
    Flow(traces,[data+'A',data+'mis2',data+'B',data+'mis3',
                 data+'C',data+'mis3',data+'D',data+'mis3',
                 data+'E'],
         '''
         cat axis=3 space=n ${SOURCES[1:9]} |
         reverse which=2 opt=i |
         put n2=%d n3=1
         '''%(par['ns']*par['no']))

#    Result(traces+'QC',
#           traces,
#           'window n1=1 f1=1000 | put n1=%(no)d n2=%(ns)d o1=0 o2=0 d1=1 d2=1 |'%par +
#           '''
#           grey title="" color=E
#           label1=%(lo)s unit1="#"
#           label2=%(ls)s unit2="#"
#           %(labelattr)s %(labelrot)s
#           '''%par)

# ------------------------------------------------------------
def sco(sco,par):
    Flow(sco,None,
         '''
         math output="x2"
         n1=%(no)d o1=%(oo)g d1=%(do)g
         n2=%(ns)d o2=%(os)g d2=%(ds)g |
         '''%par +'put n2=1 n1=%d'%(par['ns']*par['no']))
def oco(oco,par):
    Flow(oco,None,
         '''
         math output="x1"
         n1=%(no)d o1=%(oo)g d1=%(do)g
         n2=%(ns)d o2=%(os)g d2=%(ds)g |
         '''%par +'put n2=1 n1=%d'%(par['ns']*par['no']))

def mco(mid,sou,off,par):
    Flow(mid,[off,sou],
         'math s=${SOURCES[1]} output="s+0.5*input"')

def hco(hof,off,par):
    Flow(hof,[off],
         'math output="0.5*input"')
    
# ------------------------------------------------------------
# make shots
def makes(shot,data,par):
    sco(shot+'-ss',par)
    oco(shot+'-oo',par)
#    Result(shot+'OS',[shot+'-oo',shot+'-ss'],
#           'cat axis=2 space=n ${SOURCES[1]} | transp | ' +
#           '''
#           dd type=complex |
#           graph title="" symbol=. transp=y wherexlabel=t yreverse=y
#           label1=%(lo)s unit1=%(uo)s
#           label2=%(ls)s unit2=%(us)s min2=%(xmin)g max2=%(xmax)g
#           %(labelattr)s %(labelrot)s
#           '''%par)
        
    Flow(shot+'-si',shot+'-ss','math output="input/%(ds)g"'%par)
    Flow(shot+'-oi',shot+'-oo','math output="input/%(do)g"'%par)
    Flow(shot+'-os',[shot+'-oi',shot+'-si'],
         'cat axis=2 space=n ${SOURCES[1]} | transp | dd type=int')

    Flow(shot,[data,shot+'-os'],
         '''
         intbin head=${SOURCES[1]} xkey=0 ykey=1 |
         put                 unit1=%(ut)s label1=%(lt)s
         o2=%(oo)g d2=%(do)g unit2=%(uo)s label2=%(lo)s         
         o3=%(os)g d3=%(ds)g unit3=%(us)s label3=%(ls)s
         ''' %par)

#    Result(shot+'QCwin',shot,'window n1=1 f1=1000 |' + oswin(par))
    Result(shot+'QCall',shot,'window n1=1 f1=1000 |' + osall(par))
    
# ------------------------------------------------------------
def hideshots(scut,shot,mone,mask,par):

    Result(mask+'QCall',mone,osall(par))
    
    Flow(scut,[shot,mask],'add mode=p ${SOURCES[1]}')
    Result(scut+'QCall',scut,'window n1=1 f1=1000 |' + osall(par))
    
# ------------------------------------------------------------
def masktraces(subset,scut,par):
    Flow(subset,scut,'put n2=%d n3=1'%(par['ns']*par['no']))

# ------------------------------------------------------------
# make cmps
def makec(cmps,data,par):
    sco(cmps+'-ss',par)
    oco(cmps+'-oo',par)

    mco(cmps+'-mm',cmps+'-ss',cmps+'-oo',par)
    hco(cmps+'-hh',           cmps+'-oo',par)
#    Result(cmps+'MH',[cmps+'-hh',cmps+'-mm'],
#           'cat axis=2 space=n ${SOURCES[1]} | transp | ' +
#           '''
#           dd type=complex |
#           graph title="" symbol=. transp=y wherexlabel=t yreverse=y
#           label1=%(lh)s unit1=%(uh)s
#           label2=%(lm)s unit2=%(um)s min2=%(xmin)g max2=%(xmax)g
#           %(labelattr)s %(labelrot)s
#           '''%par)

    Flow(cmps+'-mi',cmps+'-mm','math output="input/%g"'%(par['ds']/2))
    Flow(cmps+'-hi',cmps+'-hh','math output="input/%g"'%(par['do']/2))
    Flow(cmps+'-mh',[cmps+'-hi',cmps+'-mi'],
         'cat axis=2 space=n ${SOURCES[1]} | transp | dd type=int')
    
    Flow(cmps,[data,cmps+'-mh'],
         '''
         intbin head=${SOURCES[1]} xkey=0 ykey=1 |
         put                 unit1=%(ut)s label1=%(lt)s 
         o2=%(oh)g d2=%(dh)g unit2=%(uh)s label2=%(lh)s
         o3=%(om)g d3=%(dm)g unit3=%(um)s label3=%(lm)s
         '''%par)
    
#    Result(cmps+'QCwin',cmps,'window n1=1 f1=1000 |' + hmwin(par))    
    Result(cmps+'QCall',cmps,'window n1=1 f1=1000 |' + hmall(par))

# ------------------------------------------------------------
def makef(fold,cmps,par):

    Flow(fold,cmps,
         '''
         window n1=1 f1=1000  |
         scale axis=123 |
         math output="abs(input)" |
         mask min=1e-6 max=1 |
         dd type=float
         '''%par)

#    Result(fold+'QCwin',fold,hmwin(par))
    Result(fold+'QCall',fold,hmall(par))

#    Result(fold+'PRwin',
#           fold,
#           '''
#           window max2=%(xwin)g |
#           stack axis=1 norm=n |
#           graph title="" plotfat=2 symbol=*
#           wherexlabel=t screenratio=0.5 screenht=5
#           label2="fold" unit2=""     min2=0 max2=100
#           label1=%(lm)s unit1=%(um)s min1=%(xmin)g max1=%(xwin)g
#           %(labelattr)s %(labelrot)s
#           '''%par)
    
    Result(fold+'PRall',
           fold,
           '''
           stack axis=1 norm=n |
           graph title="" plotfat=2 symbol=. symbolsz=5
           wherexlabel=t screenratio=0.25 screenht=3.5
           label2="fold" unit2=""     min2=0 max2=65
           label1=%(lm)s unit1=%(um)s min1=%(xmin)g max1=%(xmax)g
           %(labelattr)s %(labelrot)s
           '''%par)

    
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
# ------------------------------------------------------------
def makeshots(shot,data,par):
    
    Flow(shot+'-ss',data+'-t','dd type=float | headermath output="fldr*25" | window')
    Flow(shot+'-oo',data+'-t','dd type=float | headermath output="offset"  | window')
    
    # create sraw(t,o,s): o=full offset
    Flow(shot+'-si',shot+'-ss','math output=input/25')
    Flow(shot+'-oi',shot+'-oo','math output=input/25')
    Flow(shot+'-os',[shot+'-oi',shot+'-si'],
         'cat axis=2 space=n ${SOURCES[1]} | transp | dd type=int')
    Flow(shot+'-raw',[data,shot+'-os'],
         'intbin head=${SOURCES[1]} xkey=0 ykey=1')
    Flow(shot,shot+'-raw',
         '''
         put         unit1=%s label1=t 
         o2=%g d2=%g unit2=%s label2=o
         o3=%g d3=%g unit3=%s label3=s
         ''' % (par['ut'],
                -3.237,0.025,par['ux'],
                0,0.025,par['ux']
                ))
        
# ------------------------------------------------------------
def makecmps(cmps,data,par):

    Flow(cmps+'-ss',data+'-t','dd type=float | headermath output="fldr*25" | window')
    Flow(cmps+'-oo',data+'-t','dd type=float | headermath output="offset"  | window')

    Flow(cmps+'-mm',[cmps+'-oo',cmps+'-ss'],
         'math o=${SOURCES[0]} s=${SOURCES[1]} output=s+o/2')
    Flow(cmps+'-hh',[cmps+'-oo'     ],
         'math o=${SOURCES[0]}                 output=o/2')
    
    Flow(cmps+'-mi',cmps+'-mm','math output=input/12.5')
    Flow(cmps+'-hi',cmps+'-hh','math output=input/12.5')
    Flow(cmps+'-mh',[cmps+'-hi',cmps+'-mi'],
         'cat axis=2 space=n ${SOURCES[1]} | transp | dd type=int')
    Flow(cmps+'-raw',[data,cmps+'-mh'],
         'intbin head=${SOURCES[1]} xkey=0 ykey=1')
    Flow(cmps,cmps+'-raw',
         '''
         put         unit1=%s label1=t 
         o2=%g d2=%g unit2=%s label2=h
         o3=%g d3=%g unit3=%s label3=m |
         window j3=2 f3=1
         ''' % (par['ut'],
                -1.6185,0.0125,par['ux'],
                0.00000,0.0125,par['ux']
                ))

