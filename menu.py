'''import subprocess as sp
import xml.etree.ElementTree as et

print("WELCOME".center(60,'*'))
print("menu is \
	1.date \
	2.cal \
	3.configure and start datanode \
	4.configure ,start namenode \
	5.start webserver \
        6.start and launch docker container")
n=int(input("Enter which option you want"))
n1=input("Choose local or remote execution(l/r)")

dl={1:date,2:cal,3:dataname,4:dataname,5:webserver,6:docker}
if(n1=='r'):
    ip=input("Enter ip address of remote machine")
    x=sp.getstatusoutput('ssh '+ip+' python3 /root/menu.py')
    if(x):
        sp.getoutput('scp menu.py '+ip+':/root')
    x=sp.getstatusoutput('ssh '+ip+' python3 /root/menu.py'+n)
elif(n1=='l'):
    result=dl[n]
    result()'''

def date():
    print(sp.getoutput('date'))

def cal():
    print(sp.getoutput('cal'))

def dataname():
    if(n==3):
        string="data"
    else:
        string="name"
    out=sp.getoutput('jps')
    out=out.split()
    ip=input("Enter namenode ip: ")
    folder=input("Enter distributed folder: ")
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
    print(sp.getoutput('jps'))
def docker():
    import docker
    client=docker.from_env()
    sp.getoutput("systemctl start docker")
    print("1.pull an image\n \
            2.start a new container\n \
            3.start a stopped container\n \
            4.delete a container\n \
            5.delete an image\n \
            6.delete all containers\n \
            7.copy files between  base os and conatiner")
    n=int(input("choose which u want : "))
<<<<<<< HEAD
    while(n):
        if(n==1):
            image=input('Enter image name with version : ')
            sp.getoutput('docker pull '+image)
            print(client.images.list())
        elif(n==2):
            print('exiting images are: ')
            for i in client.images.list():
                print(i.tags[0],'\t',end="")
            #print(sp.getoutput("docker images"))
            container=input("\nImage name <Image tag_name>: ")
            container=container.split()
            #client.containers.run(container)
            #print(container)
            if(len(container)==2):
                x=sp.run('docker run -it --name '+container[1]+" "+container[0],shell=True)
            else:
                x=sp.run('docker run -it'+container[0],shell=True)
            print(x)
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
            c=input("Enter which to delete")
            x=sp.getoutput("docker rmi -f "+c)
        elif(n==7):
            print("Enter the container file location like <container_name/ID:file_path>")
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
=======
    if(n==1):
        image=input('Enter image name with version : ')
        sp.getoutput('docker pull '+image)
    elif(n==2):
        print(sp.getoutput("docker images"))
        container=input("Enter image to launch with name optionally as 'image name_to_container': ")
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
>>>>>>> e9f407b57bcbf1542bb99ac38d27fe3b3e7e432e
def webserver():
    sp.getoutput('systemctl start httpd')
    print("web server started")
def aws():
    import boto3
    access=input("aws_access_key_id :")
    key=input("aws_secret_key :")
    region=input("region :")
    s3=boto3.resource('s3',region_name=region,aws_access_key_id=access,aws_secret_access_key= key)
    ec2=boto3.resource('ec2',region_name=region,aws_access_key_id=access,aws_secret_access_key=key)
    session=boto3.session.Session(aws_access_key_id=access,aws_secret_access_key=key,region_name=region)
    print('1.create an EC2 instance\n \
            2.create S3 instance\n \
            3.Create EBS volume\n \
            4.Attach EBS volume\n \
            5.upload to S3 bucket\n\
            6.Create key-pair\
            ')
    n=int(input('Enter your option'))
    while(n):
        if(n==6):
            name=input("KeyPair name: ")
            result=ec2.create_key_pair(KeyName=name)
            print("key created")
        elif(n==1):
            image=input("Image_id ('ami-xxxx':")
            inst_type=input("Instance_type :")
            count=int(input("Count :"))
            key=input("KeyName :")
            result=ec2.create_instances(MaxCount=count,MinCount=1,ImageId=image,InstanceType=inst_type,KeyName=key)
            print("Instance created with"+result[0].instance_id)
        elif(n==2):
            name=input("Enter unique bucket name :")
            loc=input("Region")
            s3.create_bucket(Bucket=name,CreateBucketConfiguration={'LocationConstraint':loc})
        elif(n==3):
            size=int(input("Size :"))
            aZ=input("Availability Zone :")
            t=input('VOlumeType:like (gp2) :')
            vol=ec2.create_volume(AvailabilityZone=aZ,Size=size,VolumeType=t)
            print("volume created with id"+vol.volume_id)
        elif(n==4):
            vol=input("VOlume-id: ")
            instance=input("Instance-id ('ixxxx': ")
            d=input("device-name(/dev/xvdf): ")
            if(d is None):
                d='/dev/xvdf'
            v=ec2.Volume(vol)
            response=v.attach_to_instance(InstanceId=instance,Device=d)
            print("Volume attached")

        elif(n==5):
            bucket=input("Bucket : ")
            f=input("FIle: ")
            obj=input("Object name: ")
            s3=session.client('s3')
            response=s3.Bucket(bucket).upload_file(f,obj)
            print("file uploaded")
        n=int(input("Enter choice (0 to quit): "))
def partitions():
    print("welcome to ")

if(__name__=='__main__'):
    import subprocess as sp
    import xml.etree.ElementTree as et
  
    print("WELCOME".center(60,'*'))
    print("menu is \n \
        1.date \n \
        2.cal \n \
        3.configure and start datanode \n \
        4.configure ,start namenode \n \
        5.start webserver \n\
        6.start and launch docker container\n\
        7.make partitions\n\
        8.working with aws")
    #=int(input("Enter which option you want: "))
    n1=input("Choose local or remote execution(l/r): ")

    dl={1:date,2:cal,3:dataname,4:dataname,5:webserver,6:docker,7:partitions,8:aws}
    if(n1=='r'):
        ip=input("Enter ip address of remote machine: ")
        x=sp.run('ssh '+ip+' python3 remote.py',shell=True)
        if(x.returncode):
            sp.getoutput('scp remote.py '+ip+':remote.py')
        x=sp.run('ssh '+ip+' python3 remote.py',shell=True)
    elif(n1=='l'):
        n=int(input("Enter which option you want: "))
        while(n):
            #=int(input("Enter which option you want"))
            result=dl[n]()
            n=int(input("Enter choice(0 to quit): "))

