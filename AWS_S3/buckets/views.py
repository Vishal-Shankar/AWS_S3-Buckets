from django.shortcuts import render
import boto3
from django.contrib import messages

# Create your views here.
def home(request):
    if request.method == 'POST':
        global aid,sak 
        aid=request.POST.get('aid')
        log=request.POST.get('log')
        sak=request.POST.get('sak')
        try:
            if log:
                if aid and sak:
                    s3=boto3.resource(
                        service_name='s3',
                        region_name='us-east-1',
                            aws_access_key_id = aid,
                        aws_secret_access_key = sak,)
                    for i in s3.buckets.all():
                        break 
                    return render(request,'buckets/home.html',{'s':True})
                else:
                    messages.error(request,'Please Enter Access Key Id and Secret Access Key')
                    return render(request,'buckets/home.html')
        except:
            messages.error(request,'Invalid Access Key Id and Secret Access Key')
            return render(request,'buckets/home.html')
    return render(request,'buckets/home.html')

def login(request):
    if request.method == 'POST':
        s3=boto3.resource(
                       service_name='s3',
                    region_name='us-east-1',
                        aws_access_key_id = aid,
                      aws_secret_access_key = sak,) 
        lb=request.POST.get('lb')
        if lb:
            return render(request,'buckets/login.html',{'lbs':[i for i in s3.buckets.all()]})   

    return render(request,'buckets/login.html')              

def create(request):
    if request.method == 'POST':

        s3=boto3.resource(
                       service_name='s3',
                    region_name='us-east-1',
                        aws_access_key_id = aid,
                      aws_secret_access_key = sak,) 
        n=request.POST.get('name')
        cr=request.POST.get('cr')

        if cr and n:
            if n not in [i.name for i in s3.buckets.all()]:
                try:
                    s3.create_bucket(Bucket=n)
                    messages.success(request,'Bucket successfully created')
                    return render(request,'buckets/create.html',{'lbs':[i for i in s3.buckets.all()]})
                except:
                    messages.error(request,'Invalid Bucket name please try a diffrent name')
                    return render(request,'buckets/create.html',{'lbs':[i for i in s3.buckets.all()]})
            else:
                messages.error(request,'Bucket aldready exist please try a diffrent name')
                return render(request,'buckets/create.html',{'lbs':[i for i in s3.buckets.all()]})
        else:
            messages.error(request,'Please Enter Bucket name')
            return render(request,'buckets/create.html',{'lbs':[i for i in s3.buckets.all()]})   
    
    return render(request,'buckets/create.html')  



def delete(request):
    if request.method == 'POST':

        s3=boto3.resource(
                       service_name='s3',
                    region_name='us-east-1',
                        aws_access_key_id = aid,
                      aws_secret_access_key = sak,) 
        
        n=request.POST.get('name')
        dl=request.POST.get('del')   
        
        if dl and n:
            if n in [i.name for i in s3.buckets.all()]:
                bck=s3.Bucket(n)
                bck.objects.all().delete()
                bck.delete()
                messages.success(request,f'{n} Deleted successfully click on List Buckets to verify')
                return render(request,'buckets/delete.html',{'lbs':[i for i in s3.buckets.all()]})
            else:
                messages.error(request,'Bucket does not exist please try a valid name')
                return render(request,'buckets/delete.html',{'lbs':[i for i in s3.buckets.all()]})
        else:
            messages.error(request,'Please Enter Bucket name')
            return render(request,'buckets/delete.html',{'lbs':[i for i in s3.buckets.all()]})
   
    return render(request,'buckets/delete.html')  

def copy(request):
    if request.method == 'POST':

        s3=boto3.resource(
                       service_name='s3',
                    region_name='us-east-1',
                        aws_access_key_id = aid,
                      aws_secret_access_key = sak,) 
        
        sbn=request.POST.get('sbname')
        sfn=request.POST.get('sfname')
        dbn=request.POST.get('dbname')
        dfn=request.POST.get('dfname')
        cf=request.POST.get('cf')   

        if cf:
            if sbn and sfn and dbn and dfn:
                nbm=[i.name for i in s3.buckets.all()]
                if sbn in nbm and dbn in nbm:
                    mys=s3.Bucket(sbn)
                    myd=s3.Bucket(dbn)
                    nsfm=[i.key for i in mys.objects.all()]
                    ndfm=[i.key for i in myd.objects.all()]
                    if sfn in nsfm and dfn in ndfm:
                        cs={
                            'Bucket':sbn,
                            'Key':sfn
                        }
                        buck = s3.Bucket(dbn)
                        buck.copy(cs,dfn)
                        messages.success(request,f'Copied content of {sbn}/{sfn} to {dbn}/{dfn} successfully')
                    else:
                        messages.error(request,'invalid source or destination file name please enter valid names')
                        return render(request,'buckets/copy.html')
                else:
                    messages.error(request,'invalid source or destination bucket name please enter valid names')
                    return render(request,'buckets/copy.html')
                                
            else:
                messages.error(request,'Please Enter all the * fields')
                return render(request,'buckets/copy.html')   
    return render(request,'buckets/copy.html') 


def move(request):
    if request.method == 'POST':

        s3=boto3.resource(
                       service_name='s3',
                    region_name='us-east-1',
                        aws_access_key_id = aid,
                      aws_secret_access_key = sak,) 
        
        sbn=request.POST.get('sbname')
        sfn=request.POST.get('sfname')
        dbn=request.POST.get('dbname')
        dfn=request.POST.get('dfname')
        mf=request.POST.get('mf')   

        if mf:
            if sbn and sfn and dbn:
                nbm=[i.name for i in s3.buckets.all()]
                if sbn in nbm and dbn in nbm:
                    myd=s3.Bucket(sbn)
                    nsfd=[i.key for i in myd.objects.all()]
                    if sfn in nsfd:
                        s3.Bucket(dbn).put_object(Key=sfn)
                        css={
                            'Bucket':sbn,
                            'Key':sfn
                        }
                        bck = s3.Bucket(dbn)
                        bck.copy(css,sfn)
                        s3.Object(sbn,sfn).delete()
                        messages.success(request,f'Moved {sfn} from {sbn} to {dbn} successfully',{'lfs'})
                    else:
                        messages.error(request,'invalid source or destination file name please enter valid names')
                        return render(request,'buckets/move.html')
                else:
                    messages.error(request,'invalid source or destination bucket name please enter valid names')
                    return render(request,'buckets/move.html')
                                
            else:
                messages.error(request,'Please Enter all the * fields')
                return render(request,'buckets/move.html') 

    return render(request,'buckets/move.html') 

def files(request,fn: str):
    if request.method == 'POST':

        s3=boto3.resource(
                       service_name='s3',
                    region_name='us-east-1',
                        aws_access_key_id = aid,
                      aws_secret_access_key = sak,) 
        lf=request.POST.get('lf')
        crf=request.POST.get('crf')
        f=request.POST.get('fname')
        df=request.POST.get('df')
        crfo=request.POST.get('crfo')
        dfo=request.POST.get('dfo')

        myb=s3.Bucket(fn)

        if lf:
            return render(request,'buckets/files.html',{'lfs':[i.key for i in myb.objects.all()]})

        if crf:
            if f:
                s3.Bucket(fn).put_object(Key=f)
                messages.success(request,f'{f} created successfully click on List Files/Folder to verify')
                return render(request,'buckets/files.html',{'lfs':[i.key for i in myb.objects.all()]})
            else:
                messages.error(request,'Please Enter File name')
                return render(request,'buckets/files.html',{'lfs':[i.key for i in myb.objects.all()]})


        if df:
            if f:
                mfb=s3.Bucket(fn)
                if f in [i.key for i in mfb.objects.all()]:
                    s3.Object(fn,f).delete()
                    messages.success(request,f'{f} deleted  successfully click on List Files/Folder to verify')
                    return render(request,'buckets/files.html',{'lfs':[i.key for i in myb.objects.all()]})
                else:
                    messages.error(request,'File does not exist please try a valid name')
                    return render(request,'buckets/files.html',{'lfs':[i.key for i in myb.objects.all()]})
            else:
                messages.error(request,'Please Enter File name')
                return render(request,'buckets/files.html',{'lfs':[i.key for i in myb.objects.all()]}) 

        if crfo:
            if f:
                f+='/'
                s3.Bucket(fn).put_object(Key=f)
                messages.success(request,f'{f} created successfully click on List Files/Folder to verify')           
                return render(request,'buckets/files.html',{'lfs':[i.key for i in myb.objects.all()]}) 
            else:
                messages.error(request,'Please Enter Folder name')
                return render(request,'buckets/files.html',{'lfs':[i.key for i in myb.objects.all()]}) 


        if dfo:
            if f:
                mfb=s3.Bucket(fn)
                f+='/'
                if fn in [i.key for i in mfb.objects.all()]:
                    s3.Object(fn,f).delete()
                    messages.success(request,f'{f} deleted  successfully click on List Files/Folder to verify')                
                    return render(request,'buckets/files.html',{'lfs':[i.key for i in myb.objects.all()]}) 
                else:
                    messages.error(request,'Folder does not exist please try a valid name')
                    return render(request,'buckets/files.html',{'lfs':[i.key for i in myb.objects.all()]}) 
            else:
                messages.error(request,'Please Enter Folder name')
                return render(request,'buckets/files.html',{'lfs':[i.key for i in myb.objects.all()]}) 

    return render(request,'buckets/files.html')

def upload(request,fn: str):
    if request.method == 'POST':

        s3=boto3.resource(
                       service_name='s3',
                    region_name='us-east-1',
                        aws_access_key_id = aid,
                      aws_secret_access_key = sak,) 

        uf=request.POST.get('uf')
        fp=request.POST.get('fp')

        myb=s3.Bucket(fn)

        if uf and fp:
            s3.Bucket(fn).put_object(Key=[fp.split('/')][-1][-1],Body=fp)
            fns=[fp.split('/')][-1][-1]
            messages.success(request,f'{fns} Uploaded successfully click on List Files to verify')
            return render(request,'buckets/upld.html',{'lfs':[i.key for i in myb.objects.all()]})
        else:
            messages.error(request,'Please choose the File')
            return render(request,'buckets/upld.html')
            
    return render(request,'buckets/upld.html')












        