import argparse,os,re,json
import time
import colorama
INO = 'CCHZGI8X1PD90ULJ-{"bank": {"report": [], "value": 0}}-I4U25BLKZ0OFQP59'
SIG1 = "CCHZGI8X1PD90ULJ"
SIG2 = "I4U25BLKZ0OFQP59"
def savebank(dct):
    global SIG1,SIG2
    with open(__file__,"rb") as fp:
        dat = fp.read()
        dc = json.loads(re.findall(r"CCHZGI8X1PD90ULJ-({.+?})-I4U25BLKZ0OFQP59",dat)[0])
        dcn = json.dumps(json.loads(re.findall(r"CCHZGI8X1PD90ULJ-({.+?})-I4U25BLKZ0OFQP59",dat)[0]))
        dc = dct
        nf = dat
        newdat = nf.replace("%s-%s-%s"%(SIG1,dcn,SIG2),"%s-%s-%s"%(SIG1,json.dumps(dc),SIG2))
    with open(__file__,"wb") as fp:
            fp.write(newdat)
def GetValue():
    with open(__file__,"rb") as fp:
        dat = fp.read()
        dc = json.loads(re.findall(r"CCHZGI8X1PD90ULJ-({.+?})-I4U25BLKZ0OFQP59",dat)[0])
        return dc
def main():
        colorama.init()
        parser = argparse.ArgumentParser()
        parser.add_argument("--show",action="store_true")
        parser.add_argument("--add","-A",type=float)
        parser.add_argument("--sub","-S",type=float)
        parser.add_argument("--reset","-R",action="store_true")
        args = parser.parse_args()
        if(args.add):
                dc = GetValue()
                dc["bank"]["value"] += args.add
                if(dc["bank"].has_key("report")):
                        dc["bank"]["report"].append({"type":1,"count":args.add,"ts":time.time()})
                else:
                        dc["bank"]["report"] = []
                print("Added your account %s TL. Now you have %s TL"%(colorama.Fore.GREEN+str(args.add)+colorama.Fore.RESET,colorama.Fore.YELLOW+str(dc["bank"]["value"])+colorama.Fore.RESET))
                savebank(dc)
        elif(args.sub):
                dc = GetValue()
                dc["bank"]["value"] -= args.sub
                if(0 > dc["bank"]["value"]):
                        dc["bank"]["value"] = 0
                if(dc["bank"].has_key("report")):
                        dc["bank"]["report"].append({"type":0,"count":args.sub,"ts":time.time()})
                else:
                        dc["bank"]["report"] = []
                print("Taken %s TL. Now you have %s TL"%(colorama.Fore.RED+str(args.sub)+colorama.Fore.RESET,colorama.Fore.YELLOW+str(dc["bank"]["value"])+colorama.Fore.RESET))
                savebank(dc)
        elif(args.reset):
                dc = GetValue()
                dc["bank"]["value"] = 0
                dc["bank"]["report"] = []
                print(colorama.Fore.RED+"Resetting account."+colorama.Fore.RESET)
                savebank(dc)
        elif(args.show):
                dc = GetValue()
                fr = colorama.Fore
                bg = colorama.Back
                report = fr.BLUE+"Account Report"+fr.RESET+"\n"
                report += "\tMoney : %s TL"%(fr.GREEN+str(dc["bank"]["value"])+fr.RESET)+"\n"
                report += fr.BLUE+"Account History"+fr.RESET+"\n"
                if(dc["bank"]["report"]):
                        for rep in dc["bank"]["report"]:
                                if(rep["type"] == 1):
                                        report += "\t"+fr.LIGHTBLUE_EX+time.strftime("[%b %d %Y %H:%M:%S] ",time.gmtime(rep["ts"]+60*60*3))+fr.RESET+" Deposited %s TL"%(fr.GREEN+str(rep["count"])+fr.RESET)+"\n"
                                elif(rep["type"] == 0):
                                        report += "\t"+fr.LIGHTBLUE_EX+time.strftime("[%b %d %Y %H:%M:%S] ",time.gmtime(rep["ts"]+60*60*3))+fr.RESET+" Wasted %s TL"%(fr.RED+str(rep["count"])+fr.RESET)+"\n"
                else:
                        report+= fr.RED+"\tNo mobility in your account"+fr.RESET+"\n"
                report += bg.WHITE+fr.BLACK+"Now you have %s TL"%(fr.RED+str(dc["bank"]["value"])+fr.RESET+fr.BLACK)+"\n"+fr.RESET+bg.RESET
                print report
        else:
                parser.print_help()
if __name__ == "__main__":
    main()
