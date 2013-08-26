RouletteScrollEffect
===================

This is a subclass of `kivy.effects.ScrollEffect` that simulates the 
motion of a roulette, or a notched wheel (think Wheel of Fortune). It is
primarily designed for emulating the effect of the iOS and android date pickers.

Usage
-----

Here's an example of using `RouletteScrollEffect` for a 
`kivy.uix.scrollview.ScrollView` 

    if __name__ == '__main__':
        # example modified from the scrollview example
    
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.button import Button
        from kivy.uix.scrollview import ScrollView
    
        # preparing a gridlayout inside a scrollview
        layout = GridLayout(cols=1, padding=10,
                size_hint=(None, None), width=500)
    
        layout.bind(minimum_height=layout.setter('height'))
    
        for i in range(30):
            btn = Button(text=str(i), size=(480, 40),
                         size_hint=(None, None))
            layout.add_widget(btn)
    
        root = ScrollView(size_hint=(None, None), size=(500, 320),
                pos_hint={'center_x' .5}
                , do_scroll_x=False)
        root.add_widget(layout)
        
        # preparation complete. Now add the new scroll effect!
        root.effect_y = RouletteScrollEffect(anchor=20, interval=40)

        runTouchApp(root)
        
Here the `ScrollView` scrolls through a series of buttons with height
40. We then attached a `RouletteScrollEffect` with interval 40, 
corresponding to the button heights. This allows the scrolling to stop at
the same offset no matter where it stops. The `RouletteScrollEffect.anchor`
adjusts this offset. 

Other settings that can be played with include 
`RouletteScrollEffect.pull_duration`, 
`RouletteScrollEffect.coasting_alpha`,
`RouletteScrollEffect.pull_back_velocity`, and
`RouletteScrollEffect.terminal_velocity`. See their module documentations
for details.