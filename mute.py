"""
Toggles Mute on Player Unknown's Battleground
"""
from pycaw.pycaw import AudioUtilities


def main():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "TslGame.exe":
        	if volume.GetMute() == 1:
        		volume.SetMute(0, None)
        	else:
        		volume.SetMute(1, None)



if __name__ == "__main__":
    main()