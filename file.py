# -*- coding: utf-8 -*-
'''
امکانات:
    اصلاح نام فایل ورودی
        تبدیل فارسی به فینگلیش
        تبدیل کاراکترها به خط فاصله
    نشان دادن تاریخ فارسی برای فایلها
    نشان دادن  میزان قدیمی بودن فایل به دقیقه
'''
share_inf={ 'share':'اشتراک فایل',
            'paper\\pre':'محل پیش نویس نامه ها'}
import os,time
from jdatetime import datetime
import k_file
import k_finglish
import k_err

import share_value as share
xpath=share.xpath()
def _folder_w_access(args=request.args):
    """
        folder_w_access=folder_write_access
    """
    #args=request.args or ['share']
    path='\\'.join(args)
    if path in share_inf or session["admin"]:
        return {'ok':True} #x_title 
    else:
        return {'ok':False,'msg':f'you can not do this action-path={path}'} #False,'error'        
def _access_denied():
    link=URL('user','login')
    r1='''
        <div align="center">
        <h1>شما اجازه دسترسی به این صفحه را ندارید- باید اول وارد سیستم شوید</h1>
        <BR><a href='javascript:void(0)' onclick="j_box_show('{}',true)"><h3> ورود به سیستم </h3></a>
        </div>
    '''.format(link)
    return dict(x=XML(r1))
def _login_check():
    if not session["username"]: 
        return _access_denied()    #redirect(URL('_access_denied'))
def _ftime(x):
    return datetime.utcfromtimestamp(x).strftime("%Y/%m/%d - %H:%M:%S")#%a, %b
def _dif_time(x):
    import time
    now = time.time()
    d = now-x 
    mm = int(d / 60) #minutes
    h,m=divmod(mm,60)
    d,h=divmod(h,24)
    st=f'{d:03d} D, {h:02d} H,{m:02d} M'
    isi=f'{d: 3d} D' if d else f'{h: 2d} H' if h else f'{m: 2d} M' #isi=asan
    return {'m':mm,'st':st,'isi':isi}
def _list_files(path,full_name=False):
    #path=file full_path(path/name.ext) 
    showall =True if request.vars.showall else False
    files,folders=[],[]
    if not os.path.exists(path):
        return files,folders
    for item in os.listdir(path):
        if not showall and item[:2]=='__':continue
        pp=os.path.join(path, item)
        if os.path.isfile(pp):
            #if not os.path.getsize(pp):break:#omit zero size file
            if full_name:
                files+= [pp]
            else:
                ff=k_file.file_name_split(item)
                files+= [{'name':ff['name'],'size':k_file.size_easy(os.path.getsize(pp)),
                          'fname':k_finglish.fin_to_fa(ff['name']),'ext':ff['ext'],'filename':ff['filename'],
                        'mtime':_ftime(os.path.getmtime(pp)),'ctime':_ftime(os.path.getctime(pp))
                        ,'m_dif_time':_dif_time(os.path.getmtime(pp))
                        }]
        else:
            folders+=[{'name':item,'fname':k_finglish.fin_to_fa(item)}]
    return files,folders
def _list_files_meta_read(path,files,folders):#_txt
    import json
    '''
        f_path=file path
        get meta data for files & Folders form '__inf.json' in txt format
    '''
    for f in files+folders:
        for t in ['title','x']:
            f[t]=''
    f_path=os.path.join(path,'__inf.json')
    if os.path.isfile(f_path):
        meta=k_file.read('json',f_path)
        #=
        '''
        meta={'files':{ '0-4901.pdf':{'title':'abc',
                        'x':'y'},
            '1-rec-i-4901.pdf':{'title':'qwererwe',
                                'x':'z'}
        },
        'general':'abc'
        }
        '''
        for f in files:
            if f['filename'] in meta['files']:
                f.update(meta['files'][f['filename']])
        #print("###"+ str(meta['folders']))
        for f in folders:
            #print(f)
            if f['name'] in meta['folders']:
                #print(f+' is in' )
                f.update(meta['folders'][f['name']])
        for f in files+folders:
            f['title']=k_finglish.fin_to_fa(f['title'])
        return meta['general']
    else:
        return ""
#-----------------------------------------------------------------
def _list_files_meta_append(path,append_dic):#_txt
    import json
    '''
        add or change file titels in '__inf.json' in txt format
    inputs
    ------
        f_path=file path
        append_dic=dict 
            {file_name1:file_title1,...}
    '''
    def _append_dic(base_dic,add_dic):
        for x in add_dic:
            if (x in base_dic) and type(base_dic[x])==dict :
                    if type(add_dic[x])==dict:
                        _append_dic(base_dic[x],add_dic[x])
                    else: 
                        return False,'error change dict => none dict'
            else: #add or change
                base_dic[x]=add_dic[x]
        return True,'ok'
    f_path=os.path.join(path,'__inf.json')
    try:
        if os.path.isfile(f_path): # if file exist 
            meta=k_file.read('json',f_path)
            _append_dic(meta,append_dic)
            k_file.write('json',f_path,meta)
            return (str(meta)+'<br>append ok<br> '+f_path)
        else: # creat file
            meta={ "files": {},
                   "folders": {},
                   "general": "abc"}
            ok,msg=_append_dic(meta,append_dic)
            if ok:
                k_file.write('json',f_path,meta)       
                return (str(meta)+'<br>creat ok<br> '+f_path)
            else:
                return msg
    except:
        return ('error in <br> _list_files_meta_append <br> '+f_path)
#-----------------------------------------------------------------  
def _list_files_meta_change_key(path,old_key_in_dict,new_key):#_txt
    import json
    '''
        exam
        abc.inf={'file':{'a':'a'},'folder':{'x':'x_t'}    }
        _list_files_meta_change_key('abc.inf',{'folder':{'x':'x_t'},'y')
        result=
        abc.inf={'file':{'a':'a'},'folder':{'y':'x_t'}    }
    inputs:
    ------
        f_path=file path
        old_key_in_dict=dict
        new_key:str
            new nemae for last key in old_key_in_dict in this exam ='x'
    '''
    def change_dic_key(base_dic,old_key_in_dict,new_key):
        for x in old_key_in_dict:
            if (x in base_dic):
                if type(old_key_in_dict[x])==dict: #if type(base_dic[x])==dict :
                    return change_dic_key(base_dic[x],old_key_in_dict[x],new_key)
                else :
                    base_dic[new_key]=base_dic[x]
                    del base_dic[x]
                    return True,'ok'
            else: 
                return False,'error change dict => none dict'                
    #----------------------------------------------------------    
    f_path=os.path.join(path,'__inf.json')
    #try:
    if os.path.isfile(f_path):
        meta=k_file.read('json',f_path)
        ok,msg=change_dic_key(meta,old_key_in_dict,new_key)
        if ok:
            k_file.write('json',f_path,meta)
            return (str(meta)+'<br>change_key ok<br> '+f_path)
        else:
            return msg
    #except:
    #    return ('error in <br> _list_files_meta_change_key <br> '+f_path)
#-----------------------------------------------------------------      
def upload_file():
    fwa=_folder_w_access()
    if not fwa['ok']:return fwa['msg']
    
    file=request.vars.filepicker
    
    filename1=request.vars.filename
    ff=k_file.file_name_split(file.filename)#.replace(" ", "")
    xdata={    
        'user_filename':k_file.name_correct(ff['name']),
        'un':session["username"]}
    filename=filename1.format(**xdata) or xdata['user_filename']
    filename+=ff['ext']
    file_b=file.file.read() #file contents in byte format
    #ou=str(file.file.read())
    
    #ou+=str(file.filename)
    #ou+='<br>'+ str(file_b)
    
    if filename:
        session['uploaded_name']=filename
        path=xpath+'\\'.join((*request.args,filename))
        session['uploaded_path']=path
        session['uploaded_time']=time.time() #now
        response.flash=T("File Upload started!")
        with open(path, 'wb') as f:f.write(file_b)
        msgs=['File Upload Succesfully',f'filename={path}',f'args={request.args}']
        print("/n".join(msgs))
        if request.vars.todo :
            sq=request.vars.todo.split(';') 
            msgs+=['todo ='+ str(sq)]
            if sq[0]=='sql':
                print('xxx')
                from k_sql import DB1
                db_path='applications\\ksw\\databases\\'
                db_p=db_path+sq[1]+'.db'
                if os.path.isfile(db_p):
                    msgs+=['todo file is found =>'+ db_p]   
                    db1=DB1(db_p)
                    xu=db1.update_data(table_name=sq[2],set_dic={sq[4]:filename},where_dic={'id':sq[3]}) #tb_name=sq[1]
                    msgs+=['update db is done =>'+ str(xu)]
        return "<br><h2>فایل با موفقیت آپلود شد</h2><hr>"+'<br>'.join(msgs)
    else:
        return f'File Not Found <br> filename={path}'
    
def mdir():
    args=request.args
    if args:
        path=xpath+'\\'.join(args)
        print(f'mdir:{path}')
        return k_file.dir_make(path)
def upload():
    """ 010825
        input by request.vars
            filepicker (auto by <input tyep='file' id,name='filepicker'>
            file_ext
            filename
            todo    = action that do after file upload
                sql;<db_name;<table_name>;<id>;<field_name>
    """
    fwa=_folder_w_access()
    if not fwa['ok']:return fwa['msg']
    
    args=request.args
    file_ext=request.vars.file_ext #"jpg,gif" #"gif,jpg,jpeg,png,doc,docx"
    #if type(file_ext)!=list:file_ext=[]
    file_ext_list=file_ext.split(",")
    file_ext_tit=','.join([f' {x} ' for x in file_ext_list])
    file_ext_li=','.join([f'"{x}"' for x in file_ext_list])
    file_ext_dot=','.join([f'.{x}' for x in file_ext_list])  #".gif,.jpg,.jpeg,.png,.doc,.docx"
    link=XML(URL(f='upload_file',args=args,vars=request.vars))#upload_file # action='j_box_show("{}");'
    return dict( link=link,
                args=str(args)+"<br>"+str(request.vars),
                file_ext_tit=file_ext_tit,
                file_ext_list=XML(file_ext_li),
                file_ext_dot=file_ext_dot )
def download():#ownload
    #return response.download(request,db,download_filename=xpath+'per.xlsx')
    args=request.args
    if args:
        path=xpath+'\\'.join(args)
        if not os.path.exists(path):return f'file not exist => {path}'
        #fn=args[0] if len(args)>0 else 'per.xlsx'
        #path=xpath+fn
        return response.stream(open(path,'rb'),chunk_size=4096)
def unzip():
    args=request.args
    if args:
        path=xpath+'\\'.join(args)
        ok=k_file.zip_extract(path)
        if ok: return (f'<br> unzip done successfully <br> {path} <hr>')
    return (f'Error in unzip\n{path}')
def zip():
    args=request.args
    if args:
        folder=xpath+'\\'.join(args)
        r_file=folder+'.zip' #xpath+'\\'.join(args[:-1]+[''])
        msg=k_file.zip_folder_to(folder,r_file)
        return (msg)        
def delete():
    fwa=_folder_w_access(args=request.args[:-1])
    if not fwa['ok']:return fwa['msg']

    args=request.args
    if args:
        xp=os.path.join(xpath,*args)
        k_file.file_delete_rcl(xp)
        from k_set import K_set
        return (f"""<br><h2>فایل با موفقیت پاک شد</h2><hr>
                    <br> Delete  Done Successfully <br> move to recycle:<br>===>   {K_set.recycle})<br>fome:<br><=== {xp}<br> <hr>""")
    return 'error : args is empty'
def name_correct():
    args=request.args
    if args:
        xp=os.path.join(xpath,*args[:-1])
        n1=args[-1]
        n2=k_file.name_correct(n1)
        re1=k_file.file_move((xp,n1),(xp,n2))
        return '{3} : {0}\\{1}<br>    {0}\\{2}<br>'.format(xp,n1,n2,re1) 
def correct_files_name_in_folder():
    args=request.args
    if args:
        xp=os.path.join(xpath,*args)
        re1=k_file.correct_files_name_in_folder(xp)
        return XML('<hr>'.join(['-'*20 + x +'<br>'.join(['']+re1[x]) for x in re1]))
def manage():
    args=request.args
    path=os.path.join(xpath,*args)
    files,folders=_list_files(path)
    #print(str(f_list))
    return dict(a=A('upload new file',_href=URL(f='upload',args=args,vars=request.vars)),
    files=TABLE(*[TR(A(x['name'],_href=URL(f='download',args=args+[x['name']])),x['size'],x['mtime'],x['ctime']) for x in files],_class='table2'),
    folders=TABLE(*[A(x,_href=URL(args=args+[x])) for x in folders],_class='table2'))
def f_list_sd():    #sd=sade
    return f_list()
def f_list():#file_browser=file.index
    r1=False #_login_check()
    if r1:return dict(address='',m_dir='',upload='',path='',a='',files=XML(r1),folders='',js='')
    '''
    use:
    ----------
        url?del=1
    '''
    import re
    args=request.args
    path=xpath+'\\'.join(args)
    x_path=";"+path.lower().replace("\\",";")+";"
    #file_change_access-----------------------------
    def fca(x_path):
        '''
        بررسی امکان تغییر یک فلدر توسط یک نفر
        input
        ------
            session["file_access"]=> set by user.py on login
            session["my_folder"]=> set by user.py on login
                سسشن های فایل_اکسس و مای_فلدر در داخل برنامه یوزر.پای در زمان لاگین کردن فرد تنظیم می شود
                
        '''
        def list_match(pt_list,st):
            for pt in pt_list:
                if re.findall(pt,st):
                    return True
        #------------------------    
        
        fc_list=(session["file_access"].split(",") if type(session["file_access"])==str else [])+[f';{session["my_folder"]};']
        print(str(fc_list))
        return True if session["admin"] or (list_match(fc_list,x_path)) else False #file_change_access: user have file_change_access for this folder
    fc_access=fca(x_path)
    print('curren user file_change_access='+ str(fc_access)+ '  | on floder ='+x_path)
    #print(f'f_list : file_access -{fc_access}-{session["file_access"]}-{x_path}')
    
    #add_folder_access
    def m_dir(x_path):
        def afa():
            x_match=r";prj;\w*;\w*;\B"
            if re.findall(x_match,x_path):
                path=xpath+'\\'.join(args+[session["my_folder"]])
                if not os.path.exists(path):
                    return True
        #------------------------------------        
        #   re1 = True if session["admin"] or (re.findall(x_match,x_path)) else False
        #    print(f'f_list : add-folder -{re1}-{x_match}-{x_path}')
        #    return re1
        if afa():
            link1=XML(URL(f='mdir',args=request.args+[session["my_folder"]],vars=request.vars))
            return XML('''<a  href = 'javascript:void(0)' onclick='j_box_show("{}",true);' title='{} ساخت پوشه تحت مدیریت من با نام :'   > + MY Folder </a>'''.format(link1,session["my_folder"]))
        return ''
    #--------------------------------------------    
    
    files,folders=_list_files(path)
    meta=_list_files_meta_read(path,files,folders)
    #print(str(f_list))
    def link_unzip(fname):
        f=k_file.file_name_split(fname)
        return A('unzip',_href=URL(f='unzip',args=args+[fname],vars=request.vars),_target="x_frame") if f['ext'] in ['.zip'] and fc_access else ''
    def link_delete(fname):
        return A('Del',_href='javascript:void(0)',_onclick=f"j_box_show('{URL(f='delete',args=args+[fname],vars=request.vars)}',true)") if fc_access and request.vars['del'] else '' #_target="x_frame"
    def link_rename(fname):
        return A('Ren',_href=URL(f='name_correct',args=args+[fname],vars=request.vars),_target="x_frame") if fc_access and request.vars['ren'] else ''     
    def link_ren2(fname):
        return A('Ren-*',_href=URL(f='correct_files_name_in_folder',args=args+[fname],vars=request.vars),_target="x_frame") if fc_access and request.vars['ren'] else ''     
    def link_rename_title(case,f_name,f_title):
        if not f_title:f_title='-'
        vars={'f_name':f_name,'f_title':f_title,'case':case}
        vars.update(dict(request.vars))
        return A(f_title,_href=URL(f='file_meta_edit',args=args,vars=vars),_target="x_frame") if fc_access else f_title 
        return A(f_title,_href=URL(f='file_meta_edit',args=args,vars={'f_name':f_name,'f_title':f_title,'case':case}.update(dict(request.vars))),_target="x_frame") if fc_access else f_title 
    def link_view(x):
        xd={'json':'json_read','csv':'read_csv','md':'read_m','mm':'read_m','ksm':'read_m'}
        ext=x['ext'][1:]
        r1=[]
        if ext in xd:
            r1+=[ A('v',_href=URL('xfile',xd[ext],args=args+[x['filename']],vars=request.vars),_target="x_frame",_title='View')]
        if fc_access:
            r1+=[ ' | ',
                    #XML(f'''<button onclick="copyToClipboard('{x['filename']}')">Copy</button>''')]
                    #XML(f'''<button onclick="$('#input_adr').val('{os.path.join(*args,x['filename'])}');alert('ok')">Copy</button>''')]
                    A('T',_href=URL('xfile','tools',args=args+[x['filename']],vars=request.vars),_target="x_frame",_title='Tools')]
            if ext in ['md','mm','json','csv','txt']:
                r1+=[ ' | ',
                    A('e',_href=URL('xfile','edit_r',args=args+[x['filename']],vars=request.vars),_target="x_frame",_title='Edit')]
   
        return DIV(*r1)    
    #def list(path):
    copyclip_func='''<script>
                          function copyToClipboard(copyText) {
                             navigator.clipboard.writeText(copyText).then(() => {
                                // Alert the user that the action took place.
                                alert("Copied to clipboard");
                            });
                          }
                        </script> '''   
    copyclip_func='''<script>var $temp = $("<input>");
            $("body").append($temp);
            $temp.val($(element).text()).select();
            document.execCommand("copy");
            $temp.remove();
            </script>'''                        
    xp=XML(path.replace('/','\\'))
    filepath=f'''
    <button id="copy">Copy</button>
    <input id="input_adr" type="text" value="{xp}" style="width:80%" />
    <script>
        function copy() {{
            var copyText = document.querySelector("#input_adr");
            copyText.select();
            document.execCommand("copy");
        }}
        document.querySelector("#copy").addEventListener("click", copy);
    </script>
    '''
    xx1=f'<div onclick="navigator.clipboard.writeText(\'{xp}\');alert(\'ok\')">{xp}</div>'
    def address(name,args,titel=''):
        return DIV(' \\ ',A(name,_href=URL(args=args,vars=request.vars),_style='background-color:#ffddcc;margin:0px 10px 0px 10px;padding:0px 10px 0px 10px'),_style='float:left; ',_title=titel)
    def x_class(ext): 
        '''
           در جدول به ردیف هر نوع از فایلها یک کلاس اختصاص می دهد تا بتوان با سی.اس.اس گرافیک آنرا تنظیم کرد
            تنظیمات گرافیک در فایل زیر می باشد
            ks.css 
        '''
        xx={'folder':['older'],
            'pic':['jpg','png'],
            'pdf':['pdf'],
            'txt':['txt'],
            'zip':['zip'],
            'ml':['md','mm','ksl']
            }
        #  
        for x in xx:
            if ext[1:].lower() in xx[x]:
                t=x
                break
        else:
            t='general'
        return 'file_'+ t
    def x_upload():
        link1=XML(URL(f='upload',args=request.args,vars={**request.vars,'filename':'','file_ext':""}))
        return XML('''<a  href = 'javascript:void(0)' onclick='j_box_show("{}",true);' title='بارگزاری فایل'> +File </a>'''.format(link1) if fc_access else '')

    return dict(js=XML(copyclip_func),
    m_dir=m_dir(x_path),upload=x_upload(),
    path=(XML(filepath)  if session["admin"] else ''),
    #a=DIV(*[DIV(' \\ ',A(args.get(i),_href=URL(args=args[:(i+1)]),_style='background-color:#ddddff'),_style='float:left') for i in range(-1, len(args))],DIV(' : ')) ,
    address=DIV(address('..',[]),*[address(args[i],args[:i+1],k_finglish.fin_to_fa(args[i])) for i in range(len(args))]," : ") ,
    files=TABLE(THEAD(TR(*[TH(x) for x in ['n','Title','Name','E_1','E_2','Size','Date','-','-','-']])),
                TBODY(  *[TR((i+1),
                            link_rename_title('folders',x['name'],x['title']),
                            A(f"<{x['name']}>",_href=URL(args=args+[x['name']],vars=request.vars),_title=x['fname']),
                            '<>',
                            'folder',
                            link_rename(x['name']),
                            link_ren2(x['name']),
                            '',
                            '',
                            '',
                            _class=x_class('folder')
                            ) for i,x in enumerate(folders)],
                        *[TR((i+1),
                            link_rename_title('files',x['filename'],x['title']),
                            A(x['name'],_href=URL(f='download',args=args+[x['filename']],vars=request.vars),_target="x_frame",_title=x['fname']+'\n'+x['ext']),
                            x['ext'][1:],
                            link_view(x),
                            x['size'],
                            x['mtime'],
                            link_unzip(x['filename']),
                            link_delete(x['filename']),
                            link_rename(x['filename']),
                            _class=x_class(x['ext'])
                            ) for i,x in enumerate(files)],
                     ),
        _class='table_file'),
    folders=TABLE(THEAD(TR(*[TH(x) for x in ['n','Folder Name','-','-']])),
                  TBODY(*[TR((i+1),
                        A(x['name'],_href=URL(args=args+[x['name']],vars=request.vars),_title=x['fname']),
                        link_rename(x['name']),
                        link_ren2(x['name'])
                        ) for i,x in enumerate(folders)]),
        _class='table_file'),
    frame=XML('<iframe id="f_frame" name="f_frame" src="" height="1000" width="1740" title="file previw"></iframe>')
    )
def socket_x():
    from gluon.contrib.websocket_messaging import websocket_send
    websocket_send('http://127.0.0.1:8888', 'Hello World', 'mykey', 'mygroup')
    return 'ok'
"""
index temp    
    $('#wait').ajaxStart(function() {{
                $(#wait).show();
                $(#file_form).hide();
            }}).ajaxComplete(function() {{
                $(#wait).hide();
                $(#file_form).show();
    --------------------------------------
    ajaxStart(function() {{
                $('#wait').show();
                $('#file_form').hide();
            }}).ajaxComplete(function() {{
                $('#wait').hide();
                $('#file_form').show();
            }});
            $('#x_frame').attr("src", "{1}");
                r"http:/10.36.1.200:8000"+
    ------------------------------------
        <div name="wait" id="wait">Please wait</div>
        <script>
            function loadIframe(iframeName, url) {{
                var $iframe = $('#' + iframeName);
                if ( $iframe.length ) {{
                    $iframe.attr('src',url);    // here you can change src
                    return "A";
                }}
                document.getElementById(iframeName).src=url;
               
                //$iframe.attr('src',url)
                return "2";
            }}
            
            $('#wait').hide();
            alert("{1}");
            //alert(loadIframe("x_frame", "{1}"));
            $('#file_form').submit(function( event ) {{
                loadIframe("x_frame", "{1}")
                return;
            }});    
        </script>  
    .format(link,URL(f="wait"))),        
----------------------
    link=XML(URL(f='upload_file',args=['share']))#upload_file    
    upload=XML('''
        <form name="file_form" id="file_form" method="post" enctype="multipart/form-data" action="{0}" target="x_frame">
             <input name="file" type="file" size="60">
             <input type="Submit" value="Upload">
        </form> 
    '''.format(link)),
    
"""    
def index1():
    '''
    share folder
    '''
    args=['share']
    path=xpath+'\\'.join(args)
    files,folders=_list_files(path)
    def myFunc(file):
        return file['mtime']
    files.sort(reverse=True,key=myFunc)
    def link_delete(fname):
        return A('Del',_href=URL(f='delete',args=['share',fname],vars=request.vars),_target="x_frame") #if request.vars['del'] else ''
    link=XML(URL(f='upload_file',args=['share'],vars=request.vars))#upload_file
    #<input name="file" type="file" size="60" maxlength="10000000">

    return dict(
    x_farme=1,
    upload=XML('''
        <form name="file_form" id="file_form" method="post" enctype="multipart/form-data" action="{0}" target="x_frame">
             <input name="file" type="file" size="60">
             <input type="Submit" value="Upload">
        </form> 
    '''.format(link)),
    files=TABLE(THEAD(TR(*[TH(x) for x in ['n','Name','Size','Date','Age','-']])),
                TBODY(*[TR((i+1),
                    A(x['filename'],_href=URL(f='download',args=args+[x['filename']],vars=request.vars),_target="x_frame",_title=x['fname']),
                    x['size'],x['mtime'],x['m_dif_time']['isi'],link_delete(x['filename'])
                        ) for i,x in enumerate(files)]),
                _class='table2'),
    )
  
def index():
    #r1=_login_check()
    '''
        share folder
    '''
    args=request.args or ['share']
    fwa=_folder_w_access(args)
    if not fwa['ok']:return fwa['msg']
    
    path='\\'.join(args)
    x_title=share_inf[path]
    path=xpath+path
    files,folders=_list_files(path)
    def myFunc(file):
        return file['mtime']
    files.sort(reverse=True,key=myFunc)
    j_box_txt='''<div ><a  href = 'javascript:void(0)' title='{2}' onclick='j_box_show("{0}",true);'> {1}</a></div>'''
    def link_delete(fname):
        # return A('Del',_href=URL(f='delete',args=['share',fname]),_target="x_frame") #if request.vars['del'] else ''
        return XML(j_box_txt.format(URL(f='delete',args=[*args,fname],vars=request.vars),'X','Delete file')) #A('Del',_href='javascript:void(0)',_onclick=f"""j_box_show("{URL(f='delete',args=['share',fname])}",true)""") #_target="x_frame"
    link1=XML(URL(f='upload',args=args,vars={**request.vars,'filename':'{un}-{user_filename}','file_ext':"gif,jpg,jpeg,png,doc,docx,xls,xlsx,pdf,dwg,zip,rar,ppt,pptx"}))
    #<input name="file" type="file" size="60" maxlength="10000000">
    return dict(
    x_title=x_title,
    x_farme=1,
    upload1=XML(j_box_txt.format(link1,'+ File','Uload File (بارگزاری فایل)')),
    
    files=TABLE(THEAD(TR(*[TH(x) for x in ['n','Name','Size','Date','Age','-']])),
                TBODY(*[TR((i+1),
                    A(x['filename'],_href=URL(f='download',args=args+[x['filename']],vars=request.vars),_target="x_frame",_title=x['fname']),
                    x['size'],x['mtime'],x['m_dif_time']['isi'],link_delete(x['filename'])
                        ) for i,x in enumerate(files)]),
                _class='table2'),
    )    
def file_meta_edit():
    def file_meta_save(f_name,f_title):
        if f_name and f_title:
            append_dic={request.vars['case']:{f_name:{'title':k_finglish.fa_to_fin(f_title)}}}
            return (_list_files_meta_append(xpath+'\\'.join(request.args),append_dic))  
        return 'save not done'
    def file_meta_change(f_name1,fname2):
        x_dic={request.vars['case']:{f_name1:''}}
        return (_list_files_meta_change_key(xpath+'\\'.join(request.args),
            old_key_in_dict=x_dic,new_key=fname2))  
    #------------------------------URL('file_meta_save',args=args,vars=request.vars)
    k_err.xxprint_reset_html()
    args=request.args
    path=xpath+'\\'.join(args)
    vars=request.vars
    f_name=vars['f_name']
    f_title=vars['f_title']
    ou=''
    if vars['f_title2'] and vars['f_title'] !=vars['f_title2']:
        ou+=file_meta_save(f_name,vars['f_title2'])
    if vars['f_name2'] and vars['f_name'] !=vars['f_name2']:
        import os
        f1=os.path.join(path, vars['f_name'])
        f2=os.path.join(path, vars['f_name2'])
        print(xpath)
        print(f1)
        print(f2)
        os.rename(f1,f2)
        ou+=file_meta_change(vars['f_name'],vars['f_name2'])
    if ou:return ou 
    #else
    f_n =INPUT(_name='f_name2',_id='f_name2',_value=vars['f_name2'] or vars['f_name'])
    f_t =INPUT(_name='f_title2',_id='f_title2',_value=vars['f_title2'] or vars['f_title'])
    return XML(FORM(DIV(f_n,f_t),INPUT(_type='submit'), _action='', _method='post'))

def file_meta_edit1():
    def file_meta_save(f_name,set_dict):
        args=request.args
        path=xpath+'\\'.join(args)
        if f_name:
            append_dic={request.vars['case']:{f_name:{'title':k_finglish.fa_to_fin(f_title)}}}
            #return (str(append_dic))
            return (_list_files_meta_append(path,append_dic))  
        return 'save not done'
    #------------------------------URL('file_meta_save',args=args,vars=request.vars)
    args=request.args
    rr=['name','title','title2','title_fa']
    #dict(request.vars)
    #rr.pop('case')
    path=xpath+'\\'.join(args)
    f_name=request.vars['f_name']
    f_title=request.vars['f_title']
    for x in rr:
        if request.vars[x+'2'] and request.vars[x] !=request.vars[x+'2']:
            return file_meta_save(f_name,rr)
    else: 
        xx=[INPUT(_name=x+'2',_id=x+'2',_value=request.vars[x+'2'] or request.vars[x]) for x in rr]
        return XML(FORM(DIV(*xx),INPUT(_type='submit'), _action='', _method='post'))

def wait():
    return "please wait"
def test():
    return dict(x=response.toolbar())

from gluon.tools import Expose
def test_myfolder():
    return dict(files=Expose('d:'))
#test    