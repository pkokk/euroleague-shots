class Player():
    ''' 
    Consructor input
    playerid : str
    name : string
    '''
    def __init__(self,playerid,name):
        self.__playerid=playerid
        self.name=name

    def __str__(self):
        return "Player(" + self.playerid + ", " + self.name + ")"

    @property
    def playerid(self):
        return self.__playerid

    def get_team(self,df,season):
        #_res = df.loc[(df['season'] == season) & (df['playerid'] == self.playerid)]
        _res = df[(df['season']== season) & (df['playerid'] == self.playerid)].iloc[0]['team']
        print(_res)

    
    def __eq__(self,other):
        return self.__dict__ == other.__dict__ 
    
