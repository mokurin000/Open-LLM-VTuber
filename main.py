
import llm
import text2speech 
import speech2text
from dotenv import load_dotenv
import utils
import os

from datetime import datetime
now = datetime.now()

load_dotenv()  # take environment variables from .

CURRENT_SESSION_ID = now.strftime("%Y-%m-%d-%H-%M-%S")

SAVE_CHAT_HISTORY = (os.getenv("SAVE_CHAT_HISTORY") == "True")

CHAT_HISTORY_DIR = os.getenv("CHAT_HISTORY_DIR")

EXIT_PHRASE = os.getenv("EXIT_PHRASE")

MEMORY_SNAPSHOT = (os.getenv("MEMORY_SNAPSHOT") == "True")

MEMORY_DB_PATH = os.getenv("MEMORY_DB_PATH")

def textInteractionMode():
    '''
    interact with the llm in text mode, but with speech output
    '''
    while True:
        user_input = input(">> ")
        if user_input == EXIT_PHRASE:
            print("Exiting...")
            break
        else:
            callLLM(user_input)

def speechInteractionMode():
    '''
    Lauch the speech to text service and interact with the llm in speech mode.
    The function callbackToLLM is the callback function when a sentence is recognized.
    '''
    # The commented code below is for continuous speech to text service.
    # The recognizer will listen to you even when the llm is talking (so it can hear itself...)
    # Not recommended if you are using the speaker
    # recognitionResult = launchContinuousSpeech2TextService(callLLM)

    while True:
        recognitionResult = speech2text.speech2TextOnce()
        if recognitionResult == EXIT_PHRASE:
            print("Exiting...")
            break
        if(recognitionResult != ""):
            print("\nUser Input: \n" + recognitionResult + "\n")
            callLLM(recognitionResult)
            print("\n======\n")
    


def callLLM(text, verbose=False, saveChatHistory=SAVE_CHAT_HISTORY, chatHistoryDir=CHAT_HISTORY_DIR):
        '''
        Call the llm with text and print the result.
        text: str
            the text that is recognized
        '''
        result = llm.talkToLLM(text)
        if verbose:
            print(">> Results: \n")
            print(result)

        if saveChatHistory:
            message = "User: \n" + text + "\n\n" + "AI: \n" + result + "\n\n"
            utils.messageLogger(message, chatHistoryDir, CURRENT_SESSION_ID + ".txt")


        text2speech.speak(result)
        print("\n")


# =======

if __name__ == "__main__":
    if MEMORY_SNAPSHOT:
        backUpFilePath = utils.backUpFile(MEMORY_DB_PATH)
        print(">>> Memory snapshot saved at " + MEMORY_DB_PATH + ".bk")
    speechInteractionMode()

    if MEMORY_SNAPSHOT:
        revertMemory = input("\n>>> Do you want to revert the memory, not save your conversation, and pretend this conversation ever took place? (y/N)")
        if revertMemory == "y":
            utils.restoreFile(MEMORY_DB_PATH, backUpFilePath)
            print(">>> Memory reverted. This conversation never took place.")
            print(">>> But in case you need it, the message log is still saved at " + CHAT_HISTORY_DIR + "/" + CURRENT_SESSION_ID + ".txt")
        else:
            print(">>> LLM will remember this conversation.")
            print(">>> But if you change your mind, replace the memory file with " + backUpFilePath)
    
    #  textInteractionMode()

    
