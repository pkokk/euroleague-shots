class Shot():
    ''' 
    Constructor input
    shotid : str
    playerid : str
    xcoord : float
    ycoord : float
    action : str
    season : int
    '''
    def __init__(self,shotid,playerid,xcoord,ycoord,action,season):
        self.__shotid=shotid
        self.__playerid=playerid
        self.__action=action
        self.__season=season
        self.__x = xcoord
        self.__y = ycoord
    
    @property
    def shotid(self):
        return self.__shotid
    @property
    def playerid(self):
        return self.__playerid
    @property
    def action(self):
        return self.__action 
    @property
    def season(self):
        return self.__season
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y


    def __hash__(self):
        hash(self.shotid)

    def __eq__(self,other):
        return self.__dict__ == other.__dict__  

    


