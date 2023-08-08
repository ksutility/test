# -*- coding: utf-8 -*-
# ver 1.01 1400/09/28 : customize cols in table show +  row edit 
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
xpath='0-file\\pp\\'
# ---- example index page ----
from gluon.custom_import import track_changes; track_changes(True)
from datetime import datetime
from k_sql import DB1
import kytable
import k_htm
def err_out(fun_name,msg):
    print(f'error in fun({fun_name}),msg=({msg})')
now = datetime.now().strftime("%H:%M:%S")
db_path='applications\\ksw\\databases\\'
style1='''
        <style>
            table {
              font-family: Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              text-align: center;
              width: 100%;    }

            table td, #customers th {
              border: 1px solid #ddd;
              padding: 8px; }

            table tr:nth-child(even){background-color: #f2f2f2;}

            table tr:hover {background-color: #ffccaa;}

            table th {
              padding: 8px;
              padding-top: 12px;
              padding-bottom: 12px;
              background-color: #04AA6D;
              border: 1px solid #ddd;
              
              color: white; }
        </style>
      '''
style2='''
        <style>
            table {
              font-family: Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              text-align: center;
              width: 100%;    }

            table td, #customers th {
              border: 1px solid #ddd;
              padding: 8px; }

            table tr:nth-child(even){background-color: #f2f2f2;}

            table tr:hover {background-color: #ffccaa;}

            table th {
              padding: 8px;
              padding-top: 12px;
              padding-bottom: 12px;
              background-color: #04AA6D;
              border: 1px solid #ddd;
              
              color: white; }
           
           a.box:link, a.box:visited {
              background-color: #2222aa;
              color: white;
              padding: 14px 25px;
              text-align: center;
              text-decoration: none;
              display: inline-block;
            }
            a.box:hover, a.box:active {
              background-color: #ff33ff;
            }
            
            
            input[type=button], input[type=submit], input[type=reset] {
              width:100%;
              background-color: #4CAF50;
              border: none;
              color: white;
              padding: 16px 32px;
              text-decoration: none;
              margin: 4px 2px;
              cursor: pointer;}
          input:hover {
              background-color: #ff33ff;
            }
        </style>
      '''
script1='''<script>
        $(document).ready(function(){
            $("table td").click(function(){
                $("#viewcell").text($(this).text());
            });
        });
    </script>
    '''      
def f_cod(s1, enc_st='09377953310'):
    return s1
    s2=enc_st*5
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(s1,s2)])
def reference_get_inf(ref):
    db2=DB1(db_path+ref['db']+'.db')
    rows,tit=db2.select(ref['tb'])
    idn=tit.index(ref['id'])
    '''
    r1={'titles':tit}
    r1['rows']=rows
    r1['rows_dict']={str(r[idn]):r for r in rows}
    r1['rows_format_args_val']={str(r[idn]):[r[tit.index(x)] for x in ref['format_args']] for r in rows}
    r1['format']= {str(r[tit.index(ref['id'])]):ref['format'].format(*[r[tit.index(x)] for x in ref['format_args']]) for r in rows2}
        str(r[idn]):[ref['format'].format(*r1['rows_format_args_val'][v])
        r[tit.index(x)] for x in ref['format_args']] for r in rows}
        re1[fn]=ref['format'].format(*ref_i[fn]['rows_format_args_val'][v])
    #print(str(ref_i))
    return r1
    '''
    return {str(r[tit.index(ref['id'])]):ref['format'].format(*[r[tit.index(x)] for x in ref['format_args']]) for r in rows}
def ref_get(get_case,ref_case,ref_inf,filde,base_val):
    '''
        get_case:'names'/'values'
            output case 
        ref_case:'all'/'one'
            output case '
        ref_inf:1 row in list of dict    
            all data in db of ref
        filde:dic
            the filde structure inf of base table
        base_val:text
            base table value in 1 cell of 1 row 
    '''
    if get_case not in ('names','values'):err_out('ref_get',)
    rc=ref_case
    if rc=='all':
        if get_case=='names':
            return ref_inf['titles']
        else:
            return ref_inf['rows_dict'][base_val]
    elif re=='one':
        if get_case=='names':
            return filde['name']
        else:
            return filde['ref']['format'].format(*ref_inf['rows_format_args_val'][base_va])
        
#prop:['read']=readonly ['hide']=hidden in table and edit row
cols_filter=[['lno','sbj'],
             ['lno','sbj','date_s','io_t','folder'],  ] #table_view cols filter
row_view=[{'lno':'r','sbj':'r'}]

'''
help  for (fildes={'paper )
    type:str
        link :
            'link':{'pro':['<app name>','<module name>','<func name>'],'args':['<arg_1>','<arg_2>',...,'<arg_n>']
                '<app name>','<module name>','<func name>' : format
                '<arg_1>','<arg_2>',...,'<arg_n>':format 
                format = text + {python script includ <value_nameS> } + text
                <value_nameS>=1 of [x for x in field['paper']]  
        xlink:
            'xlink' differenc by 'link' is:
                'xlink' not have value in base database file
                در فایل بانک اطلاعاتی فیلدی و اطلاعات ثبت شده ندارد
        reference:
            'ref':{'db':'database_neme','tb':'table_name','id':'id','format':'{:03d}-{}','format_args':['abb','family','pre_txt','name']}},#,
    prop:['prop1','prop2',...]
        read:
'''

fildes={'paper':{'prj':{'type':'reference','width':'30','ref':{'db':'prj','tb':'a','id':'id','format':'{:03d}-{}','format_args':['id','name']},'title':'پروژه'},#,'prop':['read']
                 'lno':{'type':'text','width':'10','title':'شماره نامه','prop':['read']},
                 'lno_t':{'type':'text','width':'10','title':'شماره پیشنویس','prop':['read']},
                 'sbj':{'type':'text','width':'50','title':'موضوع نامه','prop':['read']},
                 'date_s':{'type':'fdate','width':'10','title':'تاریخ اولین ارجاع','prop':['read']},
                 'date_e':{'type':'fdate','width':'10','title':'تاریخ آخرین ارجاع','prop':['read']},
                 'comment':{'type':'text','width':'30','title':'خلاصه','prop':['read']},
                 'cdate':{'type':'fdate','width':'10','title':'تاریخ ثبت','prop':['read']},#'prop':['hide']
                 'io_t':{'type':'text','width':'5','title':'نوع','prop':['read']},
                 'outbox':{'type':'text','width':'5','title':'ارسالی','prop':['read']},
                 'des':{'type':'text','width':'20','title':'توضیح'},#,'prop':['read']
                 'man_crt':{'type':'reference','width':'5','title':'تهیه کننده','ref':{'db':'user','tb':'user','id':'id','format':'{}-{}','format_args':['un','family','name_add','name']},'prop':['']},#,'prop':['read']
                 'man_ar_mng':{'type':'reference','width':'5','title':'مسئول طرح معماری','ref':{'db':'user','tb':'user','id':'id','format':'{}-{}','format_args':['un','family','name_add','name']},'prop':['read']},
                 'paper_num':{'type':'text','width':'6','title':'شماره کوچک','prop':['hide']},
                 'attach':{'type':'text','width':'10','title':'ضمایم','prop':['hide']},
                 'folder':{'type':'link','width':'20','title':'محل فایلها','link':{'pro':['ksw','file','f_list'],'args':['pp','{folder}']},'prop':['hide']}
                 #,'get_inf':{'type':'xlink','width':'20','title':'دانلود','link':{'pro':['ksw','aqc','import_paper_inf'],'args':['{lno}']},'prop':['hide']}                
                 #,'data':{'ks':'خودم','at':'مهندس طلابکی','ig':'مهندس قندهاری'}
                 },#,
                 #{'name':'fill_date','type':'fdate','title':'تاریخ تکمیل'}],
        'prj':{'name':{'type':'text','title':'نام پروژه'},
               'des':{'type':'text','title':'توضیحات'},
               'cat_1':{'type':'text','title':'موارد جاری'}
              },
        'user':{'un':{'type':'text','title':'نام کاربری'},
                'ps':{'type':'text','title':'پسورد'},
                'name_add':{'type':'text','title':'پیش نام'},
                'name':{'type':'text','title':'نام'},
                'family':{'type':'text','title':'فامیل'},
                'job':{'type':'reference','ref':{'db':'user','tb':'job','id':'id','format':'{}{}','format_args':['id','name']},'title':'سمت'}
               },
        'job':{'name':{'type':'text','title':'سمت'}
              }
       }
       
f_views={'paper':{}}
'''
    {'paper':{  'input':['prj','man_crt','des','date_s','folder'],
                    'view1':['lno','lno_t','sbj','date_e','comment'],
                    'view2':['cdate','io_t','outbox','man_ar_mng','paper_num','attach']
                  }
        }
'''        
for f in fildes:
    for obj_name,obj in fildes[f].items():
        if 'prop' not in obj:obj['prop']=[]
        if 'width' not in obj:obj['width']='10'
        obj['name']=obj_name
        if 'def_value' not in obj:obj['def_value']=''
#------------------------------------------------------------------------------
def htm_correct(x):
    if x:
        t= x.replace('"','|')
        return t.replace('None','-')
    else:
        return '-'         
#------------------------------------------------------------------------------         

def get_table_cols(fildes):
    #return select_cols, all_cols
    hlp={'cols_filter':'''
                none => all cols
                "#1"=>cols_filter[1]
                "1,3,4"=>cols[1],cols[3],cols[4]''',
        'data_filter':'''
               "des" like "%L%"
               "prj"="29" AND "des" like "%L-%"
            '''
        }
    all_cols=list(fildes.keys())
    #print(f'all_cols={all_cols}')
    flt=request.vars['cols_filter']
    if flt:
        if flt[0]=='#':
            select_cols=cols_filter[int(flt[1:])] 
        else:
            select_cols=[all_cols[int(x)] for x in flt.split(',')]
    else:
        select_cols= all_cols
    def set_htm_var(caption,name,help):
        val=request.vars.get(name,'') #if request.vars[name] else ''
        return (f'''<td><label><a title='{help}'>{caption}</a></label><input name='{name}' id='{name}' value='{val}' style='width:15vw'></td>''')
    """    
    htm_col_filter=XML(f'''<form><label>data_filter</label><input name="data_filter" value="{request.vars['data_filter']}" style='width:20vw'>
                    <label><a title="{hlp['cols_filter']}">cols_filter</a></label><input name="cols_filter" value="{request.vars['cols_filter']}" style='width:20vw'>
                    <label>table_class</label><input name="table_class" value='{request.vars['table_class']}' style='width:20vw'>
                    <input type="submit"></form>''')
    """
    htm_col_filter=XML('<form><table><tr>'
                            +set_htm_var(caption='data_filter',name='data_filter',help=hlp['data_filter'])
                            +set_htm_var(caption='cols_filter',name='cols_filter',help=hlp['cols_filter'])
                            +set_htm_var(caption='table_class',name='table_class',help='')
                            +'<td><input type="submit"></td></tr></table></form>')
                            
    """htm_col_filter1=FORM(TABLE(TR(
                            set_htm_var(caption='data_filter',name='filter',help=''),
                            set_htm_var(caption='cols_filter',name='cols_filter',help=cols_filter_help),
                            set_htm_var(caption='table_class',name='table_class',help=''),
                            XML('<input type="submit">'))),_class='table1')"""
    return select_cols, all_cols,htm_col_filter
#-----------------------------------------------------------------------------
def get_table_row(i,row,titles,fildes,select_cols,all_cols,ref_i):
    re1={}
    for fn in all_cols:#fn=field name
        try:
            v=row[titles.index(fn)]
        except:
            v=''
            #help:use this fun becuse 1 field like 'xlink' no have data in db
        f=fildes[fn]
        sc=f['type']
        if not v or v=='None':v=''
        if sc=='text':
            re1[fn]=htm_correct(v)
        elif sc=='reference':
            ref=f['ref']
            if fn not in ref_i:ref_i[fn]=reference_get_inf(ref)
            try:
                re1[fn]=ref_i[fn][v]
            except:
                re1[fn]='error'
        elif sc=='fdate':
            re1[fn]=v
        elif sc=='link':
            re1[fn]=v
        elif sc=='xlink':
            re1[fn]='<->'
    tds=['{:03d}'.format(row[0])]
    for fn in select_cols:#fn=field name
        f=fildes[fn]
        #print(f['type'])
        if f['type'] in ['link','xlink']:
            p=[x.format(**re1) for x in f['link']['pro']]
            #print(str(p))
            args=[x.format(**re1) for x in f['link']['args']]
            #tds.append(A(re1[fn],_href=URL('prj','file','f_list',args=('pp',re1[fn]))))#link
            tds.append(A(re1[fn],_href=URL(*p,args=tuple(args))))
        else:
            tds.append(re1[fn])
    return tds  
#-------------------------------    
#===============================================================================------------------------------------------------------------------
def show_table():
    #show simple table(no field setting need) by all data 
    #نمایش یک جدول ساده( بدون توجه به نوع فیلد) و  شامل کلیه فیلدها
    def insert_test():
        pass
        x,r=db.insert_data(table_name,['lno','sbj','i_per','i_des','i_date'],('12','abcd','2','3','xx'))
        out= f'filed =>{x}<br>add = {r}<br><h1>{now}</h1><hr>'
    def table_show():
        thead=THEAD(TR(*[TH(x) for x in titles]))
        def edit(i):
            return A('edit',_href=URL(args=(args[0],args[1],'edit',i))) if session["admin"] else '-'
        return TABLE(thead,TBODY(*[TR(*row,edit(i)) for i,row in enumerate(rows)])),len(rows)
    def row_edit(titles,vals='',comp_vals=''):
        titles.remove("id")
        if comp_vals=='':
            c_v=['' for x in titles]
        else:
            c_v=[]
            for i in range(len(titles)):
                c_v.append([c[i+1] for c in comp_vals])
        if vals=='':
            vals=['' for x in titles]
            xid=-1
        else:
            xid=vals[0]
            vals=vals[1:]
        def changed():
            for i,t in enumerate(titles):
                if request.vars[t]:
                    if request.vars[t]!=vals[i]:
                        return f'{request.vars[t]} != {vals[i]}'
            return False
        def update():
            vv={t:request.vars[t] for t in titles}
            xu=db1.update_data(table_name,vv,{'id':xid})
            return "UPDATE",BR(),"sql="+str(xu['sql']) #+"<hr>"+str(vv)
        def insert():
            vv=[request.vars[t] for t in titles]
            xi,r1=db1.insert_data(table_name,titles,vv)
            return "INSERT",BR(),"sql="+str(xi['sql']),BR(),"row id="+str(xi['id']),BR(),"result:"+str(r1)
        def save():
            if xid==-1:
                r1=insert()
            else:
                r1=update()
            return DIV(r1)
        url_b=URL(args=(args[0]))
        if changed():
            return DIV(save(),BR(),A('goto list',_href=url_b))
        else:
            i_table=FORM(TABLE(*[TR(titles[i],INPUT(_name=titel, _value=vals[i]),*c_v[i]) for i,titel in enumerate(titles)]),INPUT(_type='submit'), _action='', _method='post')
            cvt=request.vars['cv'] or ''
            #print('cvt='+cvt) 
            cv=INPUT(_value=cvt,_name='cv',_id='cv')
            return DIV(f'ID=:{xid}',cv,i_table,A('Cancel- goto list',_href=url_b))
#---------------------------------------------------------------------------------------------------
    args=request.args
    if len(args)>0:
        db_name=args[0]
        if len(args)<2:args+=['a']
        table_name=args[1] 
        db1=DB1(db_path+db_name+'.db')
        print('abc')
        rows,titles=db1.select(table_name)
        try:
            pass
        except:
            return f'error: table_name={table_name}'
        if len(args)>3 and args[2]=='edit':
            #--------------------
            cv=request.vars['cv']
            comp_vars=[]
            if cv:
                cvs=cv.split(',')
                comp_vars=[rows[int(x)-1] for x in cvs]
            #---------------------
            return row_edit(titles,rows[int(args[3])-1],comp_vars)
        if len(args)>2 and args[2]=='insert':
            return row_edit(titles)
        else:
            table,nr=table_show()
            l1=A(' NEW RECORD',_href=URL(args=(args[0],args[1],"insert"))) if session["admin"] else '-'
            t1=TABLE(TR(l1,"rows:"+str(nr),"time="+now,"args="+str(args)))
            return DIV(XML(style1),t1,table) 
    return 'error: argumwnt is needed'
#-------------------------------------------------------------------------------------------------------------------------------
def show_xtable(fildes,f_views,ref_case='one'):#,tb_name,fildes):#'example2.db'
    
    '''
    inputs:
        ref_case:select (one/all)
            show all ref table filde or one
        
    '''
    #from k_sql import DB1
    #set_table()
    def table_show(tb_name,fildes,where):
        #fieldes{name:'',type:'text' or 'reference prj' or 'select'}
        rows,titles=db1.select(tb_name,where=where)#'paper')
        if rows:rows.reverse()
        #tb=[{'id']
        select_cols, all_cols,htm_col_filter=get_table_cols(fildes)
        thead=THEAD(TR(TH('n',_width='30px'),TH('id',_width='30px'),*[TH(A(fildes[x]['title'],_title=f'{i} : {x}')) for i,x in enumerate(select_cols)]))
        trs=[]
        ref_i={}
        for i,row in enumerate(rows):
            tds=get_table_row(i,row,titles,fildes,select_cols, all_cols,ref_i)
            n=str(i+1)
            n=A(n,_title='edit',_href=URL(args=(args[0],args[1],'edit',row[0]))) if session["admin"] else n
            trs.append(TR(n,*tds))
        cc='table'+request.vars['table_class'] if request.vars['table_class'] else ''
        return TABLE(thead,TBODY(*trs),_class=cc),len(rows),htm_col_filter #DIV(,_style='height:100%;overflow:auto;')
    def row_edit(tb_name,fildes,f_views,xid=-1):
        '''
            xid=id of row that shoud be edit
                if xid=-1 => insert new row 
        '''
        
        def changed():
            for i,t in enumerate(titles):
                if request.vars[t]:
                    if request.vars[t]!=vals[i]:
                        return f'{request.vars[t]} != {vals[i]}'
            return False
        def update():
            vv={t:request.vars[t] for t in request.vars}
            xu=db1.update_data(tb_name,vv,{'id':xid})
            rr="UPDATE:"+str(xu) #+"<hr>"+str(vv)
            #print(rr)
            return rr
        def insert():
            #vv={t:request.vars[t] for t in request.vars}
            #return "INSERT",BR(),"titles="+str(titles),BR(),"vv="+str(vv)
            vv=[request.vars[t] for t in request.vars]
            tt=[t for t in request.vars]
            xi,r1=db1.insert_data(tb_name,tt,vv)
            rr="INSERT:result="+str(r1)+" => "+str(xu) #+"<hr>"+str(vv)
            #print(rr)
            return rr
        def save():
            if xid==-1:
                r1=insert()
            else:
                r1=update()
            return DIV(r1)
        def fildes_val_set(fildes,row,titles):
            for fn,f in fildes.items():
                if fn in titles:
                    f['value']=row[titles.index(fn)]
                else:
                    f['value']=''
        def edit_table_show(fildes,xid,f_views=''):
            def htm_input(x_field,x_field_name):
                fn=x_field_name
                sc=x_field['type']
                if sc=='text':
                    #ix=INPUT(_name=f['name'], _id=f['name'],_value=f['value'],_style='width:100%')
                    return XML(f"<textarea name={fn} id={fn} rows='2' style='width:100%'>{x_field['value']}</textarea>")#cols="50"
                    #if 'disabled' in f:ix=XML(f"<INPUT name={f['name']} id={f['name']} value={f['value']} style='width:100%' disabled>")
                elif sc=='reference':
                    ref=x_field['ref']
                    db2=DB1(db_path+ref['db']+'.db')
                    rows2,tit2=db2.select(ref['tb'])
                    val_dic={str(r[tit2.index(ref['id'])]):ref['format'].format(*[r[tit2.index(x)] for x in ref['format_args']]) for r in rows2}
                    return k_htm.select(_options=val_dic,_name=fn,_value=x_field['value'])
                elif sc =='fdate':
                    return INPUT(_class='fDATE',_name=fn,_id=fn,_value=x_field['value'])
                elif sc =='link':
                    return XML(f"<INPUT name={fn} id={fn} value={x_field['value']} style='width:100%'>")#INPUT(_name=fn,_id=fn,_value=f['value']),_style='width:100%'))
                else:
                    return x_field['value']
            #-------------------------------------------------
            args_c=args[:]
            args_c[3]=str(int(args[3])+1)
            t_add=A('+',_href=URL(args=args_c),_class='box')
            args_c[3]=str(int(args[3])-1)
            t_sub=A('-',_href=URL(args=args_c),_class='box')
            t_cncl=A('Cancel- goto list',_href=URL(args=(args[0],args[1])),_class='box')
            t_ok=INPUT(_type='submit',_style='width:100%,background-color:#ff00ff')
            t_sl=' | '
 
            #-------------------------------------------------
            if f_views:
                trs=[TR('id',xid)]
                trs_i=[TR(fildes[fn]['title'],htm_input(fildes[fn],fn)) for fn in f_views['input']]
                trs_v1=[TR(fildes[fn]['title'],fildes[fn]['value']) for fn in f_views['view1']]
                trs_v2=[TR(fildes[fn]['title'],fildes[fn]['value']) for fn in f_views['view2']]
                tr_ap=TR(TD(t_add,t_sl,t_sub,t_sl,t_cncl,_style='width:40%'),TD(t_ok,_style='width:60%'))
                return DIV(TABLE(*trs,*trs_v1,*trs_i,tr_ap,_style='width:100%'),TABLE(*trs_v2,_style='width:100%'),)
            else:
                trs=[TR('id',xid)]
                for fn,f in fildes.items():
                    if 'hide' in f['prop']:continue
                    if 'read' in f['prop']: #readonly
                        trs.append(TR(f['title'],f['value']))
                        continue
                    trs.append(TR(f['title'],htm_input(f,fn)))
                trs.append(TR(TD(t_add,t_sl,t_sub,t_sl,t_cncl,_style='width:40%'),TD(t_ok,_style='width:60%')))
                return DIV(TABLE(*trs,_style='width:100%'))
        #url_b=URL(args=(args[0]))
        rows,titles=db1.select(tb_name)
        titles.remove("id")
        if xid==-1:
            vals=['' for x in titles]
        else:
            #xid+=1
            vals=rows[xid-1][1:]
        if changed():
            save()
            if len(args)>3:
                args[3]=str(int(args[3])+1)
                url_b=URL(args=args)
            else:
                url_b=URL(args=(args[0],args[1]))
            redirect(url_b)
            #return DIV(save(),BR(),A('goto list',_href=url_b))
        else:
            fildes_val_set(fildes,vals,titles)
            #return "fildes="+str(fildes)+"<br>vals="+str(vals)+"<br>titles="+str(titles)
            return FORM(edit_table_show(fildes,xid,f_views), _action='', _method='post')
#----------------------------------------------------------------------------------------------------------  
    #flt=request.vars['filter']
    filter_data=request.vars.get('data_filter') #eval(flt) if flt else ''
    #print ('filter_data='+str(filter_data))
    #print(str(request.vars))
    #exec('xx={"a":"2"}')
    #xx=eval('{"a":"2"}') #'x={'+filter_data[1:-1]+'}')
    #return filter_data['id'] #filter_data
    args=request.args
    response.title='xtable-'+'-'.join(args)#[x] for x in range(0,len(args),2)])
    if len(args)>0:
        if args[0] not in fildes:
            return f'error: >  "{args[0]}" not defined in Fieldes'
        db_name=args[0]
        #print (db_name)
        if len(args)<2:args+=['a']
        tb_name=args[1]# if len(args)>1 else 'a'
        db1=DB1(db_path+db_name+'.db')
        fildes=fildes[args[0]]
        f_views=f_views[args[0]]
        #db=DB1(db_name)

        if len(args)>3 and args[2]=='edit':
            return DIV(XML(style2),row_edit(tb_name,fildes,f_views,int(args[3])))
        if len(args)>2 and args[2]=='insert':
            return DIV(XML(style2),row_edit(tb_name,fildes,f_views))
        else:
            table,nr,htm_col_filter=table_show(tb_name,fildes,filter_data)
            htm_head=DIV(TABLE(TR(  TD(A('+',_title='NEW RECORD',_href=URL(args=(args[0],args[1],"insert"))) if session["admin"] else '-',_width='20px')
                                ,TD(A(str(nr),_title="rows:"),_width='40px')
                                ,TD(DIV('...',_id='viewcell',_name='viewcell')))),_style='position:sticky;top:0px')
            return DIV(XML(style1),XML(script1),htm_col_filter,htm_head,table,)
    return 'error: argumwnt is needed'
#----------------------------------------------------------------------------------------------------------    
def show_kxtable(fildes):
    
    def table_show(tb_name,fildes):
        #fieldes{name:'',type:'text' or 'reference prj' or 'select'}
        select_cols, all_cols,htm_col_filter=get_table_cols(fildes)
        rows1,ttls1=db1.select(tb_name)#'paper')
        ttls2=['id']+[fildes[x]['title'] for x in select_cols]#+['link']
        wids2=['3']+[fildes[x]['width'] for x in select_cols]#+['4']
        rows2=[]
        ref_i={}
        for i,row in enumerate(rows1):
            tds=get_table_row(i,row,ttls1,fildes,select_cols, all_cols,ref_i)
            rows2.append(tds)#+[str(A('edit',_href=URL(args=(args[0],'edit',i))))])
        return kytable.kxtable_prepar(rows2,ttls2,wids2,"")
    #----------------------------------------------------
    args=request.args
    if len(args)>0:
        if args[0] not in fildes:
            return f'error: >  "{args[0]}" not defined in Fieldes'
        db_name=args[0]
        if len(args)<2: args+=['a']
        tb_name=args[1] #if len(args)>1 else 'a'
        db1=DB1(db_path+db_name+'.db')
        fildes=fildes[args[0]]
        return table_show(tb_name,fildes)
    return 'error: argumwnt is needed'
#----------------------------------------------------
def table_show_filter(rows,titles,filters,fildes):
    #filter={filde_name:filde_value)
    f_rows=[r for r in rows if sum([1 for x in filters if r[titles.index(x)]==str(filters[x])])==len(filters)]
    thead=['id']+[f['title'] for fn,f in fildes.items()]
    trs=[]
    for i,row in enumerate(f_rows):
        tds=[row[0]]+[row[titles.index(fn)] for fn,f in fildes.items()]
        trs.append(TR(*tds))
    n=len(f_rows)
    return (TABLE(thead,*trs),n) if n>0 else ('',n)

#---------------------------------------------------------------------------------------
def show_sptable(fildes,ref_col):
    #split data by col
    args=request.args
    if len(args)>0:
        if args[0] not in fildes:
            return f'error: >  "{args[0]}" not defined in Fieldes'
        db_name=args[0]
        if len(args)<2:args+=['a']
        tb_name=args[1] #if len(args)>1 else 'a'
        db1=DB1(db_path+db_name+'.db')
        rows1,titles1=db1.select(tb_name)
        fildes1=fildes[args[0]]

        f=[x for xn,x in fildes1.items() if xn==ref_col][0]
        ref=f['ref']
        db2=DB1(db_path+ref['db']+'.db')
        rows2,titles2=db2.select('a')
        fildes2=fildes[ref['db']]
        
        thead=['id']+[x['title'] for xn,x in fildes2.items()]
        trs=[]
        for i,row in enumerate(rows2):
            tds=[row[0]]+[row[titles2.index(fn)] for fn,f in fildes2.items()]
            filter1={ref_col:row[titles1.index(ref['id'])]}
            tb1,n=table_show_filter(rows1,titles1,filter1,fildes1)
            
            trs.append(TR(*tds,n))
            trs.append(XML('<tr><td colspan="4">'+str(tb1)+'</td></tr>'))#TD(tb1)))
        return DIV(XML(style1),TABLE(*trs))
    return 'error: argumwnt is needed'
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def index():
    f_l='لیست - '
    ff={'prj':'پروژه ها','paper':'نامه ها'}
    trs=[]
   
    if session["admin"]:
        trs+=[TR(*[TH(f_l+x) for x in ['0','x','kx','sp','select']])]#[TR(TH(f_l+'0'),TH(f_l+'X'),TH(f_l+'KX'),TH(f_l+'SP'),TH('update'))]
        for arg in ['prj','paper']:
            trs+=[TR(*[A(ff[arg],_href=URL(xtbl,args=(arg)))   for xtbl in ['table','xtable','kxtable','sptable','select']])]
        t1=DIV(DIV(A('admin',_href=URL('ksw','default','admin')))
              ,DIV(A('xxprint_reset_html',_href=URL('ksw','data','_xxprint_reset_html'),_target="x_frame")))
    else:
        trs+=[TR(*[TH(f_l+x) for x in ['x','select']])]
        for arg in ['prj','paper']:
            trs+=[TR(*[A(ff[arg],_href=URL(xtbl,args=(arg)))   for xtbl in ['xtable','select']])]
        t1=DIV('-')

    return dict(x=DIV(XML(style1),TABLE(*trs),t1))
def _xxprint_reset_html():
    import k_err
    return k_err.xxprint_reset_html()
def set_tables():
    set_table(db_name)
    return 'tables created'

def table():
    return dict(table=show_table())
def xtable():
    #f = open('applications\prj\databases\example2.json','w')
    #import json
    #json.dump(fildes,f)
    return dict(table=show_xtable(fildes,f_views))#,'paper',fildes['paper']))
def sptable():
    return dict(table=show_sptable(fildes,'prj'))
def kxtable():
    return dict(table=XML(show_kxtable(fildes)))#,'paper',fildes['paper']))
def ggtable():
    args=request.args
    #if len(args)>0:
        #try:
        #grid = SQLFORM.grid(db[args[0]],deletable=False)
        #grid = SQLFORM.grid(db.prj,deletable=False)
        #return dict(grid=grid)
        #except:
        #return f"error of open table({args[0]})"
    return "enter table name in argument of url:l="+str(args)
def select_i(fildes):
    '''
        goal 1=creat sql by pick category then pick data
        هدف = ساختن دستور اسکیوال با انتخاب دسته و یک  مقدار
        input:
            1:select category
            2:select 1 data from select_cat
        output:
            sql: select_cat=data
    '''
    args=request.args
    response.title='update-'+'-'.join(args)
    if len(args)>0:
        if args[0] not in fildes:
            return f'error: >  "{args[0]}" not defined in Fieldes'
        db_name=args[0]
        if len(args)<2:args+=['a']
        tb_name=args[1]
        db1=DB1(db_path+db_name+'.db')
        fildes=fildes[args[0]]
        ##-----
        val_dic={x:fildes[x]['title'] for x in fildes}
        s1=k_htm.select(_options=val_dic,_name='sel1',_value=request.vars['sel1'],_onchange="submit();")#$('#res1').text($(this).val())")
        ##-----
        s2,t1='',''
        if request.vars['sel1']:
            sel1=request.vars['sel1']
            traslate_dict =reference_get_inf(fildes[sel1]['ref']) if fildes[sel1]['type']=='reference' else {}
            val_dic=db1.grupList_of_colomn(tb_name,sel1,traslate_dict=traslate_dict)
            #print(str(val_dic))
            #s2=k_htm.select(_options=val_dic,_name='sel2',_value=request.vars['sel2'],_onchange="set_val();")
            s2=k_htm.select(_options=val_dic,_name='sel2',_value=request.vars['sel2'],_onchange="submit();")
            #------
            def remove(base_str,chars):
                #remove chars from base_str
                for x in chars:
                    base_str=base_str.replace(x,'')
                return base_str
            #----
            result1='"{}"{}'.format(request.vars["sel1"],request.vars["abc"])
            t1=TABLE(   THEAD(TR(*[TH(x) for x in ['index','Grup','number']])),
                        TBODY(*[TR(A(i+1,_href=URL('xtable',args=('paper'),vars={'data_filter':f'{result1}"{v}"'}))
                                   ,val_dic[v]['title'],val_dic[v]['num']) for i,v in enumerate(val_dic)]))
                        #TBODY(*[TR(i+1,*remove(val_dic[v],"()").split(':')) for i,v in enumerate(val_dic)]))
        ##-----
        i1=XML('<input name="abc" id="abc" value="=" onchange="submit();">')
        v=request.vars
        result='"{}"{}"{}"'.format(request.vars["sel1"],request.vars["abc"],request.vars["sel2"])
        result_htm=XML(f'<div name="result" id="result">{result}</div>')
        return XML(f'''<form id="form5"><label>data_filter(dict)</label>
                    {s1}
                    {i1}
                    {s2}
                    {result_htm}
                    <input type="submit">
                    {A('Open Selected List-باز کردن لیست انتخاب شده',_href=URL('xtable',args=('paper'),vars={'data_filter':result}))}
                    </form>
                    {t1}
                    <script>
                    var filter1=0
                    function submit() {{
                        document.getElementById("form5").submit();
                    }}
                    
                    $('input[type=submit]').hide();
                    </script>''')
                    
        '''
                    function set_val(){{
                        document.getElementById("result").innerHTML='"'+document.getElementById("sel1").value+'"'+document.getElementById("abc").value+'"'+ document.getElementById("sel2").value+'"';
                        
                    }}  
                    set_val();
                    '''
        
    return 'error'
def select():
    return dict(x=DIV(XML(style2),select_i(fildes)))
#                    <a href='../xtable/paper?data_filter="prj=\\'36\\'"'>---</a>
'''
        final goal=update multi filed by sql
        هدف= تغییر و به روز رسانی چندین فیلد به صورت همزمان
'''
def testj1():
    import os,k_file
    f_path2=os.path.join("0-file",'xxx1.json')
    k_file.write('json',f_path2,fildes)
    return 'ok'
def testj2():
    import os,k_file,json
    f_path2=os.path.join("0-file",'xxx1.json')
    meta=k_file.read('json',f_path2)
    return print(json.dump(meta,indent=4)) #str(meta)    
    