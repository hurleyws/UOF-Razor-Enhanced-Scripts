while True:
    Misc.ScriptRun("petTrainer.py")
    Misc.Pause(500)
    
    while Misc.ScriptStatus("petTrainer.py"):
        Misc.Pause(1000)
    
    Misc.Pause(8 * 60 * 1000)