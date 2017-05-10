from lib import action

class NewAdComputer(action.BaseAction):
    def run(self, **kwargs):
        return self.run_ad_cmdlet("New-ADComputer", kwargs)
    
