# -*- coding: utf-8 -*-
"""A package to make it easier to go from data analysis to a web delivarable with plots and results. Experimental.

author: Hans Melberg
"""
__version__ = "0.0.1"

import io
import time
import random

import matplotlib.pyplot as plt
import pandas as pd
#import boto3
import requests
import tabulate


#%%
def random_name(tstr=False):
  letter=list('abcdefghijklmnopqrstuvw')
  number=list('0123456789')
  now=str(time.time())
  rstr=[]
  for x in range(12):
    r = random.choice(letter+number)
    rstr.append(r)
  if tstr:
    rstr="".join(rstr)+now
  else:
    rstr="".join(rstr)
  return rstr

#%%
def _dropdown_plots_gui(names, gui=None, text=None):
       
    # makes sets of possible dict values
    length=len(names[0])
    
    def extract_items(lst, pos):
        its = [item[pos] for item in lst]
        its=list(set(its))
    
        return its
    
    items=[extract_items(names, pos) for pos in range(length)]
    
    # if a gui is specified, extract the names for the different dict positions
    # example "Select country {country} and gender {gender} and variable of interest {outcome}"
    # will collect country, gender , outcome
    
    def extract_var(text):
        before, after = text.split('{', maxsplit=1)
        name, rest = after.split('}', maxsplit=1)
        return name, rest
    text=gui
    
    if gui:
        cols=[]
        while '{' in text:
            rest, col=extract_var(text)
            cols.append(col)
            text=rest
    else:
        cols=[f'var_{n}' for n in range(length)]
        gcols=[f'{{var_{n}}}' for n in range(length)]
        gui = " ".join(gcols)
        
    
    
    item={}
    for n, col in enumerate(cols):
        item[col]=items[n]
    return gui, items

#%%


class Presentation():
    def __init__(self, key=None, name=None):
        self.pid=random_name()+'_draft'
        self.name=name
        self.cards={}
        self.slides=[]
        self.plots={}
        self.data={}
        self.url=None
        self.options={'allow_comments':True}
        if key is None:
            key=random_name()+'_no_name'
        self.key=key
        
        #comments can be no (no comments allowed), list of emails (users allowed to comment), all (!)reistered users 

    def save(self, name, description=None, comment=None):
        self.name=name
        cards=list(self.cards.values())

        presentation={'pid':self.pid, 
                      'name':self.name, 
                      'description':description, 
                      'cards':cards,
                      'options': self.options,
                      'key':self.key}
        r = requests.post('https://results.link/_/api/save', json=presentation, 
        headers={'Content-Type': 'application/json'})
    
        pid=self.pid
        
        for name, plot in self.plots.items():    
            url=f"https://results.link/_/api/save_plot/{name}/{pid}"
            res = requests.post(url=url, data=plot,
                    headers={'Content-Type': 'image/png'})
            #print(res.text)
        self.url= f"https://results.link#{pid}"
        return self.url

    def add(self):
        return self
    
    def _fixargs(self, args, skip=None):
        if args['name'] is None:
            name=random_name()
        else:
            name=args['name']
        
        args['name']=name
        
        if skip is None:
            skip=' self '
        else:
            skip =skip + ' self '
   
        args={k: v for k, v in args.items() if v is not None if k not in skip.split()}
            #print('returned', name, args)
        return name, args

    def code(self, code=None, language='python', name=None, title=None, 
             only_output=True, edit=True, layout=None):
        name, args=self._fixargs(locals())
        self.cards[name]=("code", args) 
            
    def df(self, df, name=None, title=None, 
               index=True, beautify=True, tabulate_kwargs=None,**kwargs):
        name, args=self._fixargs(locals(), skip="df beautify index")

        if beautify:
            df.columns=df.columns.str.replace('_','').str.title()
        if tabulate_kwargs is not None:
            markdown=df.to_markdown(index=index, **tabulate_kwargs)
        else:
            markdown=df.to_markdown(index=index)
        args.update({"markdown":markdown})
        self.cards[name]=('markdown_df', args)
        

    def dropdown_plots(self, plots, name=None, title=None, text=None, 
                            gui=None, **kwargs):
        """
        Transforms a dictionary of plots to interactive dropdown page of plots

        plots: a dictionary of plots where the key is a tuple and the value is a pandas plot

        example:
        a dictionary of plots generated in the following format:
        plots[('norway', 'female', 'income')]=df.query("country=='norway' & gender=='female').[income].plot()
        
        """
        name, args=self._fixargs(locals())
        
        # add plots to list of plots and keep track of the different possible categories 
        names=[]
        
        for name, plot in plots.items():
            plot_name=",".join(name)
            self.plot(name=plot_name, plot=plot, add_card=False)
            names.append(name)
        
        gui, items = _dropdown_plots_gui(names=names, gui=gui, text=text)

        self.cards[name]=('dropdown_plots', args)
    
    def headline(self, text, name=None, **kwargs):
        name, args=self._fixargs(locals())
        self.cards[name]=("headline", args)
        
    def html(self, html, name=None, title=None, **kwargs):
        name, args=self._fixargs(locals())
        self.cards[name]=("html", args)
        
    def image(self, source, name=None, title=None):
        name, args=self._fixargs(locals())
        self.cards[name]=("image", args)
    
    def interactive(self, code=None, name=None, title=None, layout=None, location='left',
                              widgets=None):
        name, args=self._fixargs(locals())
        self.cards[name]=("interactive", args)
    
    def line(self, name=None):
        name, args=self._fixargs(locals())
        self.cards[name]=("line", args)
    
    # def latex(self, latex, name=None)
        #https://latex.js.org/usage.html#webcomponent
        #name, args=self._fixargs(locals())
        #self.cards[name]=("latex", args)
    
    def layout(self, location, name=None):
        name, args=self._fixargs(locals())
        self.cards[name]=("layout", args)
        
    def new_page(self, name=None, title=None, **kwargs):
        name, args=self._fixargs(locals())
        self.cards[name]=("new_page", args)
        
    def no_page_break(self, name=None, **kwargs):
        name, args=self._fixargs(locals())
        self.cards[name]=("no_page_break", args)
        
    def plot(self, plot=None, name=None, title=None, add_card=True, **kwargs):
        name, args=self._fixargs(locals(), skip="plot add_card")
        f=self._capture_plot(plot=plot)
        self.plots[name]=f
        
        if add_card:
            self.cards[name]=('plot', args)
    
    def speak(self, text, language='english', name=None, title=None, **kwargs):
        name, args=self._fixargs(locals())
        self.cards[name]=("speak", args)
        
    def text(self, text, name=None, title=None, animation=None, speak=None, **kwargs):
        """
        adds a text card. markdown is allowed.
        if name is specified, will overwrite existing card with same name
        (prevent addition of many identical cards when the script is executed multiple times)
        """
        name, args=self._fixargs(locals())
        self.cards[name]=("text", args)
        
    def _capture_plot(self, plot):
        f = io.BytesIO()
        if plot is None:
            fig = plt.gcf()
            fig.savefig(f, format = "png", dpi=200, bbox_inches='tight')
        else:
            fig = getattr(plot[0], 'get_figure')()
            fig.savefig(f, format = "png", dpi=200, bbox_inches='tight')
        f.seek(0)
        return f


    def publish(name, user_name=None, api_key=None, share=None):
        pass