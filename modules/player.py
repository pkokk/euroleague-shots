class Player():
    ''' 
    Consructor input
    playerid : str
    name : string
    '''
    def __init__(self,playerid,name):
        self.playerid=playerid
        self.name=name 
    
    def __eq__(self,other):
        return self.__dict__ == other.__dict__  


#NOTE
# I will instantiate players from [team]_players.json, so that I get team per season  
    
