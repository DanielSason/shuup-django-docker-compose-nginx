import crossplane
import sys

payload = crossplane.parse('/etc/nginx/nginx.conf')
#payload = crossplane.parse('./new.conf')
#print(payload)
#print("\n***********************")
print(sys.argv[1])
print(sys.argv[2])
print(sys.argv[3])
b=[]
for f in payload["config"]:
	if f["file"] == '/etc/nginx/conf.d/wallak.conf':
		#print(f["parsed"][3])
		#print(f["parsed"])
		
		#print("\n\n\n", f["parsed"], "\n\n\n")
		for e in f["parsed"]:
			
			if e["directive"] == "upstream":
		#		print(e["block"][0]["args"]) 
				e["block"][0]["args"] = [sys.argv[1]+':8000']
		#		print(e["block"][0]["args"])
			if e["directive"] == "server":
				#print(e) 
				for k in e["block"]:
					if k["directive"] == "server_name":
		#				print(k["args"] )	
						k["args"] = [sys.argv[2]]
		#				print(k["args"] ) 
					if k["directive"] == "listen":
		#				print(k)
						k["args"] = [sys.argv[3], 'ssl']
		#				print(k)
		b = crossplane.build(f["parsed"])
#print("\n***********************")

#print("\n***********************\n")

#print("\n***********************a\n")

print(b)
f = open('/etc/nginx/conf.d/wallak.conf', "w")
f.write(b)
f.close()

