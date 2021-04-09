class Bin():
    '''
    Class represents one bin of which we segment the basketball (half)court
    Constructor inputs:
    binid : int
    boundaries dict of boundaries 
    '''
    def __init__(self,binid,boundaries):
        self.__x_bound_up=boundaries["x_bound_up"]
        self.__y_bound_up=boundaries["y_bound_up"]
        self.__x_bound_down=boundaries["x_bound_down"]
        self.__y_bound_down=boundaries["y_bound_down"]
        self.__binid = binid
    
    @property
    def binid(self):
        return self.__binid

    @property
    def x_bound_up(self):
        return self.__x_bound_up

    @property
    def y_bound_up(self):
        return self.__y_bound_up

    @property
    def x_bound_down(self):
        return self.__x_bound_down
        
    @property
    def y_bound_down(self):
        return self.__y_bound_down


    def _attr_shots(self,shotlist,season):
        #Get all shots that fall in the bin for a particular season
        self.binshots = []
        for shot in shotlist:
            if shot.season == season:
                if shot.x < self.x_bound_up and shot.x >= self.x_bound_down and shot.y < self.y_bound_up and shot.y >= self.y_bound_down:
                    self.binshots.append(shot)


    def calc_shots(self,shotlist,season,players):
        self.__player_shot_dict = {}
        self.__shot_dict = {}
        _three_total_cnt = 0
        _two_total_cnt = 0
        _ft_total_cnt = 0
        _three_made_cnt = 0
        _two_made_cnt = 0
        _ft_made_cnt = 0

        self._attr_shots(shotlist,season)
        if self.binshots:
            for player in players:
                #Initialize shot counters
                _player_three_total_cnt = 0
                _player_two_total_cnt = 0
                _player_ft_total_cnt = 0
                _player_three_made_cnt = 0
                _player_two_made_cnt = 0
                _player_ft_made_cnt = 0
                _player_three_x = 0
                _player_three_y = 0
                _player_two_x = 0
                _player_two_y = 0
                for shot in self.binshots:                
                    if shot.playerid == player.playerid:
                        if shot.action == '2FGA' :
                            _player_two_total_cnt +=1
                            _player_two_x +=shot.x
                            _player_two_y +=shot.y
                            _two_total_cnt +=1
                        elif shot.action == '2FGM' :
                            _player_two_made_cnt += 1
                            _player_two_total_cnt +=1
                            _two_made_cnt += 1
                            _two_total_cnt +=1                            
                        elif shot.action == '3FGA' :
                            _player_three_total_cnt += 1
                            _three_total_cnt += 1
                            _player_three_x +=shot.x
                            _player_three_y +=shot.y                            
                        elif shot.action == '3FGM' :
                            _player_three_made_cnt += 1  
                            _player_three_total_cnt += 1      
                            _three_made_cnt += 1  
                            _three_total_cnt += 1                                                    
                        elif shot.action == 'FTA' :
                            _player_ft_total_cnt += 1
                            _ft_total_cnt += 1
                        elif shot.action == 'FTM' :
                            _player_ft_made_cnt += 1
                            _player_ft_total_cnt  += 1 
                            _ft_made_cnt += 1
                            _ft_total_cnt  += 1 

                

                self.__player_shot_dict[player.playerid] = {
                    '2p' : _player_two_total_cnt,
                    '3p' : _player_three_total_cnt,
                    'ft' : _player_ft_total_cnt,
                    '3pct' : round(float(_player_three_made_cnt/_player_three_total_cnt),4) if _player_three_total_cnt > 0 else None ,
                    '2pct' : round(float(_player_two_made_cnt/_player_two_total_cnt),4) if _player_two_total_cnt > 0 else None,
                    'ftpct' : round(float(_player_ft_made_cnt/_player_ft_total_cnt),4) if _player_ft_total_cnt > 0 else None,
                    '2px' : _player_two_x/_player_two_total_cnt if _player_two_total_cnt > 0 else None ,           
                    '2py' : _player_two_y/_player_two_total_cnt  if _player_two_total_cnt > 0 else None,
                    '3px' : _player_three_x/_player_three_total_cnt if _player_three_total_cnt > 0 else None,           
                    '3py' : _player_three_y/_player_three_total_cnt if _player_three_total_cnt > 0 else None
                    } 
                
            

        self.__shot_dict = {
                    '2p' : _two_total_cnt,
                    '3p' : _three_total_cnt,
                    'ft' : _ft_total_cnt,
                    '3pct' : round(float(_three_made_cnt/_three_total_cnt),4) if _three_total_cnt > 0 else None ,
                    '2pct' : round(float(_two_made_cnt/_two_total_cnt),4) if _two_total_cnt > 0 else None,
                    'ftpct' : round(float(_ft_made_cnt/_ft_total_cnt),4) if _ft_total_cnt > 0 else None
                    }

        return self.__shot_dict,self.__player_shot_dict


    def calculate_hextile(self):
        pass