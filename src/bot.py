#!/usr/bin/env python3

import irc.bot
import irc.strings
import openai
import os
import ssl
import logging
import argparse
import sys

# Set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

# Define IRC bot class
class OpenAIBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6697):
        factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname, connect_factory=factory)
        self.channel = channel

    def on_welcome(self, c, e):  # manual code. gpt didnt wanna add this
        c.join(self.channel)

    # Function to handle incoming messages
    def on_pubmsg(self, c, e):
        message = e.arguments[0]

        # If message starts with "!ai ", process the request
        if message.startswith("!ai "):

            """ so, this is pretty funny. I had issues getting it to give me a reasonable replacement to handle multi-line outputs.  just by modifying the query.. I just did my first AI-friendly total hackjob! and just realized now, I could even set a length limit. here's to the first of many dumb bad hacks with GPT!"""

            # Get the query text
            # query = message[len("!ai "):].strip()
            query = "In a single paragraph" + message[len("!ai "):].strip()  # manually changed

            # Log request to stdout
            logging.debug("Received request: %s", query)

            try:
                # Call OpenAI API to get response
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=query,
                    max_tokens=2048,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )

                # Send response to IRC channel, replacing any carriage return characters with a newline
                print(response.choices[0].text)  # manual code
                self.connection.privmsg(self.channel, response.choices[0].text.strip())

                # Log response to stdout
                logging.debug("Sent response: %s", response.choices[0].text)

            except Exception as e:
                # Print exception to IRC channel
                self.connection.privmsg(self.channel, f"Error: {str(e)}")
                logging.exception("Error processing request")

    # Function to handle channel invitations
    def on_invite(self, c, e):
        channel = e.arguments[0]
        logging.debug("Invited to join channel: %s", channel)
        self.connection.join(channel)

# Main function to start the bot
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="OpenAI IRC bot")
    parser.add_argument("--server", help="IRC server to connect to", default="irc.freenode.net")
    parser.add_argument("--port", help="Port number to connect to", type=int, default=6697)
    parser.add_argument("--nickname", help="Nickname to use in IRC", default="openaibot")
    parser.add_argument("--channel", help="Channel to join in IRC", default="#openai")
    args = parser.parse_args()

    # Create and start bot
    bot = OpenAIBot(args.channel, args.nickname, args.server, args.port)
    logging.info("Starting bot...")
    bot.start()

if __name__ == "__main__":
    main()

