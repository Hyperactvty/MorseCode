import datetime
import keyboard

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
    @staticmethod
    def main():
        settings = Settings()
        user_input = Input()

        # TESTING
        current_date = datetime.datetime.now()
        elapsed_ticks = (datetime.datetime.now() - current_date).total_seconds()
        # TESTING END

        input_registered = False
        tmp = 0
        print("Press ESC to stop")
        while True:
            tmp += 1
            if not console_key_available():
                input_registered = False
                current_date = datetime.datetime.now()
                elapsed_ticks = (datetime.datetime.now() - current_date).total_seconds()
                print(f"{tmp} Start -> {elapsed_ticks}")
            else:
                print("ELSE")
                if not input_registered:
                    input_registered = True
                    elapsed_ticks = (datetime.datetime.now() - current_date).total_seconds()
                    input_registered_as = "-" if elapsed_ticks > settings.inputBuffer else "."
                    print(f"Input held for {elapsed_ticks} -> Input registered as {input_registered_as}")

    def calculate():
        pass

def console_key_available():
    import msvcrt
    return msvcrt.kbhit()

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

def getCode(_s: Settings, _c: str, _reverse: bool=False):
  # if not any(_c in q for q in MorseLexicon.get(_c)): return
  if(_s.programMode==1): _c=_c.upper()
  # vals = MorseLexicon.values() if _s.programMode == (0 if _reverse==False else 1) else MorseLexicon.keys()
  # print("MorseLexicon.values()" if _s.programMode == (0 if _reverse==False else 1) else "MorseLexicon.keys()")
  
  vals = MorseLexicon.values() if _s.programMode == (0 if _reverse==False else 1) else MorseLexicon.keys()
  if not any(_c in q for q in vals): return
  # res = list(filter(lambda q: (_c in q), vals))
  # print(list(vals))

  # ORIGINAL
  # res = [r for r, q in MorseLexicon.items() if q == _c]
  res=""
  if(_s.programMode == (0 if _reverse==False else 1)):
    res = [r for r, q in MorseLexicon.items() if q == _c]
    if(res==[]): return
    res=res[0]
  else:
    # res = next((q for q in (MorseLexicon.values() if _s.programMode == (1 if _reverse==False else 0) else MorseLexicon.keys()) if q==_c),"None?")
    # vals = MorseLexicon.values() if _s.programMode == (1 if _reverse==False else 0) else MorseLexicon.keys()
    # res = [k for k in vals if k == _c][0]
    res = MorseLexicon[_c]
  if(res==[]): return

  # print(f"RES : {res} | code -> {_c}")
  return res#[0]

def main():
  settings = Settings()
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
      if(program_started==True and settings.programMode==0):
        if keyboard.is_pressed('space'):
          program_started=False
          elapsed_ticks = 0
          cBuf = datetime.datetime.now()
        else: continue
      else: elapsed_ticks = (datetime.datetime.now() - cBuf).total_seconds()
      
      # ALPHA2MORSE
      if(settings.programMode==1):
        _cs = alpha2Morse(codeString)
        if(_cs==None): continue # to avoid "ghost" or "repeat" inputs
        codeString = _cs if _cs!=None and type(codeString)!=type(None) else codeString
        cBuf=datetime.datetime.now()
        print(f"\n{codeString}", sep=' ', end='', flush=True)
        print() # Temp, maybe
        for _c in codeString:
          c=getCode(settings, _c, False)
          print(c, sep=' ', end=' ', flush=True)

        continue
      
      if(elapsed_ticks > settings.charBuffer and char_registered==False):
        char_registered=True
        cs = getCode(settings, code)
        if(cs==None):  # Have this reset the current "input"
          code=""
          char_registered = True
          elapsed_ticks=0
          print("\nInvalid Input")
          codeOutput(settings,codeString,codeBuffer)
          continue
        if(cs in ["........", "RE-MORSE"]): # Deletes up to last space
          code=""
          char_registered = True
          elapsed_ticks=0
          # reMorse = codeString.split(" ")[:-1].join(str(_c) for _c in codeString.split(" ")[:-1])
          codeBuffer = reMorse = ""
          program_started=True
          print(f"\nYou show re-morse...")
          codeOutput(settings,codeString,codeBuffer)
          continue
        # codeString += cs
        codeBuffer += cs
        code = ""
        print(f"\n{codeString}> {codeBuffer}")
        # Runs through the existing code
        codeOutput(settings,codeString,codeBuffer)
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
            cs = getCode(settings, "/")
            print("/", sep=' ', end=' ', flush=True)
            codeString += codeBuffer + cs
            codeBuffer=""
            program_started=True

def codeOutput(settings,codeString,codeBuffer):
  for _c in codeString+codeBuffer:
    c=getCode(settings, _c, True)
    print(c, sep=' ', end=' ', flush=True)

def alpha2Morse(_cs: str):
  # if not keyboard.is_pressed('>'):
    event = keyboard.read_event()
    # THIS IS WHERE THE PROGRAM HALTS UNTIL AN INPUT IS PRESSED
    if event.event_type == keyboard.KEY_DOWN:# and event.name != '>':
      # print(f"event.name -> {event.name}")
      cStr=_cs
      # print(f"Key in Question -> {event.name if len(event.name)==1 else ''}")
      keyShortcuts = {
        "space" : " ",
        "backspace": "backspace"
      }
      key = keyShortcuts.get(event.name) if keyShortcuts.get(event.name) != None else (event.name if len(event.name)==1 else "")
      if(key=="backspace"): 
        res = cStr[:-1]
        print()
        return res
      # print(f"cStr-> {_cs} | key-> {key}")
      # print((_k for _k in keyShortcuts[event.name] if _k==event.name))
      # key = next((_k for _k in keyShortcuts[event.name] if _k==event.name), event.name if len(event.name)==1 else "")
      cStr += key
      return cStr

main()
