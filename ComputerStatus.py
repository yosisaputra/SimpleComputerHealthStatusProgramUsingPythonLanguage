import psutil
import math
from tkinter import *
from tkinter import messagebox
import time
import threading
from tkinter import ttk
import platform

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def getNetworkUsages(wifiVar, top):
    dictry = psutil.net_io_counters(pernic=True)
    speed = dictry.get('Wi-Fi')
    wifiVar.set('Data Usages (Wi-Fi) : {}'.format(convert_size(speed.bytes_recv)))
    top.after(500, lambda: getNetworkUsages(wifiVar, top))

def getNetSpeed(top, netSpeedVar, ul, dl, t0, up_down):
    while True:
        last_up_down = up_down
        upload = psutil.net_io_counters(pernic=True)['Wi-Fi'][0]
        download = psutil.net_io_counters(pernic=True)['Wi-Fi'][1]
        t1 = time.time()
        up_down = (upload, download)
        try:
            ul, dl = [(now - last) / (t1 - t0) / 1024.0
                      for now, last in zip(up_down, last_up_down)]
            t0 = time.time()
        except:
            pass
        if dl > 0.1 or ul >= 0.1:
            time.sleep(0.75)
            netSpeedVar.set('Down : {:0.2f} kB/s \n'.format(dl) + 'Up : {:0.2f} kB/s'.format(ul))
        else:
            netSpeedVar.set('Down : {:0.2f} kB/s \n'.format(0.00) + 'Up : {:0.2f} kB/s'.format(0.00))
        time.sleep(1)
def about():
    about = 'Author : Y Saputra Mauludin\nVersion : 1.0\nRelease : 19-01-2021\n\nDesigned and developed by\nY Saputra'
    messagebox.showinfo("About", about)
def getCpuPercent(cpuVar):
    while True:
        cpuVar.set('CPU : {}%'.format(psutil.cpu_percent(interval=1)))
        time.sleep(1)
def resize():
    top.resizable(0, 0)
    top.geometry('300x150')
    top.minsize(200, 150)
    top.maxsize(300, 150)
def getComputerHealth(cpuInfoVar):
    cpu_count = psutil.cpu_count(logical=False)
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    cpuInfoVar.set(f"CPU Count: {cpu_count}\n"
                   f"CPU Usage: {cpu_percent}%\n"
                   f"Total Memory: {convert_size(memory.total)}\n"
                   f"Used Memory: {convert_size(memory.used)}\n"
                   f"Free Memory: {convert_size(memory.free)}\n"
                   f"Disk Usage: {convert_size(disk_usage.used)} / {convert_size(disk_usage.total)}")
    if cpu_percent < 60:
        cpu_health = "Sehat"
    elif 60 <= cpu_percent < 80:
        cpu_health = "Cukup Sehat"
    else:
        cpu_health = "Tidak Sehat"
    if memory.percent < 60:
        memory_health = "Sehat"
    elif 60 <= memory.percent < 80:
        memory_health = "Cukup Sehat"
    else:
        memory_health = "Tidak Sehat"
    if disk_usage.percent < 60:
        disk_health = "Sehat"
    elif 60 <= disk_usage.percent < 80:
        disk_health = "Cukup Sehat"
    else:
        disk_health = "Tidak Sehat"
    cpuInfoVar.set(cpuInfoVar.get() + f"\n\nCPU Health: {cpu_health}\nMemory Health: {memory_health}\nDisk Health: {disk_health}")
def main():
    global top
    top = Tk()
    menubar = Menu(top)
    file = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Menu', menu=file)
    file.add_command(label='Resize', command=resize)
    file.add_command(label='About', command=about)
    file.add_command(label='Exit', command=top.destroy)
    tabControl = ttk.Notebook(top)
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)
    tabControl.add(tab1, text='  Data  ')
    tabControl.add(tab2, text='  CPU  ')
    tabControl.add(tab3, text='  Computer Health  ')
    tabControl.pack(expand=True, fill=BOTH)
    wifiVar = StringVar()
    wifilabel = ttk.Label(tab1, font=('Verdana', 10), textvariable=wifiVar)
    getNetworkUsages(wifiVar, top)
    netSpeedVar = StringVar()
    netSpeedLabel = ttk.Label(tab1, font=('Verdana', 12), textvariable=netSpeedVar)
    cpuVar = StringVar()
    cpuLabel = ttk.Label(tab2, font=('Verdana', 12), textvariable=cpuVar)
    cpuInfo = StringVar()
    cpuInfoLabel = ttk.Label(tab2, font=('Verdana', 10), textvariable=cpuInfo)
    computerHealthVar = StringVar()
    computerHealthLabel = ttk.Label(tab3, font=('Verdana', 12), textvariable=computerHealthVar)
    cpuThread = threading.Thread(target=getCpuPercent, args=(cpuVar,))
    cpuThread.daemon = True
    cpuThread.start()
    uname = platform.uname()
    cpuInfo.set(f"System: {uname.system}\n"
                f"Node Name: {uname.node}\n"
                f"Version: {uname.version}\n"
                f"Machine: {uname.machine}\n"
                f"Processor: {uname.processor}")
    ul = 0.00
    dl = 0.00
    t0 = time.time()
    upload = psutil.net_io_counters(pernic=True)['Wi-Fi'][0]
    download = psutil.net_io_counters(pernic=True)['Wi-Fi'][1]
    up_down = (upload, download)
    netSpeedThread = threading.Thread(target=getNetSpeed, args=(top, netSpeedVar, ul, dl, t0, up_down,))
    netSpeedThread.daemon = True
    netSpeedThread.start()
    computerHealthThread = threading.Thread(target=getComputerHealth, args=(computerHealthVar,))
    computerHealthThread.daemon = True
    computerHealthThread.start()

    netSpeedLabel.grid(row=0, column=0, sticky="nsew", pady=16, padx=68)
    wifilabel.grid(row=1, column=0, sticky="nsew", pady=16, padx=32)
    tab1.grid_columnconfigure(0, weight=1)  
    tab1.grid_rowconfigure(0, weight=1)    

    cpuLabel.grid(row=0, column=0, sticky="nsew", pady=6, padx=16)
    cpuInfoLabel.grid(row=1, column=0, sticky="nsew", pady=0, padx=16)
    tab2.grid_columnconfigure(0, weight=1)  
    tab2.grid_rowconfigure(0, weight=1)

    computerHealthLabel.grid(row=0, column=0, sticky="nsew", pady=6, padx=16)  # Tambahkan label di tab baru
    tab3.grid_columnconfigure(0, weight=1)  # Set widget pada kolom 0 agar meresponsif saat diresize
    tab3.grid_rowconfigure(0, weight=1)     # Set widget pada baris 0 agar meresponsif saat diresize

    top.config(menu=menubar)
    top.title('Computer Status Healty')
    top.geometry('465x250')
    top.minsize(300, 150)
    top.maxsize(500, 500)
    top.mainloop()
if __name__ == "__main__":
    main()