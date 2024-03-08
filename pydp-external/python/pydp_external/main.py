# -*- mode: python; python-indent: 4 -*-
import ncs
import _ncs
from ncs.dp import Daemon
from ncs.application import Service
from ncs.experimental import DataCallbacks
import requests


# Data callback handler class for "numbers"
# an instance of this class is registered to handle reads on the "numbers" callpoint
class NumbersCallbackHandler(object):
    def __init__(self, log):
        self.log = log

    # See the DataCallbacks.register method doc:
    # https://developer.cisco.com/docs/nso/api/#!ncs-experimental/ncs.experimental.DataCallbacks.register
    def get_object(self, tctx, keypath, _args):
        self.log.info(f"NumbersCallbackHandler.get_object called. keypath={keypath}, _args={_args}")
        random_number_trivia = requests.get('http://numbersapi.com/random').text
        random_number_math = requests.get('http://numbersapi.com/random/math').text
        # this works with
        #        numbers_dcb.register('/pydp-external:external-data/pydp-external:instance',
        return {
            "numbers": {
                "trivia": random_number_trivia,
                "math": random_number_math
            }
        }

        #return { "trivia": random_number_trivia }


class WordsCallbackHandler(object):
    def __init__(self, log):
        self.log = log

    def get_object(self, tctx, keypath, _args):
        self.log.info(f"WordsCallbackHandler.get_object called. keypath={keypath}, _args={_args}")
        random_word = requests.get('https://random-word-api.herokuapp.com/word').text[2:-2]
        return { "words" : { "random": random_word } }
        

# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # instantiate handlers
        numbers_handler = NumbersCallbackHandler(self.log)
        words_handler = WordsCallbackHandler(self.log)

        # instantiate DataCallbacks helper classes
        numbers_dcb = DataCallbacks(self.log)
        words_dcb = DataCallbacks(self.log)

        # register the handlers w/ the DataCallbacks instances
#        numbers_dcb.register('/pydp-external:external-data/pydp-external:instance/pydp-external:numbers',
        numbers_dcb.register('/pydp-external:external-data/pydp-external:instance',
                             numbers_handler)
        words_dcb.register('/pydp-external:external-data/pydp-external:instance',
                           words_handler)

        # create a daemon to manage the connection between our data provder & NCS
        pydp_external_daemon = Daemon('pydp-external-daemon', log=self)

        # register the numbers DataCallbacks helper instances as data callbacks
        # using the daemon's context & the appropriate callpoints from our YANG
        _ncs.dp.register_data_cb(pydp_external_daemon.ctx(), 'numbers',
                                 numbers_dcb)
        _ncs.dp.register_data_cb(pydp_external_daemon.ctx(), 'words',
                                 words_dcb)

        # start the daemon
        pydp_external_daemon.start()

        ########################################################################
        ##### This is not accurate for data provider callbacks :) #####
        ##### Which is why we do it manually in this example. #####
        ########################################################################
        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).
        ########################################################################
        
        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
