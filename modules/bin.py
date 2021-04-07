class Bin():
    '''
    Class represents one bin of which we segment the basketball (half)court
    Constructor inputs:
    binid : int
    boundaries dict of boundaries 
    '''
    def __init__(self,binid,boundaries):
        self.x_bound_up=boundaries["x_bound_up"]
        self.y_bound_up=boundaries["y_bound_up"]
        self.x_bound_down=boundaries["x_bound_down"]
        self.y_bound_down=boundaries["y_bound_down"]
        self.__binid = binid
    
    @property
    def binid(self):
        return self.__binid

    
    def _attr_shots(self,shotlist,season):
        #Get all shots that fall in the bin for a particular season
        self.binshots = []
        for shot in shotlist:
            if shot.season == season:
               if shot.x < self.x_bound_up and shot.x >= self.x_bound_down and shot.y < self.y_bound_up and shot.y >= self.y_bound_down:
                    self.binshots.append(shot)

    def calc_tot_avg(self,shotlist,season):
        #Initialize shot counters
        _three_total_cnt = 0
        _two_total_cnt = 0
        _ft_total_cnt = 0
        _three_made_cnt = 0
        _two_made_cnt = 0
        _ft_made_cnt = 0

        self._attr_shots(shotlist,season)
        if self.binshots:
            for shot in self.binshots:
                if shot.action == '2FGA' :
                    _two_total_cnt +=1
                elif shot.action == '2FGM' :
                    _two_made_cnt += 1
                    _two_total_cnt +=1
                elif shot.action == '3FGA' :
                    _three_total_cnt += 1
                elif shot.action == '3FGM' :
                    _three_made_cnt += 1  
                    _three_total_cnt += 1                            
                elif shot.action == 'FTA' :
                    _ft_total_cnt += 1
                elif shot.action == 'FTM' :
                    _ft_made_cnt += 1
                    _ft_total_cnt  += 1 

        return {'3pct' : round(float(_three_made_cnt/_three_total_cnt),4) if _three_total_cnt > 0 else None ,
                '2pct' : round(float(_two_made_cnt/_two_total_cnt),4) if _two_total_cnt > 0 else None,
                'ftpct' : round(float(_ft_made_cnt/_ft_total_cnt),4) if _ft_total_cnt > 0 else None
                }    


    def calc_player_avg(self,playerid):
        pass


    def calculate_hextile(self):
        pass