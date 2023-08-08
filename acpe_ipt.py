# -*- coding: utf-8 -*-
from gluon.custom_import import track_changes; track_changes(True)
def index():

    import autocad_persian_ipt as acp
    t1=DIV(INPUT(_name='t1',_id='t1',_onchange="submit();"))
    t2_t=acp.kateb_2_win(request.vars['t1']) or request.vars['t2'] or ''
    t3_t=keyboard_e2f(t2_t)
    t4_t=acp.win_2_kateb(t3_t)
    t5_t=acp.kateb_2_win(t4_t)
    t2=DIV(INPUT(_name='t2',_id='t2',_value=t2_t,_onchange="submit();",_dir="rtl",_width="100%"))
    t3=DIV(INPUT(_name='t3',_id='t3',_value=t3_t,_ondblclick="copy_txt('t3','t2');",_dir="rtl",_width="100%"))
    #t3=DIV(t3_t,_dir="rtl",_style="text-align:right;background-color:#cccccc")
    #t3=DIV(t3_t,_dir="rtl",_style="text-align:right;background-color:#cccccc")
    t4=DIV(INPUT(_name='t4',_id='t4',_value=t4_t))
    t5=DIV(t5_t,_dir="rtl",_style="text-align:right;background-color:#cccccc")
    tm1=DIV(INPUT(_name='tm1',_id='tm1',_value=request.vars['tm1']))
    tm2=DIV(INPUT(_name='tm2',_id='tm2',_value=request.vars['tm2']))
    tm3=DIV(INPUT(_name='tm3',_id='tm3',_value=request.vars['tm3']))
    '''
    t3=DIV(INPUT(_name='t3',_id='t3',_value=win_2_kateb(request.vars['t2'])))
    t4=DIV(kateb_2_win(win_2_kateb(request.vars['t2'])),_dir="rtl")
    '''
    import k_date,os
    xtime=k_date.ir_date('yy/mm/dd-hh:gg:ss')
    import share_value as share
    xpath=share.xpath()
    file_n=os.path.join(xpath,'test','__index_use_report.txt')
    with open(file_n,"a",encoding='utf8') as f:
        f.writelines('\n'.join(['','','----'+request.client,xtime,t2_t]))
    return dict(_=XML(f'''
        <script type="text/javascript" src="{URL('static','js/datepicker/jquery-1.8.2.min.js')}"></script>
        <a href="{URL('fingilish')}">فینگلیش</a>
        <form id="form5" width="100%">
            <div id='tit'><a title='Kind Smart-AutoCad Persian Editor'>KS - AUTO PERSIA </a></div>
            <div id='tit'>ویرایشگر فارسی اتوکد سازگار با فونتهای کاتب </div>
            <button id="import">import</button>
            <table width='100%'><tr>
                <td width='80%'>{t1}</td>
                <td class='td1' width='20%'><a title='کدهای قابل تشخیص در فونتهای سازگار با کاتب'>
                   محتوای متن ورودی از اتوکد </a></td>
            </tr><tr>
                <td>{t2}</td>
                <td class='td1'>محل ایجاد و یا ویرایش متن به زبان فارسی </td>
            </tr><tr>
                <td>{t3}</td>
                <td class='td1'>متن فارسی با اصلاح اتوماتیک ورودی کیبرد از حالت انگلیسی به فارسی</td>
            </tr><tr>
                <td>{t4}</td>
                <td class='td1'><a title='کدهای قابل تشخیص در فونتهای سازگار با کاتب'>
                محتوای متن خروجی به اتوکد </a></td>
            </tr><tr>
                <td>{t5}</td>
                <td class='td1'><a title=' جهت تشخیص اشتباه احتمالی در متن خروجی به اتوکد'>
                    اعتبار سنجی متن خروجی </a></td>
            </tr>
            </table>
            <button id="copy2clip">Copy to clipboard</button>
            <input type="submit">
            <HR>
            <table width='100%'>
                <tr>
                    <td>{tm1}</td>
                    <td class='td1'>memory 1</td>
                </tr><tr>
                    <td>{tm2}</td>
                    <td class='td1'>memory 2</td>
                </tr><tr>
                    <td>{tm3}</td>
                    <td class='td1'>memory 3</td>
                </tr>
            </table>
        </form>
        <style>
            input,button,#tit {{width:100%;}}
            #t2,button {{height:50px;
                font: "tahoma";
                font-size: 16px;
                font-weight: bold;
            }}
            #t2 {{background-color: coral;}}
            #tit {{font: "arial";text-align: center;align:center;font-size: 16px;}}
            td.td1 {{font-size: 12px;
                text-align:right;
                }}
             a {{background-color: SeaShell;
                }}
        </style>
        <script>
            function submit() {{
                document.getElementById("form5").submit();
            }}
            function copy2clip() {{
                var copyText = document.querySelector("#t4");
                copyText.select();
                document.execCommand("copy");
            }}
            function copy_txt(id_from,id_to) {{
                document.getElementById(id_to).value=document.getElementById(id_from).value;
            }}
            function clip2obj() {{
                //alert("start");
                // Get the text field
                var copyText = document.querySelector("#t1") //.getElementById(xid);
                //alert(copyText.value);
                
                // Select the text field
                copyText.select();
                copyText.setSelectionRange(0, 99999); // For mobile devices
                //alert("step 1");
                // Copy the text inside the text field
                navigator.clipboard.writeText(copyText.value);
                // Alert the copied text
                alert("Copied the text: " + copyText.value);
            }}
            document.querySelector("#copy2clip").addEventListener("click", copy2clip);
            document.querySelector("#import").addEventListener("click", clip2obj);
            copy2clip();
            $('input[type=submit]').hide();
        </script>'''))   
fa={    'a':'ش',
        'b':'ذ',
        'c':'ز',
        'd':'ی',
        'e':'ث',
        'f':'ب',
        'g':'ل',
        'h':'ا',
        'H':'آ',
        'i':'ه',
        'j':'ت',
        'k':'ن',
        'l':'م',
        'm':'ئ',
        'n':'د',
        'o':'خ',
        'p':'ح',
        'q':'ض',
        'r':'ق',
        's':'س',
        't':'ف',
        'u':'ع',
        'v':'ر',
        'w':'ص',
        'x':'ط',
        'y':'غ',
        'z':'ظ',
        '[':'ج',
        ']':'چ',
        '{':'ج',
        '}':'چ',
        ';':'ک',
        ':':'ک',
        '\'':'گ',
        '"':'گ',
        '\\':'پ',
        '|':'پ',
        ',':'و',
        '<':'و',
        'T':',',
        }

def keyboard_e2f(txt):
    for x in fa:
        txt=txt.replace(x,fa[x])
    return txt #''.join([fa[x] for x in txt])
def fingilish1():
    import k_finglish as fe
    t1=DIV(INPUT(_name='t1',_onchange="submit();"))
    t2_t=fe.fin_to_fa(request.vars['t1'] or '')
    t3=DIV(INPUT(_name='t3',_onchange="submit();"))
    t4_t=fe.fa_to_fin(request.vars['t3'] or '')
    t2=DIV(INPUT(_name='t2',_id='t2',_value=t2_t,_dir="rtl",_width="100%"))
    t4=DIV(INPUT(_name='t4',_id='t4',_value=t4_t))
    return dict(_=XML(f'''
        <script type="text/javascript" src="{URL('static','js/datepicker/jquery-1.8.2.min.js')}"></script>
        <a href="{URL('index')}">اتوکد</a>
        <form id="form5" width="100%">
            <div id='tit'>'finglish</div>
            <div id='tit'>فارسی به فینگلیسی </div>
            <table width='100%'><tr>
                <td>{t1}</td>
                <td class='td1'><a title='فینگلیس به'>
                   متنی که باید از فینگلیسی به فارسی برگردد </a></td>
               
                <td>{XML('==>')}</td>
                <td>{t2}</td>
                <td class='td1'>فارسی </td>
            </tr><tr>
                <td>{t3}</td>
                <td class='td1'>فارسی به </td>
                <td>{XML('==>')}</td>
                <td>{t4}</td>
                <td class='td1'><a title='فینگلیسی'>
                متن تبدیل شده از فارسی به فینگلیسی </a></td>
            </tr><tr>
            </table>
            <button id="copy2clip">Copy to clipboard</button>
            <input type="submit">
        </form>
        <style>
            table td {{border: 2px solid #000;
                width:20%;
            }}
            input,button,#tit {{width:100%;}}
            #t2,button,#tit {{height:50px;
                font: "tahoma";
                font-size: 16px;
                font-weight: bold;
            }}
            #t2 {{background-color: coral;}}
            #tit {{text-align: center;align:center;font-size: 25px;}}
            td.td1 {{font-size: 12px;
                text-align:right;
                }}
             a {{background-color: SeaShell;
                }}
        </style>
        <script>
            function submit() {{
                document.getElementById("form5").submit();
            }}
            function copy2clip(xx) {{
                var copyText = document.querySelector(xx);
                copyText.select();
                document.execCommand("copy");
            }}
            document.querySelector("#copy2clip").addEventListener("click", copy2clip("#t4"));
            copy2clip();
            $('input[type=submit]').hide();
        </script>'''))
    """
        <tr> 
                <td><button id="bt_cp1">Copy to clipboard</button></td>
                <td>-</td>
                <td><button id="bt_cp2">Copy to clipboard</button></td>
            </tr>
        """
def fingilish():
    return dict(x=XML(f'''
        <a href="{URL('index')}">اتوکد</a>
        <form id="form5" width="100%">
            <table width='100%'><tr>
                <td><h2>فینگلیش</h2></td>
                <td>{XML('<==>')}</td>
                <td><h2>فارسی</h2></td>
            </tr><tr>    
                <td><div> <input name="t1" id="t1" onkeyup="ajax('{URL('ksw','acpe', 'fingilish2',args='fin_to_fa')}', ['t1'], 't3',cp('t2'));" onchange="cp('t2')" /></div></td>
                <td><div id="t3">farsi</div></td>
                <td><div> <input name="t2" id="t2" onkeyup="ajax('{URL('ksw','acpe', 'fingilish2',args='fa_to_fin')}', ['t2'], 't3',cp('t1'));" onchange="cp('t1')" /></div></td>
            </tr></table>
            <input name="t4" id="t4" onkeyup="jq('{URL('ksw','acpe', 'fingilish2',args='fa_to_fin')}','t4', 't1')"  />
        </form>
        <script>
            function cp(xid) {{
                document.getElementById(xid).value = document.getElementById("t3").innerHTML;
            }};
            function copy2clip(xx) {{
                var copyText = document.querySelector(xx);
                copyText.select();
                document.execCommand("copy");
            }};
            document.querySelector("#bt_cp1").addEventListener("click", copy2clip("#t1"));
            document.querySelector("#bt_cp2").addEventListener("click", copy2clip("#t2"));
            alert('abv');
            function jq(xurl,xid1,xid){{
                vv=document.getElementById(xid1).value
                //alert(vv);
                $.ajax({{url:xurl ,data:{{ t4: vv }}, success: function(result){{
                    //alert(result);
                    document.getElementById(xid).value=result;
                    }},error(xhr,status,error){{
                    alert("error")
                    alert(error)
                    alert(xhr)
                    alert(JSON.stringify(xhr));
                    }} 
              }});
            }};
            
        </script>
            '''))    
def fingilish2():

    import k_finglish as fe
    args=request.args
    #return XML("abc-"+str(args))#+str(request.vars['t4']))#request.vars['t1'])
    if args:
        #v=request.vars['txt'] or ''
        if args[0]=='fin_to_fa':
            return fe.fin_to_fa(request.vars['t1'])
        elif args[0]=='fa_to_fin':
            return fe.fa_to_fin(request.vars['t4'])          
def one():
    return dict()

def echo():
    return request.vars.name  
def inf():
    t1=DIV(INPUT(_name='t1',_onchange="submit();"))
    t2_t=','.join([str(ord(x)) for x in (request.vars['t1'] or ' ')])
    t2=DIV(INPUT(_name='t2',_id='t2',_value=t2_t,_onchange="submit();",_dir="rtl",_width="100%"))
    return dict(_=XML(f'''
        <script type="text/javascript" src="{URL('static','js/datepicker/jquery-1.8.2.min.js')}"></script>
        <a href="{URL('fingilish')}">فینگلیش</a>
        <form id="form5" width="100%">
            <div id='tit'><a title='Kind Smart-AutoCad Persian Editor'>KS - AUTO PERSIA </a></div>
            <div id='tit'>ویرایشگر فارسی اتوکد سازگار با فونتهای کاتب </div>
            <table width='100%'><tr>
                <td width='80%'>{t1}</td>
                <td class='td1' width='20%'><a title='کدهای قابل تشخیص در فونتهای سازگار با کاتب'>
                   محتوای متن ورودی از اتوکد </a></td>
            </tr><tr>
                <td>{t2}</td>
                <td class='td1'>محل ایجاد و یا ویرایش متن به زبان فارسی </td>
           
            </tr>
            </table>
            <button id="copy2clip">Copy to clipboard</button>
            <input type="submit">
            <HR>
         
        </form>
        <style>
            input,button,#tit {{width:100%;}}
            #t2,button {{height:50px;
                font: "tahoma";
                font-size: 16px;
                font-weight: bold;
            }}
            #t2 {{background-color: coral;}}
            #tit {{font: "arial";text-align: center;align:center;font-size: 16px;}}
            td.td1 {{font-size: 12px;
                text-align:right;
                }}
             a {{background-color: SeaShell;
                }}
        </style>
     '''))   
    