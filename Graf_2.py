import math
from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line

class Bezie(Widget):
    
    def calculate_bezier_point(self, t, points):
        n = len(points)
        if n == 1:
            return points[0]
        new_points = []
        for i in range(n - 1):
            x = (1-t) * points[i][0] + t * points[i+1][0]
            y = (1-t) * points[i][1] + t * points[i+1][1]
            new_points.append((x, y))
        return self.calculate_bezier_point(t, new_points)
    
    def generate_curve(self, points, num_points=100):
        curve_points = []
        for i in range(num_points + 1):
            t = i / num_points
            point = self.calculate_bezier_point(t, points)
            curve_points.append(point[0])
            curve_points.append(point[1])
        return curve_points
    
    def draw(self, cord_point):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Line(points=self.generate_curve(cord_point), width=1)
    
class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.circles = []
        self.dragging_circle = None
        self.circle_coords = []
        self.circle_labels = []
        self.line = []
    
    def get_cord(self):
        return self.circle_coords
    
    def on_touch_down(self, touch):
        def distant(circle, x, y):
            circle_x = circle.pos[0] + circle.size[0] / 2
            circle_y = circle.pos[1] + circle.size[1] / 2
            return math.sqrt((x - circle_x)**2 + (y - circle_y)**2)
        
        if touch.button == 'left':   
            for i, circle in enumerate(self.circles):
                distance = distant(circle, touch.x, touch.y)
                if distance <= circle.size[0] / 2:
                    self.dragging_circle = circle
                    self.dragging_circle.pos = (touch.x-7, touch.y-7)
                    self.circle_coords[i] = (round(touch.x), round(touch.y))
                    self.circle_labels[i].pos = (touch.x-45, touch.y-35)
                    break
            else:
                with self.canvas:
                    self.color = Color(0, 1, 0, 1)
                    circle = Ellipse(pos=(touch.x-7, touch.y-7), size=(14, 14))
                    self.circles.append(circle)
                    self.circle_coords.append((round(touch.x), round(touch.y)))
                    if len(self.circle_coords) > 1:
                        Color(1, 0, 0, 1)
                        self.line.append(Line(points = [self.circle_coords[len(self.circles)-2], self.circle_coords[len(self.circles)-1]], width=1))
                    # print(self.circle_coords)
                    label = Label(text=str(len(self.circles)), pos=(touch.x-45, touch.y-35), font_size=10)
                    self.circle_labels.append(label)
                    self.add_widget(label)
                    # print(self.circle_labels)
                    
        elif touch.button == 'right':
            for i, circle in enumerate(self.circles):
                distance = distant(circle, touch.x, touch.y)
                if distance <= circle.size[0] / 2:
                    self.canvas.remove(circle)
                    del self.circles[i]
                    del self.circle_coords[i]
                    
                    if len(self.circles) == 0:
                        pass
                    else:
                        if i == 0:
                            self.canvas.remove(self.line[i])
                            del self.line[i]
                        else:
                            self.canvas.remove(self.line[i-1])
                            del self.line[i-1]
                            if len(self.circles) > i:
                                self.canvas.remove(self.line[i-1])
                                del self.line[i-1]
                                with self.canvas:
                                    Color(1, 0, 0, 1)
                                    self.line.insert(i-1, Line(points = [self.circle_coords[i-1], self.circle_coords[i]], width=1))
                    
                    self.circle_labels[i].color = (0,0,0,0)
                    self.remove_widget(self.circle_labels[i])
                    del self.circle_labels[i]
                    for j in range(i, len(self.circle_labels)):
                        self.circle_labels[j].text = str(j + 1)
                    break

    def on_touch_move(self, touch):
        if self.dragging_circle:
            self.dragging_circle.pos = (touch.x-7, touch.y-7)
        for i, circle in enumerate(self.circles):
            if circle == self.dragging_circle:
                self.circle_coords[i] = (round(touch.x), round(touch.y))
                self.circle_labels[i].pos = (touch.x-45, touch.y-35)
                
                if len(self.circles) == 1:
                    pass
                elif i == len(self.circles)-1:
                    self.line[i-1].points = ([self.circle_coords[i-1], self.circle_coords[i]])
                elif i == 0:
                    self.line[i].points = ([self.circle_coords[i], self.circle_coords[i+1]])
                else:
                    self.line[i].points = ([self.circle_coords[i], self.circle_coords[i+1]])
                    self.line[i-1].points = ([self.circle_coords[i-1], self.circle_coords[i]])
                break

    def on_touch_up(self, touch):
        self.dragging_circle = None

class MainApp(App):
    def build(self):
        parent = Widget()
        
        but_start = Button(text= 'Start', pos= (30, 30), size= (60, 40), background_color= 'lime')
        but_start.bind(on_press = self.start)
        self.point = MyWidget()
        self.line = Bezie()
        parent.add_widget(self.point)
        parent.add_widget(but_start)
        parent.add_widget(self.line)
        return parent
    
    def start(self, event):
        a = self.point.get_cord()
        if len(a) > 0:
            self.line.draw(a)
        
if __name__ == '__main__':
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    MainApp().run()