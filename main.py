#!/usr/bin/env python3

# Slixmpp: The Slick XMPP Library
# Copyright (C) 2010  Nathanael C. Fritz
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.

import logging
from getpass import getpass
from argparse import ArgumentParser

import slixmpp

class Register(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.user = jid
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.disconnect()

    def register(self, iq):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['register']['username'] = self.boundjid.user
        iq['register']['password'] = self.password

        try:
            iq.send()
            print("New account created", self.boundjid,"\n")
        except IqError as e:
            print("Error on registration ", e,"\n")
            self.disconnect()
        except IqTimeout:
            print("THE SERVER IS NOT WITH YOU")
            self.disconnect()
        except Exception as e:
            print(e)
            self.disconnect()  

class SendMsgBot(slixmpp.ClientXMPP):

    """
    A basic Slixmpp bot that will log in, send a message,
    and then log out.
    """

    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        # The message we wish to send, and the JID that
        # will receive it.
        self.user = jid
        self.recipient = recipient
        self.msg = message

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the sesself.add_event_handler("register", self.register)ion_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()
        self.disconnect()
        # await self.get_roster()

        # self.send_message(mto=self.recipient,
        #                   mbody=self.msg,
        #                   mtype='chat')

        # self.disconnect()


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser(description=SendMsgBot.__doc__)

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")
    parser.add_argument("-t", "--to", dest="to",
                        help="JID to send the message to")
    parser.add_argument("-m", "--message", dest="message",
                        help="message to send")
    parser.add_argument("-r", "--register", dest="register",
                        help="Is new user")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    notlogged = True
    flag = True
    while flag:#!/usr/bin/env python3  # Slixmpp: The Slick XMPP Library # Copyright (C) 2010  Nathanael C. Fritz # This file is part of Slixmpp. # See the file LICENSE for copying permission.  import logging from getpass import getpass from argparse import ArgumentParser  import slixmpp   class SendMsgBot(slixmpp.ClientXMPP):      """     A basic Slixmpp bot that will log in, send a message,     and then log out.     """      def __init__(self, jid, password, recipient, message):         slixmpp.ClientXMPP.__init__(self, jid, password)          # The message we wish to send, and the JID that         # will receive it.         self.recipient = recipient         self.msg = message          # The session_start event will be triggered when         # the bot establishes its connection with the server         # and the XML streams are ready for use. We want to         # listen for this event so that we we can initialize         # our roster.         self.add_event_handler("session_start", self.start)      async def start(self, event):         """         Process the session_start event.          Typical actions for the session_start event are         requesting the roster and broadcasting an initial         presence stanza.          Arguments:             event -- An empty dictionary. The session_start                      event does not provide any additional                      data.         """         self.send_presence()         await self.get_roster()          self.send_message(mto=self.recipient,                           mbody=self.msg,                           mtype='chat')          self.disconnect()   if __name__ == '__main__':     # Setup the command line arguments.     parser = ArgumentParser(description=SendMsgBot.__doc__)      # Output verbosity options.     parser.add_argument("-q", "--quiet", help="set logging to ERROR",                         action="store_const", dest="loglevel",                         const=logging.ERROR, default=logging.INFO)     parser.add_argument("-d", "--debug", help="set logging to DEBUG",                         action="store_const", dest="loglevel",                         const=logging.DEBUG, default=logging.INFO)      # JID and password options.     parser.add_argument("-j", "--jid", dest="jid",                         help="JID to use")     parser.add_argument("-p", "--password", dest="password",                         help="password to use")     parser.add_argument("-t", "--to", dest="to",                         help="JID to send the message to")     parser.add_argument("-m", "--message", dest="message",                         help="message to send")      args = parser.parse_args()      # Setup logging.     logging.basicConfig(level=args.loglevel,                         format='%(levelname)-8s %(message)s')      if args.jid is None:         args.jid = input("Username: ")     if args.password is None:         args.password = getpass("Password: ")     if args.to is None:         args.to = input("Send To: ")     if args.message is None:         args.message = input("Message: ")      # Setup the EchoBot and register plugins. Note that while plugins may     # have interdependencies, the order in which you register them does     # not matter.     xmpp = SendMsgBot(args.jid, args.password, args.to, args.message)     xmpp.register_plugin('xep_0030') # Service Discovery     xmpp.register_plugin('xep_0199') # XMPP Ping      # Connect to the XMPP server and start processing XMPP stanzas.     xmpp.connect()     xmpp.process(forever=False)
        if (notlogged):
            print("|----------------------Menu----------------------|")
            print("|1.  Log in                                      |")
            print("|2.  Sign up                                     |")
            print("|------------------------------------------------|")
            print("Enter the number of the option: ")
            op = input()
            if (op == "1"):
                args.jid = input("Enter username: ")
                args.password =  getpass(prompt='Enter password: ')
                client = SendMsgBot(args.jid, args.password,"","")
                client.register_plugin('xep_0030') # Service Discovery
                client.register_plugin('xep_0199') # XMPP Ping
                client.connect()
                client.process(forever=False)
            elif (op == "2"):
                if args.jid is None:
                    args.jid = input("Username: ")
                if args.password is None:
                    args.password = getpass("Password: ")
                xmpp = Register(args.jid, args.password)
                xmpp.register_plugin('xep_0030') ### Service Discovery
                xmpp.register_plugin('xep_0004') ### Data Forms
                xmpp.register_plugin('xep_0066') ### Band Data
                xmpp.register_plugin('xep_0077') ### Band Registration
        else:
             print("tamo activo perri")
        break
    # if args.jid is None:
    #     args.jid = input("Username: ")
    # if args.password is None:
    #     args.password = getpass("Password: ")
    # if args.to is None:
    #     args.to = input("Send To: ")
    # if args.message is None:register
    #     args.message = input("Message: ")

    # Setup the EchoBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    # xmpp = SendMsgBot(args.jid, args.password, args.to, args.message)
    # xmpp.register_plugin('xep_0030') # Service Discovery
    # xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    xmpp.process(forever=False)