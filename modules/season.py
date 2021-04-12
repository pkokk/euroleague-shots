class Season():
    def __init__(self,season_int):
        self.season_int = season_int
    
    def __str__(self):
        return str(self.season_int)

    @property
    def season(self):
        return self.season_int
    
    def construct_team_player_dict(self,df):
        '''
        input : pandas df with all players data
        output: dict with player : team kv for particular season
        '''
        self.team_player_dict = {}
        for player in df.playerid.unique():
            _cond = (df['playerid']==player) & (df['season']==self.season_int)
            try:
                self.team_player_dict[player] = df[_cond].team.values[0]
            except:
                continue

    def retrieve_team_player_dict(self):
        return self.team_player_dict
        