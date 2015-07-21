import json
import webapp2
import telegram
import logging
from devops_reactions import DevOpsReactions

from google.appengine.api import urlfetch

bot = telegram.Bot('<TOKEN>')
bot.setWebhook('https://<URL>/<TOKEN>')

class DevOpsReactionsBotWebhookPage(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)

        logging.debug('Request: %s' % self.request.body)
        body = json.loads(self.request.body)
        update = telegram.Update.de_json(body)

        chat_id = update.message.chat.id
        message = update.message.text

        if '/start' in message or '/help' in message:
            bot.sendMessage(chat_id=chat_id,
                            text='Hello! I am DevOpsReactions Bot, I can serve the latest DevOps Reactions post or a random one. What would you like?\n\nYou can control me by sending these commands:\n\n/latest - Latest DevOps Reactions post\n/random - Random DevOps Reactions post')

        image = None
        if '/latest' in message:
            image = DevOpsReactions.latest()
        if '/random' in message:
            image = DevOpsReactions.random()

        if image:
            bot.sendMessage(chat_id=chat_id,
                            text=image['title'])
            bot.sendChatAction(chat_id=chat_id,
                               action=telegram.ChatAction.UPLOAD_PHOTO)
            bot.sendDocument(chat_id=chat_id,
                             document=image['image_url'])

        self.response.write(json.dumps(body))


app = webapp2.WSGIApplication([
    ('/<TOKEN>', DevOpsReactionsBotWebhookPage),
], debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    webapp.util.run_wsgi_app(app)

if __name__ == '__main__':
    main()
