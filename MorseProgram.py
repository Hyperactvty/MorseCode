import datetime
import keyboard
import sys

MorseLexicon = {
  "A": ".-",
  "B": "-...",
  "C": "-.-.",
  "D": "-..",
  "E": ".",
  "F": "..-.",
  "G": "--.",
  "H": "....",
  "I": "..",
  "J": ".---",
  "K": "-.-",
  "L": ".-..",
  "M": "--",
  "N": "-.",
  "O": "---",
  "P": ".--.",
  "Q": "--.-",
  "R": ".-.",
  "S": "...",
  "T": "-",
  "U": "..-",
  "V": "...-",
  "W": ".--",
  "X": "-..-",
  "Y": "-.--",
  "Z": "--..",
  "1": ".----",
  "2": "..---",
  "3": "...--",
  "4": "....-",
  "5": ".....",
  "6": "-....",
  "7": "--...",
  "8": "---..",
  "9": "----.",
  "0": "-----",
  " ": "/",
  "RE-MORSE": "........" # Deletes up to the most recent space (/)
}

class Settings:
    class Mode:
        Morse2Alpha = 0
        Alpha2Morse = 1

    def __init__(self, _ib=0.1875, _cb=1.0, _pm=Mode.Alpha2Morse, _sto=30):
        self.inputBuffer = _ib # This is the delay between a long press or a short press
        self.charBuffer = _cb # This is the delay before the character is converted
        self.programMode = _pm # The program's mode
        self.selfTimeout = _sto # Time before the program auto stops

class Input:
    def __init__(self, _is=0, _ie=0):
        self.inputStart = _is
        self.inputEnd = _ie

class MorseProgram:
    def getCode(_s: Settings.Mode, _c: str, _reverse: bool=False):
      if(_s==Settings.Mode.Alpha2Morse): _c=_c.upper()
      
      vals = MorseLexicon.values() if _s == (Settings.Mode.Morse2Alpha if _reverse==False else Settings.Mode.Alpha2Morse) else MorseLexicon.keys()
      if not any(_c in q for q in vals): return
      res=""
      if(_s == (Settings.Mode.Morse2Alpha if _reverse==False else Settings.Mode.Alpha2Morse)):
        res = [r for r, q in MorseLexicon.items() if q == _c]
        if(res==[]): return
        res=res[0]
      else:
        res = MorseLexicon[_c]
      if(res==[]): return
      return res#[0]

    @staticmethod
    def main(_mode=None):
      settings = Settings()
      mode = next(_m for _m in _mode) # sys.argv
      MODES = {"morse": Settings.Mode.Morse2Alpha, "alpha": Settings.Mode.Alpha2Morse }
      if(next(_m for _m in _mode) in list(MODES.keys())): mode = MODES[mode]
      else:
        print(f"IMPORTANT:  Mode was not specified. Running program in [MORSE]")
        mode=MODES["morse"]
      user_input = Input()

      input_registered = False
      char_registered = False
      program_started = True
      cBuf = datetime.datetime.now()
      elapsed_ticks = (datetime.datetime.now() - cBuf).total_seconds()
      timeFromLastInput=0.0
      code = ""; codeBuffer=""; codeString = ""
      print("Press ESC to stop")
      # while not keyboard.is_pressed('escape'):
      while True:
          if((datetime.datetime.now() - cBuf).total_seconds()>settings.selfTimeout): print("\nPROGRAM TIMEOUT"); break
          if(keyboard.is_pressed('escape')): print("\nPROGRAM TERMINATED"); break
          # something about char_registered to get around the first tick geing counted
          if(program_started==True and mode==Settings.Mode.Morse2Alpha):
            if keyboard.is_pressed('space'):
              program_started=False
              elapsed_ticks = 0
              cBuf = datetime.datetime.now()
            else: continue
          else: elapsed_ticks = (datetime.datetime.now() - cBuf).total_seconds()
          
          # ALPHA2MORSE
          if(mode==Settings.Mode.Alpha2Morse):
            res = MorseProgram.alpha2Morse(codeString)
            if(res["msg"]==None or res["status"]==-1): continue # to avoid "ghost" (non-alpha inputs) or "repeat" inputs
            _cs = res["msg"]
            codeString = _cs if _cs!=None and type(codeString)!=type(None) else codeString
            cBuf=datetime.datetime.now()
            print(f"\n{codeString}", sep=' ', end='', flush=True)
            print() # Temp, maybe
            for _c in codeString:
              c=MorseProgram.getCode(mode, _c, False)
              print(c, sep=' ', end=' ', flush=True)

            continue
          
          if(elapsed_ticks > settings.charBuffer and char_registered==False):
            char_registered=True
            cs = MorseProgram.getCode(mode, code)
            if(cs==None):  # Have this reset the current "input"
              code=""
              char_registered = True
              elapsed_ticks=0
              print("\nInvalid Input")
              MorseProgram.codeOutput(settings,codeString,codeBuffer)
              continue
            if(cs in ["........", "RE-MORSE"]): # Deletes up to last space
              code=""
              char_registered = True
              elapsed_ticks=0
              # reMorse = codeString.split(" ")[:-1].join(str(_c) for _c in codeString.split(" ")[:-1])
              codeBuffer = reMorse = ""
              program_started=True
              print(f"\nYou show re-morse...")
              MorseProgram.codeOutput(settings,codeString,codeBuffer)
              continue
            # codeString += cs
            codeBuffer += cs
            code = ""
            print(f"\n{codeString}> {codeBuffer}")
            # Runs through the existing code
            MorseProgram.codeOutput(settings,codeString,codeBuffer)
          # if not console_key_available():
          if keyboard.is_pressed('space'):
            if input_registered:
                input_registered = False
                char_registered = False
                cBuf = datetime.datetime.now()
                elapsed_ticks = (datetime.datetime.now() - cBuf).total_seconds()
          else:
              if not input_registered:
                  input_registered = True
                  elapsed_ticks = (datetime.datetime.now() - cBuf).total_seconds()
                  cBuf = datetime.datetime.now()
                  timeFromLastInput=elapsed_ticks
                  input_registered_as = "-" if elapsed_ticks > settings.inputBuffer else "."
                  # print(f"Input held for {elapsed_ticks} -> Input registered as {input_registered_as}")
                  print(input_registered_as, sep=' ', end='', flush=True)
                  code+=input_registered_as
                  # For the reset (..?)
                  # print(f"{elapsed_ticks}")

                  # reset()

              # Space Integration
              if(elapsed_ticks-timeFromLastInput > settings.charBuffer*4):
                cs = MorseProgram.getCode(mode, "/")
                print("/", sep=' ', end=' ', flush=True)
                codeString += codeBuffer + cs
                codeBuffer=""
                program_started=True

    def codeOutput(mode,codeString,codeBuffer):
      for _c in codeString+codeBuffer:
        c=MorseProgram.getCode(mode, _c, True)
        print(c, sep=' ', end=' ', flush=True)

    def alpha2Morse(_cs: str):
      event = keyboard.read_event()
      # THIS IS WHERE THE PROGRAM HALTS UNTIL AN INPUT IS PRESSED
      if event.event_type == keyboard.KEY_DOWN:# and event.name != '>':
        cStr=_cs
        keyShortcuts = {
          "space" : " ",
          "backspace": "backspace"
        }
        key = keyShortcuts.get(event.name) if keyShortcuts.get(event.name) != None else (event.name if len(event.name)==1 and event.name.isalnum() else None)
        if(key=="backspace"): return { "msg": cStr[:-1], "status": 200 }
        if(key==None): return { "msg": cStr, "status": -1 }
        cStr += key
        return { "msg": cStr, "status": 200 }
      return { "msg": None, "status": -1 }


if(__name__ == "__main__"): MorseProgram.main(sys.argv[1:])
