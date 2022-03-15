from talon import speech_system, Context
from talon.engines.vosk import VoskEngine

vosk_de = VoskEngine(model='vosk-model-de-0.6', language='de_DE')
speech_system.add_engine(vosk_de)
