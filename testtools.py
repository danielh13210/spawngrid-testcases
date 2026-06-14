import sys
def fail(msg,fatal=False):
  print("[FAIL]    "+msg)
  if fatal:
    print("Tests terminated.")
    sys.exit(1)

def success(msg):
  print("[SUCCESS] "+msg)
