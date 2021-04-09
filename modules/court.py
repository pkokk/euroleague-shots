from bokeh.models import Circle, Rect, Arc,Plot,LinearAxis,Grid,Range1d,ColumnDataSource
from bokeh.plotting import figure

class Court():
    def __init__(self,lcolor='black',**kwargs):
        self.p = figure(plot_width=700, plot_height=700)
        self.left, self.right, self.bottom, self.top = -800, 800, -200, 1500
        self.p.x_range=Range1d(self.left, self.right)
        self.p.y_range=Range1d(self.bottom, self.top)
        self.p.axis.visible = False
        self.p.grid.visible = False

        self.rectang = Rect(x="x", y="y", width="w", height="h",fill_color="fc")
        self.circle = Circle(x="x", y="y", radius = "r" ,line_color=lcolor, fill_color='white')
        self.arc = Arc(x="x", y="y", radius = "r" ,line_color=lcolor, start_angle="sa" , end_angle="ea" ,end_angle_units="grad",line_dash="ld")

        # Main court
        self.main_court = ColumnDataSource({'x': [0],'y': [621.25],'w':[1500],'h':[1400],'fc':["#f8f9f9"]})
        self.p.add_glyph(self.main_court, self.rectang)

        # Rim
        self.rim = ColumnDataSource({'x': [0],'y': [0],'r':[23]})
        self.p.add_glyph(self.rim, self.circle)

        # Backboard
        self.backboard = ColumnDataSource({'x': [0],'y': [-37.5],'w':[183],'h':[1],'fc':["#0"]})
        self.p.add_glyph(self.backboard,self.rectang)

        # The paint
        self.outer_paint = ColumnDataSource({'x': [0],'y': [211.25],'w':[490],'h':[580],'fc':["#0"]})
        self.p.add_glyph(self.outer_paint, self.rectang)

        # Free throw top arc
        self.ftt_arc = ColumnDataSource({'x': [0],'y': [502.5],'r':[180],'sa':[0],'ea':[200],'ld':["solid"]})
        self.p.add_glyph(self.ftt_arc, self.arc)

        # Free throw bottomw arc
        self.ftb_arc = ColumnDataSource({'x': [0],'y': [502.5],'r':[180],'sa':[600],'ea':[0],'ld':["dashed"]})
        self.p.add_glyph(self.ftb_arc, self.arc)

        # Corner 3pt

        self.corner_three_a = ColumnDataSource({'x': [663],'y': [72],'w':[-1],'h':[300],'fc':["#0"]})
        self.p.add_glyph(self.corner_three_a, self.rectang)

        self.corner_three_b = ColumnDataSource({'x': [-663],'y': [72],'w':[-1],'h':[300],'fc':["#0"]})
        self.p.add_glyph(self.corner_three_b, self.rectang)

        # 3pt Arc

        self.three_arc_src = ColumnDataSource({'x': [0],'y': [0],'r':[700]})
        self.three_arc = Arc(x="x", y="y", radius = "r" ,line_color=lcolor, start_angle=0.32, end_angle=2.825,direction='anticlock' )
        self.p.add_glyph(self.three_arc_src,self.three_arc)

        # Center court arc

        self.center_court = ColumnDataSource({'x': [0],'y': [1320],'r':[180],'sa':[600],'ea':[0],'ld':["solid"]})
        self.p.add_glyph(self.center_court, self.arc)

        # Restricted zone arc
        self.restricted= ColumnDataSource({'x': [0],'y': [0],'r':[125],'sa':[0],'ea':[200],'ld':["solid"]})
        self.p.add_glyph(self.restricted, self.arc)

    def draw_court(self):
        return self.p

    def get_bound_coords(self):
        '''
        Calculates the court boundary coordinates and returns dict
        '''
        return {
        "x_low" : self.main_court.data['x'][0] - self.main_court.data['w'][0]/2,
        "y_low" : -self.main_court.data['h'][0]/2 + self.main_court.data['y'][0],
        "x_up" :  self.main_court.data['x'][0] + self.main_court.data['w'][0]/2,
        "y_up" :  self.main_court.data['y'][0] + self.main_court.data['h'][0]/2
        }

    
    


