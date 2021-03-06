#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pprint
from get_sentence import get_sentence
from debug_lib.help_lib import  print_intentMessage
from debug_lib.help_lib import  save_intentMessage
import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

SAY_SOMTHING_NICE = "mardeh:sagwasnettes"


class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    print("subscribe_intent_callback")
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    session_id = intentMessage.session_id
    print("action_wrapper")
    print_intentMessage(intentMessage)
    save_intentMessage(intentMessage, "tmp/{}_messageInfo.txt".format(session_id))
    sentence = get_sentence()
    hermes.publish_end_session(intentMessage.session_id, sentence)


if __name__ == "__main__":
    print("MAIN MAIN")
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent(SAY_SOMTHING_NICE, subscribe_intent_callback) \
         .start()
