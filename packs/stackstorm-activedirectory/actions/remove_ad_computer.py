from lib import action

class RemoveAdComputer(action.BaseAction):
    def run(self, **kwargs):
        return self.run_ad_cmdlet("Remove-ADComputer", kwargs)
    
