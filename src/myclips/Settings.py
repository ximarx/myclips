'''
Created on 22/ago/2012

@author: Francesco Capozzo
'''

class Settings(object):
    '''
    Container of settings
    '''


    def __init__(self, settings = None):
        '''
        Create a new Settings object. Settings argument can be used
        to define a dict of base settings
        '''
        
        self._settings = settings or {}
        
    def getSetting(self, aSettingKey, *args):
        '''
        Return a setting value. If the optional defaultValue
        is provided, it will be used as return value if the
        aSettingKey is missing
        
        s.getSetting(aSettingKey [, aDefaultValue])
        
        @param aSettingKey: the setting key
        @type aSettingKey: string
        @param aDefaultValue: a default value
        @type aDefaultValue: mixed
        @return: the value with key aSettingKey or default
        '''
        
        if len(args):
            return self._settings.get(aSettingKey, args[0])
        else:
            return self._settings[aSettingKey]
        
    def setSetting(self, aSettingKey, aSettingValue):
        '''
        Set or replace a value with aSettingKey key
        
        @param aSettingKey: the setting key
        @type aSettingKey: mixed
        @param aSettingValue: a value
        @type aSettingValue: mixed
        @return: this settings object
        @rtype: Settings
        '''
        self._settings[aSettingKey] = aSettingValue
        return self
        
    def delSetting(self, aSettingKey):
        '''
        Delete and return a setting with key aSettingKey (if exists)
        @param aSettingKey: a setting key
        @type aSettingKey: string
        @return: the deleted setting value
        @rtype: mixed
        '''
        return self._settings.pop(aSettingKey, None)
        
    def getKeys(self, prefix=None):
        '''
        Return a list of keys
        If prefix argument is provided, only keys
        starting with the `prefix` prefix will be
        in the list
        @param prefix: a key prefix
        @type prefix: string
        @return: a list of keys (filtered by prefix)
        @rtype: list
        '''
        if prefix is not None:
            return [x for x in self._settings.keys() if x.startswith(prefix)]
        else:
            return self._settings.keys()
        