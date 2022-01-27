import subprocess

subprocess.check_output('node aternosAPI-master/src/index.js --start').decode('utf-8')
info = subprocess.check_output('node aternosAPI-master/src/index.js --info').decode('utf-8')

print(info)
if "Online" in info:
    print("let's gooo")
else:
    print(":(")

# print(info)
# print(json.loads(info))
