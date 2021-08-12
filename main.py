# Author: Diego Estrada
# Org: Universidad del Valle de Guatemala
# Department: Computer Science
# August 11th 2021


import logging
from getpass import getpass
from argparse import ArgumentParser
import threading
import slixmpp
from slixmpp.xmlstream.stanzabase import ET, ElementBase
from slixmpp.exceptions import IqError, IqTimeout

class AddUser(slixmpp.ClientXMPP):
    """

    This class was made for adding an especific account to a user's roster.
    In order to add other user to the roster, user and password of the client must be provided,
    as well as the account you want to add to the roster.
    For example: 
        Client's user: test@alumchat.xyz/mobile , password:1234
        User to add:   abc@alumchat.xyz

    """
    def __init__(self, jid, password, secondUser):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.user = jid
        self.toAdd = secondUser
        

    async def start(self, event):
        self.send_presence()
        self.get_roster()
        try:
            self.send_presence_subscription(pto=self.toAdd)
        except IqTimeout:
            print("Server did not respond")
        
        self.disconnect() 


class Unregister(slixmpp.ClientXMPP):
    """

    This class was made for deleting an especific account in a xmpp server.
    In order to delete an existent account, a JID and a password must be provided.
    The JID is composed by the node/username, a domain and finally the resource (optional).
    For example: test@alumchat.xyz/mobile , password:1234

    """
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.user = jid
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.user 
        resp['id'] = 'unreg1'
        query = "<query xmlns='jabber:iq:register'>\
                <remove/>'\
                </query> "
        resp.append(ET.fromstring(query))
        try:
            print("Removing account.....")
            resp.send()
        #Error Handling
        except IqError as e:
            print("Could not remove account")
            self.disconnect()
        #Time out handling Handling
        except IqTimeout:
            print("Server did not respond")
        
        self.disconnect() 

class Register(slixmpp.ClientXMPP):
    """

    This class was made for registering new users in a xmpp server.
    In order to register a new account, a JID and a password must be provided.
    The JID is composed by the node/username, a domain and finally the resource (optional).
    For example: test@alumchat.xyz/mobile , password:1234

    """
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
            print("Account Created Successfully...", self.boundjid,"\n")
        except IqError as e:
            print("Something went wrong... ", e,"\n")
            self.disconnect()
        except IqTimeout:
            print("Timeout...")
            self.disconnect()
        except Exception as e:
            print(e)
            self.disconnect()  

class Client(slixmpp.ClientXMPP):

    """

    This class was made for both sending a message and defining a new
    presence message. To send a direct message, user's JID and password
    must be provided, as well as the recipient JID and the message to send.

    To define a different presence message, user's JID, password and the 
    new presence message must be provided.

    If you only want to log in and test it, arguments aside from JID and password
    can be passed as an empty string
    
    """

    def __init__(self, jid, password, recipient, message, op):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        # The message we wish to send, and the JID that
        # will receive it.
        self.user = jid
        self.recipient = recipient
        self.msg = message
        self.presence_message = op



        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("", self.start)

        ### Nos conectamos al servidor
        self.register_plugin('xep_0047', {
            'auto_accept': True
        }) 
        

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
        if(self.presence_message != ""):
            self.send_presence(pshow="chat", pstatus=self.presence_message)
        else:
            self.send_presence(pshow="chat", pstatus="Just logged in")
        self.get_roster()
        if(self.msg != ""):
            self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

        self.disconnect()


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser(description=Client.__doc__)

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
    while flag:
        if (notlogged == True):
            print("|----------------------Menu----------------------|")
            print("|1.  Log in                                      |")
            print("|2.  Sign up                                     |")
            print("|3.  Exit                                        |")
            print("|------------------------------------------------|")
            print("Enter the number of the option: ")
            op = input()
            if (op == "1"):
                args.jid = input("Enter username: ")
                args.password =  getpass(prompt='Enter password: ')
                xmpp = Client(args.jid, args.password,"","","")
                # xmpp.register_plugin('xep_0030') # Service Discovery
                # xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.connect()
                xmpp.process(forever=False)
                notlogged = False
            elif (op == "2"):
                args.jid = input("Username: ")
                args.password = getpass("Password: ")
                xmpp = Register(args.jid, args.password)
                xmpp.register_plugin('xep_0030') ### Service Discovery
                xmpp.register_plugin('xep_0004') ### Data Forms
                xmpp.register_plugin('xep_0066') ### Band Data
                xmpp.register_plugin('xep_0077') ### Band Registration
                xmpp.connect()
                xmpp.process(forever=False)
            elif (op == "3"):
                print("Goodbye! Thanks for using this client!")
                flag = False
        else:
            print("Welcome " + args.jid)

            print("|=====================Home=======================|")
            print("|1.  Show all contacts with their state          |")
            print("|2.  Add user to the roster                      |")
            print("|3.  Show user info                              |")
            print("|4.  Direct message                              |")
            print("|5.  Group message                               |") #Add group validation
            print("|6.  Define presence                             |")
            print("|7.  Send notification                           |")
            print("|8.  Join group                                  |")
            print("|9.  Send File                                   |")
            print("|10. Create group                                |")
            print("|11. Delete account                              |")
            print("|12. Log off                                     |")
            print("| Warning! There is a chance that you are unable |")
            print("| to use some features because your credentials  |")
            print("| are wrong. Make sure they are correct          |")
            print("|================================================|")
            print("Type a number: ")
            
            op = input()
            if(op=="2"):
                userToAdd = input("Username: ")
                xmpp = AddUser(args.jid,args.password, userToAdd)
                # xmpp.addUser(userToAdd)
                xmpp.connect()
                xmpp.process(forever=False)
            if(op=="4"):
                args.to = input("Send To: ")
                args.message = input("Message: ")
                xmpp = Client(args.jid,args.password,args.to,args.message,"")
                xmpp.connect()
                xmpp.process(forever=False)
            if(op=="6"):
                messageForPresence = input("Message: ")
                xmpp = Client(args.jid,args.password,args.to,"", messageForPresence)
                xmpp.connect()
                xmpp.process(forever=False)

            if(op=="11"):
                xmpp = Unregister(args.jid,args.password)
                
                xmpp.connect()
                xmpp.process(forever=False)

                print("Done...")
                notlogged = True
            if(op=="12"):
                notlogged = True


