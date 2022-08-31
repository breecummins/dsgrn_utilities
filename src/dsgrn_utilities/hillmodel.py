# The MIT License (MIT)

# Copyright (c) 2016 Breschine Cummins

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# -----
# This file has been modified from its original version.
# It contains changes to the parsing routines for use with the DSGRN project.
# Michael Lan, Shaun Harker, 2016
# -----

import re,json
import sqlite3
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
"""
import matplotlib
font = {'family' : 'normal',
        'size'   : 22}
matplotlib.rc('font', **font)
"""


class hillmodel(object):
  '''
  This class takes a network file, a parameter, and a Hill
  exponent and builds a Hill function model. The class has two public
  methods:
  1) time,timeseries = hillmodel.simulateHillModel(initialconditions,initialtime,finaltime,timestep)
  2) hillmodel.plotResults(times,timeseries)
  The first method generates a time series for a given set of initial conditions,
  and the second method plots the results. 
  '''
  def __init__(self,network_spec_file_or_string,parameter_spec_file_or_dict,hillexp,old_format=True):
    '''
    Construct the Hill model for a given network and parameter sample.
    Inputs:
       network_file_or_string -- either (a) the filename of a network specification file (.txt file) or DSGRN database (.db file)
                                     or (b) the network spec string (identified as such if it contains a newline character)
       parameter_file_or_dict -- either (a) parameter specification filename
                                     or (b) the dictionary object describing the parameter choice
       hillexp -- Hill function exponent to use in the model
       old_format -- True: Using Shaun's formatting U[A,B], False: Using Marcio's formatting U[A->B]
    Note:
      The format of the parameter specification file is that it contains in JSON format 
      for a dictionary object giving a key-value mapping from parameters to numbers, e.g.
      { "L[X, Y]" : 2.34848, "U[X, Y]" : 1.23888, ... }
    '''
    eqnstr, self.varnames, self.varindex = self._parseEqns(network_spec_file_or_string)
    if isinstance(parameter_spec_file_or_dict, dict):
      parameter = parameter_spec_file_or_dict
    else:
      parameter = json.load(open(parameter_spec_file_or_dict))
    self.eqns=self._makeHillEqns(eqnstr,parameter,hillexp,old_format)
    self.d=len(eqnstr)

  def dim(self):
    """
    Return number of variables in model
    """
    return self.d

  def network(self):
    """
    Return the associated network specification string
    """
    return self.network_spec_string

  def simulateHillModel(self,initialconditions,initialtime,finaltime,timestep):
    '''
    Simulate the constructed Hill model for a given set of initial conditions 
    and time period. The given time step only specifies which output timeseries
    is returned. The time step for the backwards difference ODE solver is 
    determined by the algorithm.

    '''
    def RHS(t,x,eqns):
      return eqns(x) #np.array(eqns(x))
    def integrate(r,y0,t0,t1,dt):
      times=[t0]
      timeseries=[y0]
      while r.successful() and r.t < t1:
        r.integrate(r.t+dt)
        times.append(r.t)
        timeseries.append(r.y)
      return times,timeseries
    r = ode(RHS).set_integrator('vode', method='bdf')
    r.set_initial_value(initialconditions,initialtime).set_f_params(self.eqns)
    times,timeseries = integrate(r,initialconditions,initialtime,finaltime,timestep)
    return times,timeseries,self.varnames

  def plotResults(self,times,timeseries,plotoptions={},legendoptions={},figuresize=(),labeloptions = {},axisoptions={},savename=None,skipindex=None,show=False):
    '''
    Plot a time series.

    plotoptions, legendoptions, and labeloptions are optional dictionaries with keys corresponding 
    to the options for matplotlib.pyplot.plot and matplotlib.pyplot.legend.

    Examples: 
    plotoptions={'linewidth':2}
    legendoptions={'fontsize':24,'loc':'upper left', 'bbox_to_anchor':(1, 1)}
    figuresize = (20,10)
    labeloptions={'xlabel' : 'Time', 'ylabel' : 'Expression','fontsize' : 14}
    axisoptions={'xlim' : [0,15], 'ylim' : [0,4]}

    '''
    if figuresize:
      plt.figure(figsize=figuresize)
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    colors = colors[:3]+colors[4:]  #skip red for red/green colorblindness
    if 'fontsize' in labeloptions:
      plt.rcParams.update({'font.size': labeloptions["fontsize"]})
    if skipindex:
      # make sure that subnetwork uses same colors as in full plot
      if not isinstance(skipindex,list):
        skipindex = [skipindex]
      colors = [c for i,c in enumerate(colors) if i not in skipindex]
    plt.gca().set_prop_cycle(color = colors)
    timeseries=np.array(timeseries)
    for k in range(timeseries.shape[1]):
      plt.plot(times,timeseries[:,k],label=self.varnames[k],**plotoptions)
    plt.legend(**legendoptions)
    if 'xlabel' in labeloptions:
      plt.xlabel(labeloptions['xlabel'])
    if 'ylabel' in labeloptions:
      plt.ylabel(labeloptions['ylabel'])
    if 'xlim' in axisoptions:
      plt.xlim(axisoptions['xlim'])
    if 'ylim' in axisoptions:
      plt.ylim(axisoptions['ylim'])
    if savename:
      plt.savefig(savename, bbox_inches='tight')
    if show:
      plt.show()
    plt.close()

# The remainder of the file consists of private methods implementing various parsing voodoo.

  def _parseEqns(self,network_spec_file_or_string):
    """
    Parse a network specification file to obtain data structures representing ODEs
      Input: "network_file_or_string" is either (a) the filename of a network specification file or DSGRN database
                                             or (b) the network spec string (i.e. contents)
      Output: The function outputs 
                eqnstr, varnames, varindex 
              where
                eqnstr   is a list of strings representing the ODE in a p-n formatting (see below)
                varnames is a list of variable names, the order of which gives an internal indexing
                varindex is a dictionary with keys being the variable names and values being an internal indexing

      Note: "p-n formatting" of a network node's input formula replaces the variables occuring in 
            the string instead with the variable indices and suffixes them with either "n" or "p" 
            depending on whether they are negated. Multiplication in this formatting is always explicit 
            (never mere juxtaposition). It is easiest to describe by example:  
                      (~X + Y)(Z)  becomes ((0n)+(1p))*((2p)) when 
                      varindex["X"] == 0, varindex["Y"] == 1, and varindex["Z"] == 2
      Notes on Network specification file:
          A network spec file contains on each line 
            <varname> : <input-formula> [: E]
            (The optional last colon and what follows we may ignore.)
            An input-formula is an algebraic combination of variable names which allows the
            usage of the variables and the symbols (, ), +, and * in the usual ways. We may also
            prepend any variable name with the symbol "~". 
          We note the following:
            (a) Some variable names are contained inside of other variable names
            (b) There may be redundant whitespace (even between ~ and variable name)
            (c) We may write "X*Y" "X(Y)" "(X)Y" "X Y" which are equivalent and refer to the product, 
              but "XY" can only refer to a single variable "XY", and not the product of "X" and "Y".
    """
    if '\n' in network_spec_file_or_string:
      self.network_spec_string = network_spec_file_or_string
    elif network_spec_file_or_string.lower().endswith('.db'):
      conn = sqlite3.connect(network_spec_file_or_string)
      c = conn.cursor()
      c . execute ( "select Specification from Network;" )
      self.network_spec_string = c.fetchone()[0]
    else:
      with open(network_spec_file_or_string) as f:
        self.network_spec_string = f.read()
    eqns=[]
    varnames = []
    varindex = {}
    for line in self.network_spec_string.splitlines():
      parsed = line.split(':')
      if len(parsed) < 2: continue   # Ignore blank lines
      varname = parsed[0].strip() # e.g. "X"
      formula = parsed[1].strip() # e.g. "(~X + Y)U Z"
      if varname[0] == '.' or varname[0] == '@': continue  # Ignore comment lines
      varnames.append(varname)
      varindex[varname]=str(len(varindex))
      eqns.append(formula)
    eqnstr=[]
    for e in eqns:
      # Replace occurences of variables with variable indices followed by p if occurring without ~ prefix and followed by n otherwise
      # Example: "(~X + Y)U Z" --> "((0n) + (1p))(2p) (3p)"
      e = re.sub('([ ()+*]*)(~?) *([^ ~()+*]+)([ ()+*]*)', lambda x: x.group(1) + "(" + varindex[x.group(3)] + ("n" if (x.group(2) == '~') else "p") + ')' + x.group(4), e)
      # Remove spaces and make multiplications explicit
      # Example: "((0n) + (1p))(2p) (3p)" --> "((0n)+(1p))*(2p)*(3p)"
      e = e.replace(' ','').replace(')(',')*(')
      # Add parsed equation to eqnstr output list
      eqnstr.append(e)
    return eqnstr,varnames,varindex
      

  def _makeHillStrs(self,U,L,T,n,J):
    """
    Create the Hill function expressions
       neghill = "(U-L)*(T**n)/(X[J]**n+T**n) + L"
       poshill = "(U-L)*(X[J]**n)/(X[J]**n+T**n) + L"
       with the appropriate values for U, L, T, n, and J substituted
    """    
    scalar = "("+U+"-"+L+")"
    Xn = "X["+J+"]**"+n
    Tn = T+"**"+n
    denom = "("+Xn+"+"+Tn+")"
    neghill=scalar+"*"+Tn+"/"+denom+" + "+ L
    poshill=scalar+"*"+Xn+"/"+denom+" + "+ L
    return neghill,poshill

  def _makeHillEqns(self,eqnstr,parameter,n,old_format):
    """
    Construct a lambda expression evaluation the right hand side of the Hill Model ODE
    Inputs:  eqnstr          -- a list of p-n format specification of the network node inputs
             parameter       -- a dict of {parameter name : real nonzero value}
             n               -- Hill function exponent
             old_format      -- True or False, use Shaun's variable formatting or Marcio's
    Output:  eqns            -- A list of lambda functions representing the right-hand-side of an ODE
                                The length of the list is the dimension of the ODE (which is also the length of eqnstr).
                                The ODE which is represented is d/dt x[i] = eqns[i]
    Implementation:
      This task is accomplished by reading the network specification file and replacing each variable
      in the input formulas with a suitable Hill function. The parsing is facilitated by having "eqnstr"
      in the form outputted by _parseEqns, e.g. 
         eqnstr == ["((0n)+(1p)*((2p))", ... ]
      and the algebraic syntax already present in the input formula already being suitable.
      We also add a decay term for each input formula.
         - X[0] + algebraic-combination of Hill functions
    """
    expression = "["
    for k,e in enumerate(eqnstr):
      def replaceWithHillFunction(match):
        j = match.group(1)  # integer which indexes input variable
        regulation = match.group(2) # either "n" or "p"
        if not old_format:
          pair = "["+self.varnames[int(j)]+"->"+self.varnames[int(k)]+"]"
        else:
          pair = "["+self.varnames[int(j)]+", "+self.varnames[int(k)]+"]"
        U = str(parameter["U" + pair])
        L = str(parameter["L" + pair])
        T = str(parameter["T" + pair])
        neghill, poshill = self._makeHillStrs(U,L,T,str(n),str(j))
        return (poshill if regulation == 'p' else neghill)
      # Include the formula into the expression
      expression += (',' if len(expression) > 1 else '') + "-X["+str(k)+"]+" + re.sub('([0-9]*)([np])', replaceWithHillFunction, e)
    expression += ']'
    return eval('lambda X :' + expression)
