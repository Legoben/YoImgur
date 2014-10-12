from tornado import web, ioloop, httpclient
import pyimgur
import json

print("restarted")

conf = json.loads(open("conf.json").read())
im = pyimgur.Imgur(conf['imgur_key'])


class YoHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.finish()

        username = self.get_argument("username", None, False)
        link = self.get_argument("link", None, True)

        print(username, link)

        if username == None or link == None:
            return

        try:
            uploaded_image = im.upload_image(url=link)
        except Exception:
            print("not image")
            return

        print(uploaded_image.link)

        self.sendYo(username,uploaded_image.link)

    def sendYo(self, username, link):
        client = httpclient.HTTPClient()
        body = "username="+username+"&link="+link+"&api_token="+conf['yo_key']
        req = httpclient.HTTPRequest("https://api.justyo.co/yo/", method="POST",body=body)
        client.fetch(req)
        pass




app = web.Application([
     (r'/yo', YoHandler),
], debug=True)

if __name__ == '__main__':
    app.listen(9009)
    ioloop.IOLoop.instance().start()