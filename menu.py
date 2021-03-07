def date():
    print(sp.getoutput('date'))

def cal():
    print(sp.getoutput('cal'))
def client():
    ip=input("Enter namenode ip with port num: ")
    try:
        core=et.parse('/etc/hadoop/core-site.xml')
        hdfs=et.parse('/etc/hadoop/hdfs-site.xml')
    except ParseError:
        print('Format the xml tags in conf files properly')
    croot=core.getroot()
    hroot=hdfs.getroot()
    if(len(croot)>=1):
        croot[0][1].text='hdfs://'+ip
    else:
        prop=et.Element("property")
        name=et.Element("name")
        value=et.Element("value")
        name.text="fs.default.name"
        value.text='hdfs://'+ip
        prop.append(name)
        prop.append(value)
        croot.append(prop)
    if len(hroot)>=1:
        hroot[0][0].text=""
        hroot[0][1].text=""
    else:
        prop=et.Element("property")
        name=et.Element("name")
        value=et.Element("value")
        prop.append(name)
        prop.append(value)
        hroot.append(prop)
    hdfs.write("/etc/hadoop/hdfs-site.xml",encoding='utf-8',xml_declaration=True)
    core.write('/etc/hadoop/core-site.xml',encoding='utf-8',xml_declaration=True)
    sp.getoutput("hadoop-daemon.sh start datanode")
    print('Configured as client....')

def dataname():
    if(n==3):
        string="data" #configure as datanode
    else:
        string="name" #conf as namenode
    out=sp.getoutput('jps')
    out=out.split()
    ip=input("Enter namenode ip with port number: ")
    folder=input("Enter distributed folder: ")
    try:
        core=et.parse('/etc/hadoop/core-site.xml')
        hdfs=et.parse('/etc/hadoop/hdfs-site.xml')
    except ParseError:
        print('Format the xml tags in conf files properly')
    croot=core.getroot()
    hroot=hdfs.getroot()
    if(len(croot)>=1 and len(hroot)>=1): #conf file is already changed and added some tags
        if(croot[0][1].text=='hdfs://'+ip and hroot[0][1].text==folder and hroot[0][0].text=='dfs.'+string+'.dir'):
            #checking whether the ip and folder name were already written correctly and service is running
            if(('DataNode' in out) or ('NameNode' in out)):
                print(string+"node is already running")
            else:
                sp.getoutput("hadoop-daemon.sh start "+string+"node")
        else: #conf files has conf with some other namenode prevoiusly
            sp.getstatusoutput('hadoop-daemon.sh stop datanode')
            sp.getstatusoutput('hadoop-daemon.sh stop namenode')
            croot[0][1].text='hdfs://'+ip
            hroot[0][1].text=folder
            hroot[0][0].text='dfs.'+string+'.dir'
            core.write('/etc/hadoop/core-site.xml',encoding='utf-8',xml_declaration=True)
            hdfs.write("/etc/hadoop/hdfs-site.xml",encoding='utf-8',xml_declaration=True)
            sp.getoutput("hadoop-daemon.sh start "+string+"node")
    else: #there are no tags under <configuration> tag.so creating tags
        prop=et.Element("property")
        name=et.Element("name")
        value=et.Element("value")
        name.text="fs.default.name"
        value.text='hdfs://'+ip
        prop.append(name)
        prop.append(value)
        croot.append(prop)
        core.write('/etc/hadoop/core-site.xml',encoding='utf-8',xml_declaration=True)
        name.text="dfs."+string+'.dir'
        value.text=folder
        hdfs.write('/etc/hadoop/hdfs-site.xml',encoding='utf-8',xml_declaration=True)
        sp.getoutput("hadoop-daemon.sh start "+string+"node")
    print(string+"node is running")
    print(sp.getoutput('jps'))
def docker():
    import docker
    sp.getoutput("systemctl start docker")
    client=docker.from_env()
    print("1.pull an image\n \
            2.start a new container\n \
            3.start a stopped container\n \
            4.delete a container\n \
            5.delete an image\n \
            6.delete all containers\n \
            7.copy files between  base os and conatiner")
    n=int(input("choose which u want : "))
    while(n):
        if(n==1):
            image=input('Enter image name with version(image:version): ')
            sp.getoutput('docker pull '+image)
            print(client.images.list())
        elif(n==2):
            print('exiting images are: ')
            for i in client.images.list():
                print(i.tags[0],'\t',end="")
            #print(sp.getoutput("docker images"))
            container=input("\nImage name <Image:version tag_name>: ")
            container=container.split()
            #client.containers.run(container)
            #print(container)
            if(len(container)==2):
                x=sp.run('docker run -it --name '+container[1]+" "+container[0],shell=True)
            else:
                x=sp.run('docker run -it'+container[0],shell=True)
            #print(x)
        elif(n==3):
            print(sp.getoutput("docker ps -a")) #client.containers.list(all)
            s=input("container name/id: ")
            x=sp.run("docker start "+s,shell=True) #conta=client.containers.start(s)
            x=sp.run("docker attach "+s,shell=True) #conta.attach(True,True,True)
        elif(n==4):
            print(sp.getoutput('docker ps -a')) # client.images.list
            c=input("Enter which container to delete : ")
            x=sp.run("docker rm -f "+c,shell=True)
        elif(n==5):
            print(sp.getoutput('docker images'))
            c=input("Enter which to delete: ")
            x=sp.getoutput("docker rmi -f "+c)
        elif(n==7):
            print("Enter the container file location in the format <container_name/ID:file_path>")
            src=input("Enter source file location/path: ")
            dest=input("Enter destination file location/path: ")
            c=input("container name/id: ")
            client.containers.get(c).start()
            sp.getoutput("docker cp "+src+" "+dest)
        elif(n==6):
            sp.getoutput("docker rm `docker ps -a -q`")
            sp.getoutput("docker ps -a")
            print("containers were deleted")
        n=int(input("Enter option to work with docker: "))
def webserver():
    sp.getoutput('systemctl start httpd')
    print("web server started")
def aws():
    import boto3
    access=input("aws_access_key_id(press enter to read from credentials,config files):")
    key=input("aws_secret_key :")
    region=input("region :")
    if(access and key and region):
        s3=boto3.resource('s3',region_name=region,aws_access_key_id=access,aws_secret_access_key= key)
        ec2=boto3.resource('ec2',region_name=region,aws_access_key_id=access,aws_secret_access_key=key)
        session=boto3.session.Session(aws_access_key_id=access,aws_secret_access_key=key,region_name=region)
    else:#uses credentials from config,credential files 
        s3=boto3.resource('s3')
        ec2=boto3.resource('ec2')
    print('1.create an EC2 instance\n \
            2.create security group\n \
            3.Adding/Removing inbound rules to security group\n \
            4.create S3 instance\n \
            5.Create EBS volume\n \
            6.Attach EBS volume to EC2 instance\n \
            7.upload files to S3 bucket\n\
            8.Create key-pair\n \
            ')
    n=int(input('Enter your option: '))
    while(n):
        if(n==8):#creating key-pair
            name=input("KeyPair name: ")
            try:
                result=ec2.create_key_pair(KeyName=name)
                print("key created")
            except ClientError:
                print('Entered key already exists')
        elif(n==1): #creating ec2 instance
            image=input("Image_id ('ami-xxxx'): ")
            inst_type=input("Instance_type: ")
            count=int(input("Count: "))
            key=input("KeyName: ")
            sg=input('Securitygroup Ids(separated by space): ')
            sg=sg.split()
            result=ec2.create_instances(MaxCount=count,MinCount=1,SecurityGroupIds=sg,ImageId=image,InstanceType=inst_type,KeyName=key)
            print("Instance created with id "+result[0].instance_id)
        elif(n==2): #creating sg
            name=input("Name for security group: ")
            desc=input("Description: ")
            i=ec2.create_security_group(Description=desc,GroupName=name)
            print("security group created with id "+i.id)
        elif(n==3):#adding,removing inbound rules
            d=input('Add /Remove inbound rules(A/R): ')
            
            i=input('Security group id: ')
            Ip=input('CidrIp/Security group name: ')
            sgname=""
            if(Ip[0:2]=='sg'):
                sgname=Ip
                IP=""
            fport=int(input('FromPort/code: '))
            tport=int(input('ToPort/code: '))
            protocol=input('Protocol: ')
            sg=ec2.SecurityGroup(i)
            if(d=='A'):
                x=sg.authorize_ingress(CidrIp=Ip or '',GroupName=sgname or '',FromPort=fport,ToPort=tport,IpProtocol=protocol)
            elif(d=='R'):
                x=sg.revoke_ingress(CidrIp=Ip or '',GroupName=sgname or '',FromPort=fport,ToPort=tport,IpProtocol=protocol)
        elif(n==4):#creating s3 bucket
            loc=input("Region: ")
            while(True):
                name=input("Enter unique bucket name :")
                try:
                    s3.create_bucket(Bucket=name,CreateBucketConfiguration={'LocationConstraint':loc})
                    break
                except:
                    print("Bucketname already exists in the namespace.")
            print('Bucket created succesfully....')
        elif(n==5):#creating EBS volume
            try:
                size=input("Size(multiple of 1Gib)/snapshot Id :")
                si=''
                if(size[0:4]=='snap'):
                    si=size
                    size=''
                else:
                    size=int(size)
            except:
                print('Enter an integer for size.')
                size=int(input('size: '))
            AZ=input("Availability Zone(like ap-south-1a) :")
            t=input('VOlumeType:like (gp2) :')
            try:
                vol=ec2.create_volume(AvailabilityZone=AZ,Size=size or '',SnapshotId=si or '',VolumeType=t)
            except:
                print('Enter all parameters in correct format.')
            print("volume created with id "+vol.volume_id)
        elif(n==6):#attaching vol to ec2 instance
            vol=input("VOlume-id: ")
            instance=input("Instance-id ('ixxxx': ")
            d=input("device-name(/dev/xvdf): ")
            if(d== ''):
                d='/dev/xvdf'
            V=ec2.Volume(vol)
            response=V.attach_to_instance(InstanceId=instance,Device=d)
            print("Volume attached")

        elif(n==7):#uploading files to s3
            bucket=input("Bucket : ")
            f=input("FIle: ")
            obj=input("Object name: ")
           #s3=session.client('s3')
            response=s3.Bucket(bucket).upload_file(f,obj)
            print("file uploaded")
        n=int(input("Enter choice (0 to quit): "))
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
    
if(__name__=='__main__'):
    import subprocess as sp
    import xml.etree.ElementTree as et
    print("WELCOME".center(60,'*'))
    print("menu is \n \
           1.date \n \
           2.cal \n \
           3.configure and start datanode \n \
           4.configure ,start namenode \n \
           5.configure and start hadoop client\n\
           6.start webserver \n\
           7.working with docker containers\n\
           8.working with partitions(static,dynamic)\n\
           9.working with aws")
    #=int(input("Enter which option you want: "))
    n1=input("Choose local or remote execution(l/r): ")

    dl={1:date,2:cal,3:dataname,4:dataname,5:client,6:webserver,7:docker,8:partitions,9:aws}
    if(n1=='r'):
        ip=input("Enter ip address of remote machine: ")
        x=sp.run('ssh '+ip+' python3 remote2.py',shell=True)
        if(x.returncode):
            print("transferring the file..")
            sp.getoutput('scp remote2.py '+ip+':remote2.py')
            x=sp.run('ssh '+ip+' python3 remote2.py',shell=True)
    elif(n1=='l'):
        n=int(input("Enter which option you want: "))
        while(n):
            #=int(input("Enter which option you want"))
            result=dl[n]()
            n=int(input("Enter choice(0 to quit): "))
    else:
        print('Enter valid letter')

