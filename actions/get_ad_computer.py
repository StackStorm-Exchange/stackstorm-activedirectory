from lib import action

class GetAdComputer(action.BaseAction):
    def run(self, **kwargs):
        return self.run_ad_cmdlet("Get-ADComputer", **kwargs)
    
