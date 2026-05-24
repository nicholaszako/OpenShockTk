from tkinter import ttk, StringVar, IntVar


# Main view
class View:

    def __init__(self, root, api_client):
        self.api = api_client
        self.shockers = self.get_shockers()     # List of dicts
        self.shocker_names = [s['name'] for s in self.shockers]
        # tkinter variables for current selection
        self.shocker_name_v = StringVar(value=self.shocker_names[0])
        self.type_v = StringVar(value='Stop')
        self.intensity_v = IntVar(value=10)
        self.duration_v = IntVar(value=1000)    # milliseconds
        # Tracking intensity & duration to set label value on update
        self.intensity_v.trace_add('write', self.on_intensity_change)
        self.duration_v.trace_add('write', self.on_duration_change)
        # String representation of current intensity
        self.intensity_strv = StringVar(value='10')
        self.duration_strv = StringVar(value='1000')

        # Ready to load gui elements
        root.title("OpenShockTk")
        mainframe = ttk.Frame(root, padding=10)
        mainframe.grid()
        ttk.Label(mainframe, text='Options').grid(column=0, row=0)
        ttk.Combobox(mainframe, textvariable=self.shocker_name_v, 
                     values=self.shocker_names).grid(column=0, row=1)
        
        # Scales frame
        scales_frm = ttk.Frame(mainframe, padding=10)
        scales_frm.grid(column=0, row=2)
        # Intensity
        (ttk.Label(scales_frm, text='Intensity:')
            .grid(column=0, row=0, sticky="ew"))
        (ttk.Scale(scales_frm, from_=0, to=100, variable=self.intensity_v)
            .grid(column=1, row=0))
        (ttk.Label(scales_frm, textvariable=self.intensity_strv, width=4)
            .grid(column=2, row=0))
        # Duration
        (ttk.Label(scales_frm, text='Duration (ms):')
            .grid(column=0, row=1, sticky="ew"))
        (ttk.Scale(scales_frm, from_=300, to=3000, variable=self.duration_v)
            .grid(column=1, row=1))
        (ttk.Label(scales_frm, textvariable=self.duration_strv, width=4)
            .grid(column=2, row=1))
        
        # Type frame
        type_frm = ttk.Frame(mainframe, padding=10)
        type_frm.grid(column=0, row=3)
        ttk.Radiobutton(type_frm, text='Stop', variable=self.type_v, 
                        value='Stop').grid(column=0, row=0, padx=5)
        ttk.Radiobutton(type_frm, text='Shock', variable=self.type_v, 
                        value='Shock').grid(column=1, row=0, padx=5)
        ttk.Radiobutton(type_frm, text='Vibrate', variable=self.type_v, 
                        value='Vibrate').grid(column=2, row=0, padx=5)
        
        # Footer frame
        footer_frm=ttk.Frame(mainframe, padding=10)
        footer_frm.grid(column=0, row=4)
        (ttk.Button(footer_frm, text='Send', command=self.send)
            .grid(column=0, row=0, sticky='e'))
        (ttk.Button(footer_frm, text='Quit', command=root.destroy)
            .grid(column=1, row=0, sticky='w'))

    def on_intensity_change(self, var, index, mode):
        intensity_str = str(self.intensity_v.get())
        self.intensity_strv.set(intensity_str)

    def on_duration_change(self, var, index, mode):
        duration_str = str(self.duration_v.get())
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

