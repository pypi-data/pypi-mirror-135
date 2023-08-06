import json
import os
import dill


class varstore:
    def __init__(self):
        print("mlOS Variable Store - Session initialized...")
        self.wp="/root/wp/mos"
        _uhome=os.path.expanduser('~')
        _wp = os.path.join(_uhome, 'wp',"mos")
        uinfohere=os.path.join(_wp,"users")
        self.wp=_wp
        if(os.path.exists(uinfohere)):
            self.wp=_wp
    def getwp(self,_vtoken):
        _uhome=os.path.expanduser('~')
        _wp = os.path.join(_uhome, 'wp',"mos")
        uinfohere=os.path.join(_wp,"users")
        self.wp=_wp
        if(os.path.exists(uinfohere)):
            return _wp
        else:
            return self.wp
    def addvariable(self,varinfo, _vtoken):
        try:
            wp=self.getwp(_vtoken)
            if "wp" in varinfo:
                wp=varinfo["wp"]
            # uname= varinfo["uname"]
            varname= varinfo["varname"]
            vartype= varinfo["vartype"]
            # dtype= varinfo["datatype"]
            # vver= varinfo["varversions"]

            if(vartype=="local"):
                if("varpin" in varinfo):
                    vver= varinfo["varpin"]
                else:
                    tmp={
                        "msg":"Owner is not there.",
                        "success":False,
                        "error":True,
                    }
                    return tmp

            varpath=os.path.join(wp,"varstore")
            if(os.path.exists(varpath)==False):
                os.mkdir(varpath)
            
            if(vartype=="local"):
                vpath=os.path.join(varpath,"local")
                if(os.path.exists(vpath)==False):
                    os.mkdir(vpath)
                vver= varinfo["varpin"]
                varnamedr= os.path.join(vpath,vver)
                if(os.path.exists(varnamedr)==False):
                    os.mkdir(varnamedr)
                varnamedr= os.path.join(vpath,vver,varname)
                if(os.path.exists(varnamedr)==False):
                    os.mkdir(varnamedr)
                    confn=os.path.join(varnamedr,"conf.pkl")
                    with open(confn,"wb") as outfile:
                        dill.dump(varinfo,outfile)
                    tmp={
                        "msg":"Created",
                        "success":True,
                        "error":False,
                    }
                    return tmp
                else:
                    tmp={
                        "msg":"Already Exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
            elif(vartype=="global"):
                vpath=os.path.join(varpath,"global")
                if(os.path.exists(vpath)==False):
                    os.mkdir(vpath)
                varnamedr= os.path.join(vpath,varname)
                if(os.path.exists(varnamedr)==False):
                    os.mkdir(varnamedr)
                    confn=os.path.join(varnamedr,"conf.pkl")
                    with open(confn,"wb") as outfile:
                        dill.dump(varinfo,outfile)
                    tmp={
                        "msg":"Created",
                        "success":True,
                        "error":False,
                    }
                    return tmp
                else:
                    tmp={
                        "msg":"Already Exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
            else:
                tmp={
                    "msg":"Not proper varibale type.",
                    "success":False,
                    "error":True,
                }
                return tmp

            tmp={
                    "msg":"Not proper varibale type.",
                    "success":False,
                    "error":True,
                }
            return tmp
        except:
            raise
            tmp={
                "msg":"Variable can not initiated.",
                "success":False,
                "error":True,
            }
            return tmp

    
    def getvariable(self,varinfo,_vtoken):
        try:
            wp=self.getwp(_vtoken)
            if "wp" in varinfo:
                wp=varinfo["wp"]
            varname= varinfo["varname"]
            vartype= varinfo["vartype"]
            
            vowner= "global"

            varpath=os.path.join(wp,"varstore")

            if(os.path.exists(varpath)==False):
                os.mkdir(varpath)
                tmp={
                    "msg":"Variable does not exists.",
                    "success":False,
                    "error":True,
                }
                return tmp
            if(vartype=="local"):
                vpath=os.path.join(varpath,"local")
                vver= varinfo["varpin"]
                varnamedr= os.path.join(vpath,vver,varname)
                if(os.path.exists(varnamedr)):
                    confn=os.path.join(varnamedr,"conf.pkl")
                    _cursor= varinfo["cursor"]
                    _curfile=os.path.join(varnamedr,str(_cursor)+".pkl")
                    if(os.path.exists(_curfile)):
                        with open(_curfile,"rb") as infile:
                            var_i=dill.load(infile)
                        tmp={
                            "value":var_i,
                            "msg":"Created",
                            "success":True,
                            "error":False,
                        }
                        return tmp
                    else:
                        _curfile=os.path.join(varnamedr,"1.pkl")
                        print(_curfile)
                        if(os.path.exists(_curfile)):
                            with open(_curfile,"rb") as infile:
                                var_i=dill.load(infile)
                            tmp={
                                "value":var_i,
                                "warning":"yes",
                                "msg":"Specific cursor not found",
                                "msg":"Created",
                                "success":True,
                                "error":False,
                            }
                            return tmp
                        else:
                            tmp={
                                "msg":"Variable does not exists.",
                                "success":False,
                                "error":True,
                            }
                            return tmp
                else:
                    tmp={
                        "msg":"Variable does not exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
            elif(vartype=="global"):
                vpath=os.path.join(varpath,"global")
                if(os.path.exists(vpath)==False):
                    tmp={
                        "msg":"Variable does not exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
                
                varnamedr= os.path.join(vpath,varname)
                print(varnamedr)
                if(os.path.exists(varnamedr)):
                    confn=os.path.join(varnamedr,"conf.pkl")
                    _cursor="1"
                    if("cursor" in varinfo):
                        _cursor= varinfo["cursor"]
                    _curfile=os.path.join(varnamedr,str(_cursor)+".pkl")
                    print(_curfile)
                    if(os.path.exists(_curfile)):
                        with open(_curfile,"rb") as infile:
                            var_i=dill.load(infile)
                        tmp={
                            "value":var_i,
                            "msg":"Created",
                            "success":True,
                            "error":False,
                        }
                        return tmp
                    else:
                        _curfile=os.path.join(varnamedr,"1.pkl")
                        if(os.path.exists(_curfile)):
                            with open(_curfile,"rb") as infile:
                                var_i=dill.load(infile)
                            tmp={
                                "value":var_i,
                                "msg":"Created",
                                "success":True,
                                "error":False,
                            }
                            return tmp
                        else:
                            tmp={
                                "msg":"Variable does not exists.",
                                "success":False,
                                "error":True,
                            }
                            return tmp
                else:
                    tmp={
                        "msg":"Variable does not exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
        except:
            raise
            tmp={
                "msg":"Variable not found",
                "success":False,
                "error":True,
            }
            return tmp


    def setvariable(self,varinfo,value,cursor,_vtoken):
        try:
            wp=self.getwp(_vtoken)
            if "wp" in varinfo:
                wp=varinfo["wp"]
            varname= varinfo["varname"]
            vartype= varinfo["vartype"]
            
            vowner= "global"

            varpath=os.path.join(wp,"varstore")

            if(os.path.exists(varpath)==False):
                os.mkdir(varpath)
                tmp={
                    "msg":"Variable does not exists.",
                    "success":False,
                    "error":True,
                }
                return tmp
            if(vartype=="local"):
                vpath=os.path.join(varpath,"local")
                vver= varinfo["varpin"]
                varnamedr= os.path.join(vpath,vver,varname)
                if(os.path.exists(varnamedr)):
                    confn=os.path.join(varnamedr,"conf.pkl")
                    _cursor= str(cursor)
                    _curfile=os.path.join(varnamedr,str(_cursor)+".pkl")
                    with open(_curfile,"wb") as outfile:
                        dill.dump(value,outfile)
                    tmp={
                        "msg":"Created",
                        "success":True,
                        "error":False,
                    }
                    return tmp
                else:
                    tmp={
                        "msg":"Variable does not exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
            elif(vartype=="global"):
                vpath=os.path.join(varpath,"global")
                varnamedr= os.path.join(vpath,varname)
                if(os.path.exists(varnamedr)):
                    confn=os.path.join(varnamedr,"conf.pkl")
                    _cursor= str(cursor)
                    _curfile=os.path.join(varnamedr,str(_cursor)+".pkl")
                    with open(_curfile,"wb") as outfile:
                        dill.dump(value,outfile)
                    tmp={
                        "msg":"Created",
                        "success":True,
                        "error":False,
                    }
                    return tmp
                else:
                    tmp={
                        "msg":"Variable does not exists.",
                        "success":False,
                        "error":True,
                    }
                    return tmp
        except:
            raise
            tmp={
                "msg":"Variable not found",
                "success":False,
                "error":True,
            }
            return tmp