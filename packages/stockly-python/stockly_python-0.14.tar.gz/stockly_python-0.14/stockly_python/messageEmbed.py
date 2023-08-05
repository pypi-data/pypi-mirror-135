import json
from datetime import datetime
class messageEmbed:
    def setColor(self, color):
        self.data['color'] = color
        self.color = color
        return self.data

    def setTitle(self, title):
        self.data['title'] = title
        self.title = title
        return self.data
  
    def setURL(self, url):
        self.data['url'] = url
        self.url = url
        return self.data

    def setAuthor(self, name, iconURL, url) :
        self.data['author'] = { "name" : name, "iconURL" : iconURL, "url" : url }
        self.author = { name, iconURL, url }
        return self.data
    
    def setDescription(self, description) :
        self.data['description'] = description
        self.description = description
        return self.data

    def setThumbnail(self, url) :
        self.data['thumbnail'] = url
        self.thumbnail = url
        return self.data

    def setImage(self, url) :
        self.data['image'] = url
        self.image = url
        return self.data

    def setTimestamp(self) :
        self.data['timestamp'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.timestamp = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        return self.data

    def setFooter(self, text, iconURL) :
        self.data['footer'] = { "text": text, "iconURL": iconURL }
        self.footer =  { "text": text, "iconURL": iconURL }
        return self.data
    def getJson(self):
        return json.dumps(self.data)
    def __init__(self):
        self.data = {}
    def __str__(self):
        return json.dumps(self.data)