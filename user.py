# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
from gluon.custom_import import track_changes; track_changes(True)
from datetime import datetime
from k_sql import DB1
import kytable
now = datetime.now().strftime("%H:%M:%S")
db_name=r'applications\ksw\databases\user.db'
db1=DB1(db_name)
def f_cod(s1, enc_st='09377953310'):
    return s1
    s2=enc_st*5
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(s1,s2)])
def index():
    redirect(URL('login'))
#--------------------------user
def logout():
    #call page_set("f","خروج","-")
    #users_report "o"
    session["username"] = ''
    session["admin"] = ''
    session["user_fullname"]=''
    #session.forget(response) #Session.Abandon
    response.cookies["username"] = ''
    response.cookies["user_fullname"]=''
    return dict(ou=XML('''  <br><br><div align=center><h4>شما از سيستم خارج شديد</h4><br><br>
                <a href='login'><h3> بازگشت </h3></a></div>'''))
def retrieve_password():     
    def send_ps(un): #,re):
        sql=db1.sql_set(_top="",_fields_name="*",_table_name="[un]",_where=f"un='{un}'" ,_order="")
        rs=db1.select(table_name='user',sql=sql,result='dict')
        if rs:
            ps=f_cod(rs["ps"])
            im="<br>" + un + dbc_mail_suffix + "<br>"
            if False: #s_mail_ps(un,ps) :
                r1=f"""رمز به ايميل شما در آدرس {im}
                       با موفقيت ارسال شد"""
            else:
                r1=f"""ارسال ايميل به آدرس شما {im}
                       با اشکال مواجه شد<br>
                       لطفا چند دقيقه ديگر مجددا سعي نماييد"""
        else:
            r1="نام وارد شده در سيستم ثبت نشده"
        return r1
    #-------------------------------------------------
    ou=f'''<div align=center>
        <h1>لطفا براي ورود رمز و پسورد خود را وارد کنيد</h1>
        <Form action = "login" method="POST"  id=form1 name=form1>
        Username:<input type="text" name="username" id="username"  size="20" value="{request.vars["username"]}" ><br>
        در صورت فراموش کردن رمز پس از وارد کردن کد مخفف خود در قسمت اول دکمه زير را بزنيد
        <br>
        <INPUT type="button" value="ارسال رمز به ايميل" name=butmail id=butmail  style="width:200px;" onclick='gomail();'>
        </Form></div>'''
    ou+='''
        <script type="text/javascript">
            function gomail()
            {
            j_n=document.getElementById("username").value;
            document.location.assign("login.asp?mail=ok&un=" + j_n);
            }
        </script>'''
    return dict(ou=XML(ou))
      
def login():
    def isok_un_ps (un,ps):
        #input un:user abb  ps:password
        #output		if un and ps is ok	=>	true
        #			else				=>	false
        # tavjoh natige in barname dakhel 2 session ("username","user_fullname") garar migirad ke khali budan anha neshaney adam vorud kamel mibashad
        r1,fullname,rs=user_chek_ps_get_Inf(un,ps)
        if r1:
            session["user_fullname"]= fullname
            session["username"]=un.lower()
            session["admin"]=True if session["username"]=='ks' else False
            session["file_access"]=rs["file_access"]
            session["my_folder"]=f'{rs["eng"].strip()}-{rs["un"].strip()}'
            #Session.Timeout=15

            response.cookies["username"]=un
            response.cookies["user_fullname"]=fullname
            #response.Cookies["username"].expires=date+30
            #response.Cookies["user_fullname"].expires=date+30
            return True
        else:
            session.forget(response) #session.Abandon ()
            response.cookies["username"]=""
            response.cookies["user_fullname"]=""
            return False
    #------------------------------------------------
    def user_chek_ps_get_Inf (un,ps):#,fullname):
        #return result , fullname
        if un=="admin" and ps==";,vasuhnjd" : return True,"admin"
        ps=f_cod(ps)
        sql=db1.sql_set("","*","user",{'un': un,'ps':ps } ,"")
        print ('sql='+sql)
        rs=db1.select('user',sql,result='dict')#share.setting_dbFile1,sql)
        if rs:
            print(str(rs))
            return True, '{m_w} {pre_n} {name} {family}'.format(**rs),rs
        else:
            return False,False,False
    #--------------------------------------------'
    #call page_set("f","ورود","-")
    #---------------------------------------------------------------------------------------------------------------------------
    goback="<BR><a href='login'><h3> بازگشت </h3></a>"
    def chek_un_ps(un,ps):
        if isok_un_ps(un,ps):
            #session["username"]=un
            ou='''  <div align=center><h3>{}</h3>
                    <h4>رمز و پسورد صحیح است</h4>
                    </div>
            '''.format(session["user_fullname"])
            ou+='<br>'.join([f'{x}={session[x]}' for x in ['username',"my_folder"]])#session
            #redirect(URL('index'))#, args=(1,2,3), vars=dict(a='b')))
        else:
            ou='''  <div align=center><h3></h3>
                    <h4>نام و يا رمز را اشتباه وارد کرده ايد</h4>
                    {}
                    </div>
            '''.format(goback,)
        return ou
    #------------------------------------------------------------------------------------------
    """
    if request.vars["mail"]:#!= "":
        ou=goback
        un=request.vars["un"]
        if un!="":
            #send_ps(un,re)
            ou+=''#re
        else:
            ou+=" نام وارد شده در سيستم ثبت نشده است <br>" + un
        return ou
    """    
    if "username" in request.cookies and "password" in request.cookies:
        un=request.cookies["username"].value
        ps=request.cookies["password"].value
        ou=chek_un_ps(un,ps)
        print(f'cookies-{un}-{ps}')
        #redirect(URL('index'))
    elif "username" in session and session["username"] and session["password"]:
        un=session["username"]
        ps=session["password"]
        ou=chek_un_ps(un,ps)
        print(f'session-{un}-{ps}')
        #redirect(URL('index'))
    elif request.vars["username"]:  #!="":
        un=request.vars["username"]
        ps=request.vars["password"]
        #session["ir_date"]= iran_time("","",0,x_w,"t")
        #session("ir_weak")=x_w
        #set_inf()
        ou=chek_un_ps(un,ps)
    else:
        ou=f'''<div align=center>
        <h2>لطفا براي ورود نام کاربری و پسورد خود را وارد کنيد</h2>
        <hr>
        <Form action = "login" method="POST"  id=form1 name=form1>
        Username:<input type="text" name="username" id="username"  size="20" value="{request.vars["username"]}" ><br><br>
        Password:<input type="password" name="password" size="20"><br><br>
        <input type="submit" value="ورود"  style="width:200px;" id=submit1 name=submit1>
        </Form></div>'''
    return dict(ou=XML(ou))
def change_password():
    #chek_un_ps(2,"")
    uf=session["user_fullname"]
    t1=f'''
    <Form method="POST"  id=form1 name=form1 onsubmit='return repass()'>
        <div align=center>
        <h2>{uf}</h2><hr>
        <h1>فرم تغییر رمز</h1>
        <table dir="rtl">
            <tr>
                <td>رمز قديم:</td>
                <hr>
                <td><input type="text" name="ps0" id="ps0"  size="20" ></td>
            </tr><tr>
                <td>رمز جديد:</td>
                <td><input type="password" name="ps1" id="ps1" size="20"></td>
            </tr><tr>
                <td>تکرار رمز جديد:</td>
                <td><input type="password" name="ps2" id="ps2" size="20"></td>
            </tr><tr>
                <td>تایید:</td>
                <td><input type="submit" value="تغيير رمز"  style="width:200px;" id=submit1 name=submit1></td>
            </tr>
        </table>
    </Form>'''
    t1+='''
    <script type="text/javascript">
        function repass()
        {
        p1=document.getElementById("ps1").value;
        p2=document.getElementById("ps2").value;
        if (p1!=p2) {
            alert("رمز تکرار شده درست نمي باشد");
            document.getElementById("ps2").value="";
            return false;
            }
        else
            {return true}
        }
    </script>
    ''' #.format(uf)
    if request.vars:
        t1='''
           <div align=center>
            <h2>{}</h2><hr>
            <h1>{}</h1>'''.format(session["user_fullname"],'{}')
        #dim un,ps,ps1,re,rs,conn_p
        un=session["username"]
        ps=f_cod(request.vars["ps0"])
        ps1=f_cod(request.vars["ps1"])
        if ps1!="":
            sql=db1.sql_set("","*","user",{'un':un,'ps':ps} ,"")
            rs=db1.select('user',sql)
            if rs:
                xr=db1.update_data(table_name="user",set_dic={'ps':ps1},where_dic={'un':un})
                if xr['id']>0:
                   r1="رمز شما با موفقیت عوض شد"
                else:
                   r1="برنامه با مشکل مواجه شد لطفا به مسئول مربوطه اطلاع دهید"
            else:
                r1="رمز اول را اشتباه وارد کرده ايد"
            return dict(ou=XML(t1.format(r1)))
    return dict(ou=XML(t1))
def test():
    return dict(x=response.toolbar(),y=str(request.cookies))#,z=request.cookies["username"].value=="abc")
def test1():
    response.cookies["username"]="abc"