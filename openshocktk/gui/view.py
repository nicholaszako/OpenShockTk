from math import floor
from tkinter import ttk, StringVar, IntVar, Tk


# Main view
class View:

    def __init__(self, root: Tk, api_client, patterns=[]):
        self.root = root
        self.api = api_client
        self.patterns = patterns
        self.shockers = self.get_shockers()     # List of dicts
        self.shocker_names = [s['name'] for s in self.shockers]
        # tkinter variables for current selection
        self.shocker_name_v = StringVar(value=self.shocker_names[0])
        self.type_v = StringVar(value='Stop')
        self.intensity_v = IntVar(value=10)
        self.duration_v = IntVar(value=100)    # in tenths of seconds
        # Tracking intensity & duration to set label value on update
        self.intensity_v.trace_add('write', self.on_intensity_change)
        self.duration_v.trace_add('write', self.on_duration_change)
        # String representation of current intensity
        self.intensity_strv = StringVar(value='10')
        self.duration_strv = StringVar(value='100')

        # Ready to load gui elements
        self.root.title("OpenShockTk")
        self.root.resizable(False, False)
        main_frm = ttk.Frame(self.root)
        main_frm.grid()

        # Controller frame
        ctrl_frm = ttk.LabelFrame(main_frm, text='Controller')
        ctrl_frm.grid(column=0, row=0, padx=10, pady=5, sticky='ew')
        ttk.Combobox(ctrl_frm, textvariable=self.shocker_name_v, 
                     values=self.shocker_names).grid(column=0, row=0)
        # Scales frame
        scales_frm = ttk.Frame(ctrl_frm, padding=10)
        scales_frm.grid(column=0, row=1)
        # Intensity
        int_label_frm = ttk.Frame(scales_frm, padding=(0,2,0,0))
        int_label_frm.grid(column=0, row=0, sticky="w")
        (ttk.Label(int_label_frm, text='Intensity:')
            .grid(column=0, row=0))
        (ttk.Label(int_label_frm, textvariable=self.intensity_strv, width=5)
            .grid(column=1, row=0))
        (ttk.Scale(scales_frm, from_=0, to=100, length=180, 
                   variable=self.intensity_v).grid(column=0, row=1))
        # Duration
        dur_label_frm = ttk.Frame(scales_frm, padding=(0,2,0,0))
        dur_label_frm.grid(column=0, row=2, sticky="w")
        (ttk.Label(dur_label_frm, text='Duration (s):')
            .grid(column=0, row=0))
        (ttk.Label(dur_label_frm, textvariable=self.duration_strv, width=5)
            .grid(column=1, row=0))
        (ttk.Scale(scales_frm, from_=3, to=300, length=180, 
                   variable=self.duration_v).grid(column=0, row=3))
        # Type frame
        type_frm = ttk.Frame(ctrl_frm, padding=10)
        type_frm.grid(column=0, row=2)
        ttk.Radiobutton(type_frm, text='Stop', variable=self.type_v, 
                        value='Stop').grid(column=0, row=0, padx=5)
        ttk.Radiobutton(type_frm, text='Shock', variable=self.type_v, 
                        value='Shock').grid(column=1, row=0, padx=5)
        ttk.Radiobutton(type_frm, text='Vibrate', variable=self.type_v, 
                        value='Vibrate').grid(column=2, row=0, padx=5)
        # Send
        (ttk.Button(ctrl_frm, text='Send', command=self.send)
            .grid(column=0, row=3, pady=5))
        
        # Patterns frame
        if patterns:
            patt_frm = ttk.LabelFrame(main_frm, text='Patterns')
            patt_frm.grid(column=0, row=1, padx=10, pady=5, sticky='ew')
            self.load_patterns(patt_frm)
        
        # Footer
        footer_frm=ttk.Frame(main_frm, padding=10)
        footer_frm.grid(column=0, row=99)
        (ttk.Button(footer_frm, text='STOP ALL', command=self.stop_all)
            .grid(column=0, row=0, sticky='e'))
        (ttk.Button(footer_frm, text='Quit', command=self.root.destroy)
            .grid(column=1, row=0, sticky='w'))

    def on_intensity_change(self, var, index, mode):
        intensity_str = str(self.intensity_v.get())
        self.intensity_strv.set(intensity_str)

    def on_duration_change(self, var, index, mode):
        duration_str = str(self.duration_v.get()/10)
        self.duration_strv.set(duration_str)

    def get_shockers(self):
        sapi = self.api.shockers
        shockers = sapi.get_shockers()
        return shockers

    def send(self):
        # id is in dict that has view's currently selected name
        shocker_name = self.shocker_name_v.get()
        shocker_id = next(s['id'] for s in self.shockers 
                          if s['name'] == shocker_name) 
        type_ = self.type_v.get()
        intensity = self.intensity_v.get()
        duration = self.duration_v.get()

        c = self.api.control
        prepped = c.get_prepared_req(shocker_id, type_, intensity, duration)
        c.send(prepped)

    # Load list of patterns into view as individual buttons
    def load_patterns(self, master):
        # Using constants for size may cause scaling issues
        BUTTONS_PER_ROW = 2
        PAD_X = 2
        PAD_Y = 2
        BTN_WIDTH = 12
        for i in range(0, len(self.patterns)):
            col = i % BUTTONS_PER_ROW
            row = floor(i / BUTTONS_PER_ROW)
            p = self.patterns[i]
            p_btn = ttk.Button(master, text=p.name, command=p.start, 
                               width=BTN_WIDTH)
            p_btn.grid(column=col, row=row, padx=PAD_X, pady=PAD_Y)
        return True

    def stop_all(self):
        # Cancel patterns first so nothing proceeds the stop message
        for p in self.patterns:
            p.stop()
        c = self.api.control
        # Send stop message to all shockers
        for s in self.shockers:
            prepped = c.get_prepared_req(s['id'], 'Stop', 0, 300)
            c.send(prepped)
        return True

