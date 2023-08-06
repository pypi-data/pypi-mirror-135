def ask(title,list,toggle):
       print("-- {} --".format(title))
       a = 0
       for i in list:    
              while a < len(list):
                     print("[{}]: {}".format(a+1,list[a]))
                     a+=1
       
       if(toggle == True):
              return input("[?]: Select Option ")
       else:
              return 

