def date():
    sp.getoutput('date')

def cal():
    sp.getoutput('cal')

def dataname():
    if(n==3):
        string="data"
    else:
        string="name"
    out=sp.getoutput('jps')
    out=out.split()
    ip=input("Enter namenode ip")
    folder=input("Enter distributed folder")
    core=et.parse('/etc/hadoop/core-site.xml')
    hdfs=et.parse('/etc/hadoop/hdfs-site.xml')
    croot=core.getroot()
    hroot=hdfs.getroot()
    if(len(croot)>=1 and len(hroot)>=1):
        if(croot[0][1]=='hdfs://'+ip+':9001' and hroot[0][1]==folder and hroot[0][0]=='dfs.'+string+'.dir'):

            if(('DataNode' in out) or ('NameNode' in out)):
                print(string+"node is already running")
            else:
                sp.getoutput("hadoop-daemon.sh start "+string+"node")
        else:
            sp.getstatusoutput('hadoop-daemon.sh stop datanode')
            sp.getstatusoutput('hadoop-daemon.sh stop namenode')
            croot[0][1]=='hdfs://'+ip+':9001'
            hroot[0][1]==folder
            hroot[0][0]=='dfs.'+string+'.dir'
            core.write('/etc/hadoop/core-site.xml')
            hdfs.write("/etc/hadoop/hdfs-site.xml")
            sp.getoutput("hadoop-daemon.sh start "+string+"node")
    else:
        prop=et.Element("property")
        name=et.Element("name")
        value=et.Element("value")
        name.text="fs.default.name"
        value.text='hdfs://'+ip+':9001'
        prop.append(name)
        prop.append(value)
        croot.append(prop)
        core.write('/etc/hadoop/core-site.xml')
        name.text="dfs."+string+'.dir'
        value.text=folder
        hdfs.write('/etc/hadoop/hdfs-site.xml')
        sp.getoutput("hadoop-daemon.sh start "+string+"node")
    print(string+"node is running")
    sp.getoutput('jps')
def docker():
    sp.getoutput("systemctl start docker")
    print("1.pull an image\n \
            2.start a new container\n \
            3.start a stopped container\n \
            4.delete a container\n \
            5.delete an image\n \
            6.delete all containers\n \
            7.copy files between  base os and conatiner")
    n=int(input("choose which u want : "))
    if(n==1):
        image=input('Enter image name with version : ')
        sp.getoutput('docker pull '+image)
    elif(n==2):
        print(sp.getoutput("docker images"))
        container=input("Enter image to launch with name optionally as 'image n                          ame_to_container': ")
        container=container.split()
        print(container)
        x=sp.getstatusoutput('docker run -it --name '+container[1]+" "+container[0])
        print(x)
    elif(n==3):
        print(sp.getoutput("docker ps -a"))
        s=input("[better to enter the container name]")
        sp.getoutput("docker start "+s)
        sp.getoutput("docker attach "+s)
    elif(n==4):
        c=input("Enter which container to delete : ")
        sp.getoutput("docker rm -f "+c)
    elif(n==5):
        c=input("Enter which to delete to delete")
        sp.getoutput("docker rmi -f "+c)
    elif(n==7):
        print("Enter the container file location like <container_name/ID:file_path>")
        src=input("Enter source file location/path: ")
        dest=input("Enter destination file location/path: ")
        sp.getoutput("docker cp "+src+" "+dest)
    elif(n==6):
        sp.getoutput("docker rm `docker ps -a -q`")
        sp.getoutput("docker ps -a")
        print("containers were deleted")
def webserver():
    sp.getoutput('systemctl start httpd')
    print("web server started")
def aws():
    import boto3
    access=input("aws_access_key_id(press enter to read from credentials,config files) :")
    key=input("aws_secret_key :")
    region=input("region :")
    if(access and key and region):
        s3=boto3.resource('s3',region_name=region,aws_access_key_id=access,aws_secret_access_key= key)
        ec2=boto3.resource('ec2',region_name=region,aws_access_key_id=access,aws_secret_access_key=key)
        session=boto3.session.Session(aws_access_key_id=access,aws_secret_access_key=key,region_name=region)
    else:
        s3=boto3.resource('s3')
        ec2=boto3.resource('ec2')
    print('1.create an EC2 instance\n \
            2.create security-group\n\
            3.create S3 instance\n \
            4.Create EBS volume\n \
            5.Attach EBS volume\n \
            6.upload to S3 bucket\n\
            7.Create key-pair\n\
            8.create Clodfront\n\
            9.Add ingree or egree rules\
            ')
    n=int(input('Enter your option'))
    while(n):
        if(n==7):
            name=input("KeyPair name: ")
            ec2.create_key_pair(KeyName=key)
            print("key created")
        if(n==1):
            image=input("Image_id ('ami-xxxx':")
            inst_type=input("Instance_type :")
            count=int(input("Count :"))
            key=input("KeyName :")
            sg=input('Securitygroup Ids(separated by space): ')
            sg=sg.split()
            '''ec2=boto3.resource('ec2',region_name=region,aws_access_key_id=access,aws_secret_access_key=key)'''
            result=ec2.create_instances(MaxCount=count,MinCount=1,SecurityGroupIds=sg,ImageId=image,InstanceType=inst_type,KeyName=key)
            print("Instance created with"+result[0].instance_id)
        elif(n==2):
            name=input("Name for security group: ")
            desc=input("Description: ")
            i=ec2.create_security_group(Description=desc,GroupName=name)
            print("security group created with id "+i.id)
        elif(n==3):#adding,removing inbound rules
            d=input('Add /Remove inbound rules(A/R): ')
            
            i=input('Security group id: ')
            Ip=input('CidrIp(press ENTER to skip): ')
            sgn=input('Securitygroup name: ')
            fport=input('FromPort/code: ')
            tport=input('ToPort/code: ')
            protocol=input('Protocol: ')
            sg=ec2.SecurityGroup(i)
            if(d=='A'):
                x=sg.authorize_ingress(CidrIp=Ip or '',GroupName=sgn,FromPort=fport,ToPort=tport,IpProtocol=protocol)
            elif(d=='R'):
                x=sg.revoke_ingress(CidrIp=Ip or '',GroupName=sgn,FromPort=fport,ToPort=tport,IpProtocol=protocol)

        elif(n==3):
            name=input("Enter unique bucket name :")
            loc=input("Region")
            '''s3=boto3.resource('s3',region_name=region,aws_access_key_id=access,aws_secret_access_key=key)'''
            s3.create_bucket(Bucket=name,CreateBucketConfiguration={'LocationConstraint':loc})
        elif(n==4):
            size=int(input("Size :"))
            AZ=input("Availability Zone :")
            t=input('VOlumeType:like (gp2) :')
            vol=ec2.create_volume(AvailabilityZone=AZ,Size=size,VolumeType=t)
            print("volume created with id"+vol.volume_id)
        elif(n==5):
            vol=input("VOlume-id: ")
            instance=input("Instance-id ('ixxxx': ")
            d=input("device-name(/dev/xvdf): ")
            if(d is None):
                d='/dev/xvdf'
            V=ec2.Volume(vol)
            response=V.attach_to_instance(InstanceId=instance,Device=d)
            print("Volume attached")

        elif(n==6):
            bucket=input("Bucket : ")
            f=input("FIle: ")
            obj=input("Object name: ")
            s3=session.client('s3')
            response=s3.upload_file(f,bucket,obj)
            print("file uploaded")
        n=int(input("Enter choice (0 to quit): "))
def partitions():
    import time
    print('1:list available partitions\t  2:create new partition\t \
            3.delete existed partition\t \
            4.create logical volume\t 5.create vg\t 6.create pv\t 7.format,mount partition(or lv)\t 8.extend lv\t 9.shrink lv')
    n=int(input('Enter option(0 to quit): '))
    while(1<=n<=3):
        disk=input('Disk name: ')
        l=['fdisk',disk]
        x=sp.Popen(l,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT)
        time.sleep(5)
        x.stdin.write(b'p\n')
        time.sleep(5)
        x.stdin.flush()
        time.sleep(5)
        x.stdin.write(b'q\n')
        time.sleep(5)
        x.stdin.flush()
        time.sleep(5)
        x.stdin.close()
        y=x.stdout.readlines()
        le=len(y[:-1])
        print(le)
        for i in y[13:le-1]:
            print(i.decode())
        x.kill()
        if(n==2):
            #disk=input('Disk to partition: ')
            #l=['fdisk',disk]
            x=sp.Popen(l,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT)
            size=input("Enter size : ")+'\n'
            #p=input("Primary or Extended(p/e): ")+'\n'
            if(le>18):
                inp=[b'n\n',b'\n',bytes(size.encode()),b'w\n']
            elif(le==18):
                p=input("Primary or Extended(p/e): ")+'\n'
                inp=[b'n\n',bytes(p.encode()),b'\n',bytes(size.encode()),b'w\n']
            else:
                p=input("Primary or Extended(p/e): ")+'\n'
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
            time.sleep(5)
            x.kill()
            print('partition deleted')
        n=int(input('Enter option (0 to quit): '))
    while(4<=n<=9):
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
        elif(n==5):
            pv=input('Enter physical vols(separated by space): ')
            pv=pv.split()
            name=input('Name of vg(for creating or extending): ')
            x=sp.getstatusoutput('vgcreate '+name)
            for i in pv:
                x=sp.getoutput('vgextend '+name+' '+i)
            print('vg created and extended'+name)
            print(sp.getoutput('vgdisplay '+name))
        elif(n==6):
            name=input('Enter device to create as pv: ')
            x=sp.getstatusoutput('pvcreate '+name)
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

            x=sp.getoutput('mkdir '+d)
            sp.getstatusoutput('mount '+part+' '+d)
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
                    size=size+y
                else:
                    actual=float(actual)*1024
                    d=int(float(actual)-float(size))
                    d=str(d)+'M'
                    size=size+y
                print(size,d)

                sp.getoutput('resize2fs '+lv+' '+d)
                x=sp.Popen(['lvreduce',lv,'--size',d],stdin=sp.PIPE,stdout=sp.PIPE)
                x.communicate(input=b'y\n')
                print('reduced...')
                print(sp.getoutput('lvdisplay '+lv))
                print('mounting again...')
                x=sp.getoutput('mount '+lv+' '+mp)
    n=int(input('Enter option(0 for quit): '))                

if(__name__=='__main__'):
    import subprocess as sp
    import xml.etree.ElementTree as et
  
    print("WELCOME TO REMOTE EXECUTION".center(70,'*'))
    '''print("menu is \n \
        1.date \n \
        2.cal \n \
        3.configure and start datanode \n \
        4.configure ,start namenode \n \
        5.start webserver \n\
        6.start and launch docker container\n\
        7.make partitions\n\
        8.working with aws")'''
    #=int(input("Enter which option you want: "))
    #n1=input("Choose local or remote execution(l/r): ")

    dl={1:date,2:cal,3:dataname,4:dataname,5:webserver,6:docker,7:partitions,8:aws}
    '''if(n1=='r'):
        ip=input("Enter ip address of remote machine: ")
        x=sp.getstatusoutput('ssh '+ip+' python3 /root/menu.py')
        if(x):
            sp.getoutput('scp menu.py '+ip+':/root')
            x=sp.getstatusoutput('ssh '+ip+' python3 /root/menu.py')'''
    #elif(n1=='l'):
    n=int(input("Enter which option you want(0 to quit): "))
    while(n):
            #=int(input("Enter which option you want"))
        result=dl[n]()
        n=int(input("Enter choice(0 to quit): "))

