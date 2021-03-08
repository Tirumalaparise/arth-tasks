def partitions():
    import time
    print('1:list available partitions\n2:create new partition\n \
            3.delete existed partition\n \
            4.create logical volume\n 5.create/extend vg\n 6.create pv\n 7.format,mount partition(or lv)\n 8.extend lv\n 9.shrink lv')
    n=int(input('Enter option(0 to quit): '))
    while(n):
        if(1<=n<=3):
            try:
                disk=input('Disk name: ') 
                l=['fdisk',disk]
                x=sp.Popen(l,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT)
            #time.sleep(5)
                x.stdin.write(b'p\n')
            #time.sleep(5)
                x.stdin.flush()
                time.sleep(5)
                x.stdin.write(b'q\n')#ends process 
            #time.sleep(5)
                x.stdin.flush()
                time.sleep(5)
                x.stdin.close()
                y=x.stdout.readlines()#reads o/p after process ends.
                le=len(y[:-1])#we require this len (num of partitions created already) to create or delete a partition.
            except:
                print('check  disk name once')
                partitions()
            print('Available partitions in the disk are: ')
            
            for i in y[13:le-1]:
                print(i.decode())#available partitions are listed everytime user selects a choice that is  related to partitions
            x.kill()
            
            if(n==2):
            #disk=input('Disk to partition: ')
            #l=['fdisk',disk]
                x=sp.Popen(l,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT)
                size='+'+input("Enter size size{K,M,G,T,P}: ")+'\n'
            #p=input("Primary or Extended(p/e): ")+'\n'
                if(le>18):
                    inp=[b'n\n',b'\n',bytes(size.encode()),b'w\n']#creating extended partition by default when 4 P are already created
                elif(le==18):
                    p=input("Primary or Extended(p/e): ")+'\n' #creating the 4 partition
                    inp=[b'n\n',bytes(p.encode()),b'\n',bytes(size.encode()),b'w\n']
                else:
                    p=input("Primary or Extended(p/e): ")+'\n' #creation 1st or 2nd or 3rd partition
                    inp=[b'n\n',bytes(p.encode()),b'\n',b'\n',bytes(size.encode()),b'w\n']
                for i in inp:
                    x.stdin.write(i)
                    x.stdin.flush()
                    time.sleep(10)
                    #time.sleep(5)
                x.stdin.close()
                time.sleep(5)
                x.kill()
                print('partition created')

            elif(n==3):
                x=sp.Popen(l,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT)
                num=input('Which partition(num>=1): ')+'\n'
                inp=[b'd\n',bytes(num.encode()),b'w\n']
                for i in inp:
                    x.stdin.write(i)
                    time.sleep(5)
                    x.stdin.flush()
                    time.sleep(5)
                x.stdin.close()
                #time.sleep(5)
                x.kill()
                print('partition deleted')
            #n=int(input('Enter option (0 to quit): '))
            #x.stdin.close()
            #x.kill()
    #while(4<=n<=9):
        else:
            if(n==4):
                vg=input('VG name: ')
                size=input('Size: ')
                name=input('Name for lv: ')
                x=sp.getstatusoutput('lvcreate '+vg+' --size '+size+' --name '+name)
                if(x[0]):
                    print('check '+vg+' size or other things and try again')
                else:
                    print('lv created')
                    print(sp.getoutput('lvdisplay '+vg+'/'+name))
            elif(n==5): #vgcreate
                pv=input('Enter physical vols(separated by space): ')
                pv=pv.split()
                name=input('Name of vg(for creating or extending): ')
                x=sp.getstatusoutput('vgdisplay '+name)#vg can't be created without pv
                if(x[0]):
                    sp.getstatusoutput('vgcreate '+name+' '+pv[0])
                    for i in pv[1:]:
                        x=sp.getoutput('vgextend '+name+' '+i)
                    print('vg created')
                else:
                    for i in pv:
                        x=sp.getoutput('vgextend '+name+' '+i)
                        print('vg extended')
                print(sp.getoutput('vgdisplay '+name))
            elif(n==6):
                name=input('Enter device to create as pv: ')
                x=sp.getstatusoutput('pvcreate '+name)
                if(x[0]):
                    print(x[1])
                else:
                    print(sp.getoutput('pvdisplay '+name))
                    print('pv created')
            elif(n==7):
                f=input('Enter format type(default ext4): ')
                if(not(f)):
                    f='ext4'
                part=input('Partition name: ')
                sp.getoutput('mkfs.'+f+' '+part)
                print('format done,mounting...')
                d=input('mount point(creates new dir or uses existing dir): ')
            
                sp.getoutput('mkdir '+d)
                x=sp.getstatusoutput('mount '+part+' '+d)
                if(x[0]):
                    print(x[1])
                else:
                    print(sp.getoutput('df -h'))
            elif(n==8):
                lv=input('LV name(/dev/vol-grp/lvname): ')
                size=input('Size to add: ')
                sp.getoutput('lvextend '+lv+' --size +'+size)
                sp.getoutput('resize2fs '+lv)
                x=sp.getoutput('lvdisplay '+lv)
                print(x)
                print('lv extended')
            elif(n==9):#reduce lv
                lv=input('LV name(/dev/volgrp/lvname): ')
                print(sp.getoutput('df -h'))
                mp=input('Mountpoint: ')
                sp.getoutput('umount '+mp)
                x=sp.call(['e2fsck','-f',lv])#e2fsck need terminal for interactive repairs
                if(not(x)):
                    actual=input('Actual LV size(M,G): ')
                
                    size=input('size to reduce(M,G): ')
                    x=actual[-1];y=size[-1];
                    actual=actual[:-1];size=size[:-1]
                    if(x==y):
                        d=int(float(actual)-float(size))
                        d=str(d)+x
                        #size=size+y
                    else:
                        actual=float(actual)*1024
                        d=int(float(actual)-float(size))
                        d=str(d)+'M'
                        #size=size+y
                    #print(size,d)
                    sp.getoutput('resize2fs '+lv+' '+d)
                    x=sp.Popen(['lvreduce',lv,'--size',d],stdin=sp.PIPE,stdout=sp.PIPE)
                    x.communicate(input=b'y\n')
                    print('reduced...')
                    print(sp.getoutput('lvdisplay '+lv))
                    print('mounting again...')
                    x=sp.getoutput('mount '+lv+' '+mp)
        n=int(input('Enter option(0 for quit): '))
partitions()