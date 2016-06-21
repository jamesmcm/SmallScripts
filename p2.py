import sys
import subprocess



parts=range(5)
epnum=range(120,125)

for e in epnum:
    s=""
    for p in parts:
       s+="nssl"+str(e)+"-news"+str(p)+".mp3|" 
    s+="nssl"+str(e)+"-grammar.mp3|"
    s+="nssl"+str(e)+"-expressions.mp3"
    #s=s[:-1]
    #print s
    #print "ffmpeg -i \"concat:" + str(s)+"\" -acodec copy episode"+str(e)+".mp3"
    s2="ffmpeg -i concat:" + str(s)+" -acodec copy episode"+str(e)+".mp3"
    print s2.split(" ")
    subprocess.Popen(s2.split(" "))
    #ffmpeg -i "concat:file1.mp3|file2.mp3" -acodec copy output.mp3
