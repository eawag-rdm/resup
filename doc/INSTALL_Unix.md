---
fontfamily: libertine
papersize: A4
fontsize: 11pt
documentclass: scrartcl
geometry: margin=2cm, bottom=3cm
numbersections: false
urlcolor: blue
header-includes:
- \usepackage{mathabx}
---
\begin{small}
hvw/2016-09-18
\end{small}
\vspace{1.5cm}

\textbf{\large resup: Installation instructions for Linux}

### 1. Install the latest Python 2.7 if you don't have it yet:

**Ask your system adminstrator to do it.**

In case you are your own system adminstrator:

1. [Download Python 2.7.12](https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tar.xz)
2. Uncompress and untar:    
    `xz -d Python-2.7.12.tar.xz && tar xvf Python-2.7.12.tar`{.bash}
3. Do the usual thing:    

	~~~bash
	 cd Python-2.7.12
	 ./configure && make
	 su
	 make install
	~~~

### 2. Install *resup* from GitHub:

1. `pip install --user git+https://github.com/eawag-rdm/resup.git`{.bash}
2. Add `$HOME/.local/bin` to your PATH if it is not already there. For `bash` users that would be:    

	```bash
	echo "export PATH=\"\${PATH}:\${HOME}/.local/bin\"" >>$HOME/.bashrc
	```

###  3. Provide your CKAN API key

1. Point your webbrowser at the Eawag Research Data Platform, log in, and click on your name (top right).    
    In case you are doing this from a machine outside the Eawag network, jump to step **5.**
2. Copy your API key (left sidebar, bottom) to the clipboard.
3. Set the environment variable CKAN_APIKEY accordingly. For bash users that would be:    
	```bash
	echo "CKAN_APIKEY=xxxxxxxxxxxxxxxxxxxxxxxxxx" >>$HOME/.bashrc
	```
	where "xxxxxxxxxxxxxxxxxxxxxxxxxx" is the API key.

### 4. Check the installation

Start a new shell or source your `.bashrc`: `. ~/.bashrc`{.bash}

Type: `resup -h`{.bash}

You should get a help text. Note that `resup`{.bash} has sub-commands,
the help of which can be accessed as, e.g.,\
`resup put -h`{.bash}

Type: `resup list`{.bash}

The output should be a list of the packages to which you have write access.

### 5. Additional steps to use  *resup* from outside the Eawag network, e.g. from servers in the ETH network at GDC.

1. Send me your SSH public key. This is is a file with extension "`.pub`" in the directory "`~/.ssh/`", e.g. "`id_rsa.pub`". In case you don have one, create one:    
    `ssh-keygen -b 4096`{.bash}    
	and answer all subsequent questions by hitting [Return].
	My positive answer will include the IP-address of a "jumphost".

2. Set 2 environment variables:

	~~~bash
	export HTTPS_PROXY=socks5://localhost:7000
	export EAW_JUMPHOST=the_ip.address.I_sent.you
    ~~~
	(also preferably persistently in `~/.bashrc`)

3. Before using *resup*, start an SSH dynamic proxy at port 7000:    
    `ssh -Nf -D 7000 $EAW_JUMPHOST`{.bashrc}

**Note:** The above setup also allows you to use the Eawag-RDM webinterface from outside the Ewag network. Simply configure your browser to use a "SOCKS5 proxy" at `localhost:7000`.


\vspace{1cm}
**Please notify me \<harald.vonwaldow@eawag.ch\> about problems with these instructions, about any bugs you discover, and about features you would like to see implemeted.**

\vspace{1cm}

\hrule

