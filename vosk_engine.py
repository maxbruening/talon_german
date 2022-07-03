from talon import speech_system, Context
from talon.engines.vosk import VoskEngine


vosk_de = VoskEngine(model='vosk-model-de', language='de_DE')
speech_system.add_engine(vosk_de)
