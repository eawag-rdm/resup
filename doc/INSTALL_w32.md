---
fontfamily: libertine
papersize: A4
fontsize: 12pt
documentclass: scrartcl
geometry: margin=2cm, bottom=3cm
numbersections: false
urlcolor: blue
header-includes:
- \usepackage{mathabx}
---
\begin{small}
hvw/2016-09-16
\end{small}
\vspace{1.5cm}

\textbf{\large resup: Installation instructions for Windows}

### 1. Install the latest Python 2.7 if you don't have it yet:

(you need local admin rights on your machine)

1. [download Python 2.7.12 for Windows](https://www.python.org/ftp/python/2.7.12/python-2.7.12.msi)
2. Double click, follow instructions,  and select "Add python.exe to Path" when asked for customizations:

![](./installer_w32.png)\


### 2. Install *resup* from GitHub:

1. Open a Powershell window:

![](./powershell.png)\


2. Type:    
    `pip install --user git+https://github.com/eawag-rdm/resup.git`
    Note: You can paste text from the clipboard into the Powershell window by **right-clicking** into the window.
3. Close Powershell and open it again (complaints about that to \texttt{\small custserv@microsoft.com})

### 3. Provide your CKAN API key

1. Point your webbrowser at the Eawag Research Data Platform, log in, and click on your name (top right).
2. Copy your API key (left sidebar, bottom) to the clipboard (Ctrl-C)
3. Type (and paste) into the Powershell window:    
    `setx CKAN_APIKEY xxxxxxxxxxxxxxxxxxxxxxxx`    
    ( 'xxxxxxxxxxxxxxxxxxxxxxxx' is your key)
4. Close Powershell and open it again (complaints about that to \texttt{\small custserv@microsoft.com})

### 4. Check the installation

Type:\
`resup -h`

You should get a help text. Note that `resup` has sub-commands,
the help of which can be accessed as, e.g.,\
`resup put -h`

Type:\
`resup list`

The output should be a list of the packages to which you have write access.


\vspace{1cm}
**Please notify me \<harald.vonwaldow@eawag.ch\> about problems with these instructions, about any bugs you discover, and about features you would like to see implemeted.**

\vspace{1cm}

\hrule

