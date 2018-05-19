import json
from github_webhook import Webhook
from flask import Flask
app = Flask(__name__)
webhook = Webhook(app)
@app.route("/")
def hello_world():
        return "Hello!"
@webhook.hook() # Defines a handle for 'push' event
def on_push(data):
        print("Got push with: {0}".format(data))
        os.system("cd PKGBUILD && git pull")
        actual = os.system("git rev-parse @")
        previous = os.system("git rev-parse @~")
        message = os.system("git log --format=%B  -n 1 | head -n -1")
        filepath = os.system("git diff %s %s --name-only" % previous actual)
        splittedpath = filepath.split("/")
        pkgname = splittedpath[0]
        os.system("cd aur && git clone ssh://aur@aur.archlinux.org/%s" %pkgname)
        os.system("rm %s/* && cp -a ../PKGBUILD/%s/* %s/" % pkgname)
        os.system("cd %s && git add *" % pkgname)
        os.system('git commit -m "%s"' % message)
        os.system("git push && cd ..")
        os.system("rm -rf %s" % pkgname)
        
if __name__ == "__main__":
        app.run()
