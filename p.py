import wget

months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

years = [13, 14]

days = range(32)

parts = range(10)

dates=["2015-10-20","2015-10-13","2015-10-06","2015-09-29","2015-09-22"]

epnum=range(120,120+len(dates))
dates.reverse()

#http://nssl.l360-audio.com/2014/may1314/nssl49-expressions.mp3
#http://nssl.l360-audio.com/2014/may1314/nssl49-grammar.mp3


for i in range(len(dates)):
    date=dates[i]
    l=date.split("-")
    year=l[0]
    month=l[1]
    day=l[2]
    for part in range(6):
        url="http://nssl.l360-audio.com/"+str(year)+"/"+months[int(month)-1]+str(day)+str(year[-2:])+"/nssl"+str(epnum[i])+"-news"+str(part)+".mp3"
        wget.download(url)
    url="http://nssl.l360-audio.com/"+str(year)+"/"+months[int(month)-1]+str(day)+str(year[-2:])+"/nssl"+str(epnum[i])+"-expressions.mp3"
    print url
    wget.download(url)
    url="http://nssl.l360-audio.com/"+str(year)+"/"+months[int(month)-1]+str(day)+str(year[-2:])+"/nssl"+str(epnum[i])+"-grammar.mp3"
    print url
    wget.download(url)
    i+=1



# for year in years:
#     for month in months:
#         print str(month)+str(year)
#         for day in days:
#             for ep in epnum:
#                 for part in parts:
#                     url="http://nssl.l360-audio.com/20"+str(year)+"/"+str(month)+str(day)+str(year)+"/nssl"+str(ep)+"-news"+str(part)+".mp3"
#                     wget.download(url)




