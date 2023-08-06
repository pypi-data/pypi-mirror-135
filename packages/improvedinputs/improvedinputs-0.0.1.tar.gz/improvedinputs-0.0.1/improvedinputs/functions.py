def ask(title,list,toggle):
       print("-- {} --".format(title))
       a = 0
       for i in list:    
              while a < len(list):
                     print("[{}]: {}".format(a,list[a]))
                     a+=1
ask("Test",["t1","t2"],True)