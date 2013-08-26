'''
RouletteScrollEffect
===================

This is a subclass of :class:`kivy.effects.ScrollEffect` that simulates the 
motion of a roulette, or a notched wheel (think of Wheel of Fortune). It is
primarily designed for emulating the effect of the iOS and android date pickers.

Usage
-----

'''
from kivy.animation import Animation
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.effects.scroll import ScrollEffect
from kivy.properties import NumericProperty, AliasProperty
from math import ceil, floor, exp

class RouletteScrollEffect(ScrollEffect):
    __events__ = ('on_coasted_to_stop',)
    
    drag_threshold = NumericProperty(0)
    '''overrides :attr:`ScrollEffect.drag_threshold` to abolish drag threshold.
    
    .. note::
        If using this with a :class:`Roulette` or other :class:`Tickline`
        subclasses, what matters is :attr:`Tickline.drag_threshold`, which
        is passed to this attribute in the end.
    '''
    
    min = NumericProperty(-float('inf'))
    max = NumericProperty(float('inf'))

    interval = NumericProperty(1)
    '''the interval of the values of the "roulette".'''
    
    anchor = NumericProperty(0)
    '''one of the valid stopping values.'''

    pull_duration = NumericProperty(.2)
    '''when movement slows around a stopping value, an animation is used
    to pull it toward the nearest value. :attr:`pull_duration` is the duration
    used for such an animation.'''
    
    coasting_alpha = NumericProperty(.5)
    '''When within :attr:`coasting_alpha` * :attr:`interval` of the
    next notch and velocity is below :attr:`terminal_velocity`, 
    coasting begins and will end on the next notch.'''

    pull_back_velocity = NumericProperty('50sp')
    '''the velocity below which the scroll value will be drawn to the 
    *nearest* notch instead of the *next* notch in the direction travelled.'''

    def get_term_vel(self):
        return (exp(self.friction) * self.interval * 
                self.coasting_alpha / self.pull_duration)
    def set_term_vel(self, val):
        self.pull_duration = (exp(self.friction) * self.interval * 
                              self.coasting_alpha / val)
    terminal_velocity = AliasProperty(get_term_vel, set_term_vel, 
                                      bind=['interval',
                                            'coasting_alpha',
                                            'pull_duration',
                                            'friction'],
                                      cache=True)

    def start(self, val, t=None):
        Animation.stop_all(self)
        return ScrollEffect.start(self, val, t=t)
    
    def on_notch(self, *args):
        return (self.scroll - self.anchor) % self.interval == 0
    
    def nearest_notch(self, *args):
        interval = float(self.interval)
        anchor = self.anchor
        n = round((self.scroll - anchor) / interval)
        return anchor + n * interval
    
    def next_notch(self, *args):
        interval = float(self.interval)
        anchor = self.anchor
        round_ = ceil if self.velocity > 0 else floor
        n = round_((self.scroll - anchor) / interval)
        return anchor + n * interval
        
    def near_notch(self, d=0.01):
        nearest = self.nearest_notch()
        if abs((nearest - self.scroll) / self.interval) % 1 < d:
            return nearest
        else:
            return None
        
    def near_next_notch(self, d=None):
        d = d or self.coasting_alpha
        next_ = self.next_notch()
        if abs((next_ - self.scroll) / self.interval) % 1 < d:
            return next_
        else:
            return None
        
    def update_velocity(self, dt):
        velocity = self.velocity
        t_velocity = self.terminal_velocity
        next_ = self.near_next_notch()
        pull_back_velocity = self.pull_back_velocity
        if pull_back_velocity < abs(velocity) < t_velocity and next_:
            duration = abs((next_ - self.scroll) / self.velocity)
            anim = Animation(scroll=next_, 
                             duration=duration,
                             )
            anim.on_complete = lambda *args: self._coasted_to_stop()
            anim.start(self)
            return
        if abs(velocity) < pull_back_velocity and not self.on_notch():
            anim = Animation(scroll=self.nearest_notch(), 
                             duration=self.pull_duration,
                             t='in_out_circ')
            anim.on_complete = lambda *args: self._coasted_to_stop()
            anim.start(self)
        else:
            self.velocity -= self.velocity * self.friction
            self.apply_distance(self.velocity * dt)
            self.trigger_velocity_update()
            
    def on_coasted_to_stop(self, *args):
        '''this event fires when the roulette has stopped, "making a selection".
        '''
        pass
        
    def _coasted_to_stop(self, *args):
        self.velocity = 0
        self.dispatch('on_coasted_to_stop')
        