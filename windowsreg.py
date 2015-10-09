import _winreg
import wmi
#import ctypes
#import _winreg

def changeIEproxy(keyName, keyValue):
	pathInReg = 'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
	pathInRegPac = 'SOFTWARE\Policies\Microsoft\Windows\CurrentVersion\Internet Settings'
	key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,pathInReg, 0, _winreg.KEY_ALL_ACCESS)
	pac = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,pathInRegPac, 0, _winreg.KEY_ALL_ACCESS)
	_winreg.SetValueEx(key, keyName, 0, _winreg.REG_SZ, keyValue)
	_winreg.SetValueEx(pac,'EnableLegacyAutoProxyFeatures', 0, _winreg.REG_DWORD, 0x00000001)
	_winreg.CloseKey(key)
	_winreg.CloseKey(pac)
if __name__ == "__main__":
        try:
            #kill_ie()
            pacPath = 'file://d:/OpenGFW/OpenGFW.pac'
            changeIEproxy('AutoConfigURL', pacPath)
            print 'done, open ie'
        except Exception, e:
            print e
            print 'config.ini is created, modify config.ini and try again'
