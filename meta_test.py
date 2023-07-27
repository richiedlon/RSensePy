import os

directory= os.path.basename(r"C:\Users\xeon\SoftwareDevProject_ope\LC09_L2SP_189053_20230412_20230414_02_T1")
namelist=[]
# print(directory)

for i in directory.split('_'):
    namelist.append(i)
    
# print(namelist)

mss=namelist[0]

def splitmss(mss):
    mission=mss[0]
    sensor=mss[1]
    satellite=mss[2:]

    return mission, sensor, satellite


mmsR = splitmss(mss)

mission=mmsR[0]
sensor=mmsR[1]
satellite=mmsR[2]
correction=namelist[1]
pr=namelist[2]

def splitpr(pr):
    path=pr[:3]
    row=pr[3:]

    return path, row

prR = splitpr(pr)

path=prR[0]
row=prR[1]
acqui_date=namelist[3]
process_date=namelist[4]
coll_number=namelist[5]
coll_cat=namelist[6]  

# print(row)
