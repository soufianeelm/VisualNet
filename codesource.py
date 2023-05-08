import tkinter

#Fonction permettant de mettre chaque ligne du fichier à lire dans le tableau trame
def lire_trame(fichier):
    trame = fichier.readlines()
    return trame

#Fonction permettant de lire un octet dans une trame à une adresse donnée.
def lire_octet(trame, adresse, passage):
    global limite, new                                           #Indice de lecture de ligne dans la trame.
    line = trame[limite].lower().split('   ')                    #Extraction de la ligne courante en séparant de l'offset et des caractères ascii
    offset = int(line[0], 16)                                    #Extraction de l'offset.
    line = line[1].split()                                       #On extrait la ligne d'octets
    lastadr_on_line = offset + len(line)-1                       #Calcul de l'adresse du dernier octet.
    if passage:                                                  #si on souhaite autoriser le saut à la ligne (dans le cas où on ne lit qu'un seul octet sans suivre l'ordre de lecture, on n'autorise pas le passage à la prochaine ligne)
        if limite == len(trame)-1 :                              #Si toutes les trames ont été parcourues.
            if adresse == lastadr_on_line :                      #Si le dernier octet de la dernière ligne de la dernière trame sur la trace a été lu.
                limite += 1                                      #Limite = len(trame), important pour la condition de fin du programme.
                new = 0                                          #passage de new à 0 indiquant que nous avons fini de lire une trame
        else :
            if adresse == lastadr_on_line:                       #Si le dernier octet d'une ligne (exceptée la dernière ligne) a été atteint.
                if len(trame[limite+1].strip(' ')) != 1:         #Si ce n'est pas la fin de la trame
                    limite += 1                                  #On passe à la prochaine ligne.
                elif len(trame[limite+1].strip(' ')) == 1:       #Si le dernier octet de la dernière ligne a été lu.
                    limite += 2                                  #on passe à la prochaine trame
                    new = 0                                      #passage de new à 0 indiquant que nous avons fini de lire une trame
    return line[adresse - offset]                                #On retourne l'octet à l'adresse entrée en paramètre.

#Fonction permettant de lire les octets de l'adresse 1 à l'adresse 2 dans la trame courante.
def lire_ligne(trame, adr1, adr2):
    ligne = []
    for i in range(adr2-adr1+1):
        ligne.append(lire_octet(trame, i+adr1, 1)) #On récupère la ligne par octet par octet en appelant la fonction lire_octet
    return ligne

#fonction permettant d'ignorer la trame en cours de lecture
def ignorer_trame(trame):
    global limite
    while limite < len(trame) and len(trame[limite-1].strip(' ')) != 1 : #tant que nous avons ni atteint la fin de la trace ni atteint la fin de la trame en court
        limite += 1                                                      #on incrémente limite pour passer à la prochaine ligne
    return 0

#fonction permettant de calculer puis retourner l'adresse du dernier octet de la trame en corus de lecture
def last_adr(trame):
    i = limite                                               
    adr = 0
    while i < len(trame) - 1:                              #tant que nous avons pas atteint la fin de la trace
        if len(trame[i+1].strip(' ')) == 1:                #si la prochaine ligne ne contient qu'une tabulation et éventuellement des espaces, celà indique la fin de la trame
            line = trame[i].lower().split('   ')           #on extrait la dernière ligne de la trame en cours de lecture en séparant les octets des offsets et des caractères ascii
            adr = int(line[0],16)                          #on extrait l'offset de cette ligne
            line = line[1].split()                         #on extrait les octets présents sur cette ligne
            adr += len(line) - 1                           #on calcul l'adresse du dernière octet présent dans la liste
            return adr
        i+=1                        
    if i < len(trame):                                     #si nous avons atteint la fin de la trace nous faisons le même processus
        line = trame[i].lower().split('   ')
        adr = int(line[0],16)
        line = line[1].split()
        adr += len(line) - 1
    return adr

#fonction permettant de décoder le filtre en entrée et donner en sortie un identifiant spécifique à ce dernier, sous la forme d'un entier entre 0 (pas de filtre) et 17 pour le filtre 17 (des exemples des filtres sont donnés)
def filtrage():
    global filtre
    filtre = entree_filtre.get()                          #on extrait la chaine de caractère correspondant au filtre en entrée                         
    if len(filtre) > 0:                                   #on vérifie la présence d'un filtre ou non
        filtre = filtre.split(' ')                        #on liste chaque mot de la phrase en filtre
        if len(filtre) == 1 : # filtre 1 = [0.0.0.0]  / filtre 2 = [tcp]  / filtre 3 = [http]
            if filtre[0].lower() == "tcp" :
                return 2
            elif filtre[0].lower() == "http" :
                return 3
            elif filtre[0] == "" :
                return 0
            return 1
        elif len(filtre) == 3 : # filtre 4 = [0.0.0.0, and, 0.0.0.0]  / filtre 5 = [0.0.0.0, and, tcp]  / filtre 6 = [0.0.0.0, and, http]  / filtre 7 = [ip.src, ==, 0.0.0.0]  / filtre 8 = [ip.dst, ==, 0.0.0.0] 
            if filtre[1].lower() == "and" :
                if filtre[2].lower() == "tcp" :
                    return 5
                elif filtre[2].lower() == "http" :
                    return 6
                return 4
            else :
                if filtre[0].lower() == "ip.src" :
                    return 7
                return 8
        elif len(filtre) == 5 : # filtre 9 = [ip.src, ==, 0.0.0.0, and, tcp]  / filtre 10 = [ip.src, ==, 0.0.0.0, and, http]  / filtre 11 = [ip.dst, ==, 0.0.0.0, and, tcp]  / filtre 12 = [ip.dst, ==, 0.0.0.0, and, http]  / filtre 13 = [0.0.0.0, and, 0.0.0.0, and, tcp]  / filtre 14 = [0.0.0.0, and, 0.0.0.0, and, http] 
            if filtre[1].lower() == "and" :
                if filtre[4].lower() == "tcp":
                    return 13
                return 14
            else:
                if filtre[0].lower() == "ip.src" :
                    if filtre[4].lower() == "tcp" :
                        return 9
                    return 10
                else :
                    if filtre[4].lower() == "tcp" :
                        return 11
                    return 12
        elif len(filtre) == 7 : # filtre 15 = [ip.src, ==, 0.0.0.0, and, ip.dst, ==, 0.0.0.0]
            return 15
        elif len(filtre) == 9 : # filtre 16 = [ip.src, ==, 0.0.0.0, and, ip.dst, ==, 0.0.0.0, and, tcp]  / filtre 17 = [ip.src, ==, 0.0.0.0, and, ip.dst, ==, 0.0.0.0, and, http]
            if filtre[8].lower() == "tcp" :
                return 16
            return 17
    return 0 

#fonction permettant de lire une trace et chercher le premier offset valide, si la fonction ne trouve pas d'offset elle indique que la trace est invalide
def is_invalide(trame):
    global limite
    while limite < len(trame) and trame[limite].split('   ')[0] != "0000": #tant que nous n'avons ni fini de lire la trace ni atteint un offset de début '0000'
        limite += 1                                                       #on passe à la prochaine ligne
    return limite == len(trame)                                           #si true alors on a lu toute la trace sans trouver de trame valide, si false alors limite est sur le premier offset valide de la trace

#Fonction permettant de récupérer les informations contenues dans une trame.
def decoder(trame):
    global ip_src, ip_dst, port_src, port_dst, comment, color, new, filtre, is_filtre, doc, limite, ptcl
    new = 1                                                               #déclaration et initialisation de new à 1 pour indiquer qu'on commence à lire une trame
    ip_src = ""
    ip_dst = ""
    port_src = ""
    port_dst = ""
    comment = ""
    doc = ""
    if last_adr(trame) < 53 : #si trame trop petite (53 = 14 + 20 + 20)
        return ignorer_trame(trame)
    en_tete_eth = lire_ligne(trame, 0, 13) #En-tête Ethernet.

    if ''.join(en_tete_eth[12:14]) == "0800" :                                                                                                         #S'il s'agit d'un protocole IP
        version = lire_octet(trame, 14, 1)                                                                                                             #On récupère la version du protocole IP.
        if version[0] == '4':                                                                                                                          #S'il s'agit d'un IPv4
            ihl = ((int(version[1], 16)-5)*4) + 33                                                                                                     #Calcul de l'adresse du dernier octet de l'en-tête en envisageant des options.
            en_tete_ip = [version] + lire_ligne(trame, 15, ihl)                                                                                        #Récupération de l'en-tête IP.

            protocol = en_tete_ip[9]                                                                                                                   #Récupération du protocole.
            if protocol == '06':                                                                                                                       #S'il s'agit du protocole TCP
                ip_src = str(int(en_tete_ip[12],16))+'.'+str(int(en_tete_ip[13],16))+'.'+str(int(en_tete_ip[14],16))+'.'+str(int(en_tete_ip[15],16))   #lecture et sauvegarde de l'ip source
                ip_dst = str(int(en_tete_ip[16],16))+'.'+str(int(en_tete_ip[17],16))+'.'+str(int(en_tete_ip[18],16))+'.'+str(int(en_tete_ip[19],16))   #lecture et sauvegarde de l'ip destination

                
                if is_filtre != 0 :                #s'il y a un filtre
                    if is_filtre in [4, 13, 14] :  #si c'est le filtre 4, 13 ou 14
                        if (filtre[0] != ip_src or filtre[2] != ip_dst) and (filtre[0] != ip_dst or filtre[2] != ip_src) :  
                            return ignorer_trame(trame)
                    elif is_filtre in [1, 5, 6] :  #si c'est le filtre 1, 5 ou 6
                        if filtre[0] != ip_src and filtre[0] != ip_dst :                                                      
                            return ignorer_trame(trame)
                    elif is_filtre in [7, 9, 10] : #si c'est le filtre 7, 9 ou 10
                        if filtre[2] != ip_src :                                                                              
                            return ignorer_trame(trame)
                    elif is_filtre in [8, 11, 12] : #si c'est le filtre 8, 11 ou 12
                        if filtre[2] != ip_dst :
                            return ignorer_trame(trame)
                    elif is_filtre in [15, 16, 17] : #si c'est le filtre 15, 16 ou 17
                        if filtre[2] != ip_src or filtre[6] != ip_dst :
                            return ignorer_trame(trame)
                    

                nb_oct_opt = (int(lire_octet(trame, ihl + 13, 0)[0],16)-5)*4        #Calcul du nombre d'octets des options TCP.
                thl = nb_oct_opt + ihl + 20                                         #Calcul de l'adresse du dernier octet de l'en-tête TCP.
                en_tete_tcp = lire_ligne(trame, ihl + 1, thl)                       #Récupération de l'en-tête TCP.
                port_src = str(int(''.join(en_tete_tcp[0:2]),16))                   #lecture et sauvegarde du port source
                port_dst = str(int(''.join(en_tete_tcp[2:4]),16))                   #lecture et sauvegarde du port destination
                if port_src == "80" or port_dst == "80":                            #si échange avec serveur web
                    if new == 1:                                                    #si nous n'avons pas fini de lire la trame, il y a donc des données http
                        if is_filtre in [2, 5, 9, 11, 13, 16]:                      #S'il y'a un filtre sur le protocole TCP
                            return ignorer_trame(trame)
                        color = "#CCCCFF"                                           #attribution d'une couleur choisie arbitrairement pour l'affichage http
                        segment_http = lire_ligne(trame, thl + 1, last_adr(trame))  #Récupération du segment HTTP
                        ptcl = "HTTP "                                            
                        i = 0
                        while i < len(segment_http):                                #parcours du segment http et conversion ascii de tout caractère rencontré n'étant pas "0d" ou "0a"
                            if i < len(segment_http)-3 and segment_http[i]+segment_http[i+1] == "0d0a" : 
                                if segment_http[i+2]+segment_http[i+3] == "0d0a":
                                    comment += " || "
                                    i+=3
                                else :
                                    comment += " || "
                                    i+=1
                            else:
                                j = 0
                                while i < len(segment_http) and segment_http[i] in ["0a","20","09"]:
                                    j = 1
                                    i += 1
                                if j == 1:
                                    comment += " "
                                else:
                                    comment += chr(int(str(segment_http[i]),16))
                            i+=1
                        
                    else:
                        if is_filtre in [3, 6, 10, 12, 14, 17] :       #S'il y'a un filtre sur le protocole HTTP
                            return ignorer_trame(trame)
                        color = "#FEFEE2"
                        ptcl = "TCP "
                        comment = str(port_src) + " -> " + str(port_dst)
                        flags = format(int(en_tete_tcp[13],16),'0>6b') #Récupération des drapeaux sous format d'octets puis conversion en binaire.
                        # URG = flags[0]
                        # ACK = flags[1]
                        # PSH = flags[2]
                        # RST = flags[3]
                        # SYN = flags[4]
                        # FIN = flags[5]
                        if flags[4]:
                            comment = comment + " [SYN]"
                        elif flags[5]:
                            comment = comment + " [FIN]"
                        elif flags[3]:
                            comment = comment + " [RST]"
                        elif flags[0]:
                            comment = comment + " [URG]"
                        elif flags[2]:
                            comment = comment + " [PSH]"
                        elif flags[1]:
                            comment = comment + " [ACK]"

                        seq = int(''.join(en_tete_tcp[4:8]), 16)
                        window = int(''.join(en_tete_tcp[14:16]), 16)
                        checksum = int(''.join(en_tete_tcp[16:18]), 16)
                        comment = comment + " Sequence number = " + str(seq)
                        if flags[1] == '1':
                            ack = int(''.join(en_tete_tcp[8:12]),16)
                            comment = comment + " Ack = " + str(ack)
                        comment = comment+" Win = "+str(window)+" Length = "+str(thl-ihl)+" Checksum = "+str(checksum)+" (not verified)" # à compléter

                        if len(en_tete_tcp) > 20: #si présence d'options tcp
                            options = en_tete_tcp[20:20+nb_oct_opt]
                            comment = comment + " Option(s) : "
                            option_table = [["01","No-Operation",0],["02","Maximum Segment Size",4],["03","WSOPT - Window Scale",3],["04","SACK Permitted",2],["05","SACK (Selective ACK)",1],["06","Echo",6],["07","Echo Reply",6],["08","TSOPT - Time Stamp Option",10],["09","Partial Order Connection Permitted",2],["0a","Partial Order Service Profile",3],["0b","CC",0],["0c","CC.NEW",0],["0d","CC.ECHO",0],["0e","TCP Alternate Checksum Request",3],["0f","TCP Alternate Checksum Data",1]] #la valeur 1 pour les options à N octets a été choisie arbitrairement
                            i = 0
                            while i < len(options) and options[i] != "00":
                                j = 0
                                while j < 15 and i < len(options):
                                    if options[i] == option_table[j][0]:
                                        comment = comment+" type (0x"+options[i]+") "+str(option_table[j][1])
                                        val = int(options[i+1],16)
                                        if option_table[j][2] != 0 and option_table[j][2] != 2:
                                            if options[i] == "08":
                                                comment = comment+" TSV = "+str(int(''.join(options[i+2:i+6]),16))+" TERV = "+str(int(''.join(options[i+6:i+10]),16))
                                            else:
                                                comment = comment+" Value = "+str(int(''.join(options[i+2:i+val]),16))
                                        i += val
                                    j += 1
                                i += 1
                    return 1
    return ignorer_trame(trame)

#fonction permettant de lancer le décodage d'une trace ainsi que de construire les widgets, et les remplir avec les informations récupérées
def analyser():
    global filtre, un, limite, new, filtre, is_filtre, color
    frame_trames = tkinter.Canvas(win2, scrollregion=(0, 0, 2000, 2000))
    frame_trames.place(x=0, y = 31, width = 1200, height = 595)
                                    
    is_filtre = filtrage() #extraction de l'identifiant de filtre
    limite = 0
    new = 0
    i = 3                  #variable de placement sur l'axe Y
    t = 0                  #variable de temps
    sis = ""               #variable de sauvegarde ip source
    sid = ""               #variable de sauvegarde ip dest
    sps = ""               #variable de sauvegarde port source
    spd = ""               #variable de sauvegarde prot dest
    res = open("resultat_"+str(un)+".txt", "w") #ouverture du fichier texte de sauvegarde avec un identifiant permettant la sauvegarde de plusieurs fichiers
    while len(trame) > limite:                  #tant que nous n'avons pas fini de lire la trace
        if is_invalide(trame):                  #si trace invalide
            color = "#E4E4E4"
            ch = "               la trace insérée est invalide"
            doc = "Erreur : la trace insérée est invalide"
            frame_erreur = tkinter.Label(win2, background = color, width=2000, height=1000)
            frame_erreur.place(x = 0, y = 30)
            label_erreur = tkinter.Label(frame_erreur, text = ch, background = color)
            label_erreur.place(x = 500, y = 400) 
            res.write(doc)
        else:                                   #décodage trame par trame
            if decoder(trame):                  #si la trame a été lue avec succès
                doc = "Trame n°"+str(t)+"        Source :                Destination :            Protocole :           Info :\n"

                doc += "                 "+ip_src+"          "+ip_dst+"          "+ptcl+"                  "+comment+"\n\n"
                if ((sis == ip_src and sid == ip_dst) and (spd == port_dst and sps == port_src)):
                    ch1 = port_src + "       ------------------->      " + port_dst
                    ch2 = "|  "+ptcl+": "+comment
                elif ((sis == ip_dst and sid == ip_src) and (spd == port_src and sps == port_dst)):
                    ch1 = port_dst + "       <-------------------      " + port_src
                    ch2 = "|  "+ptcl+": "+comment
                else:
                    sis = ip_src
                    sid = ip_dst
                    sps = port_src
                    spd = port_dst
                    ch1 = port_src + "       ------------------->      " + port_dst
                    ch2 = "|  "+ptcl+": "+comment 
                
                    frame_ip = tkinter.Frame(frame_trames, width=2000, height=30, background = "#FFFFFF")
                    frame_ip.place(x = 0, y = i)

                    label_ip = tkinter.Label(frame_ip, text =ip_src +"                                 "+ip_dst, background = "#FFFFFF", font = ("Mono Space",11,"bold"))
                    label_ip.place(x = 58, y = 2)

                    i += 30

                temps = str(t)
                res.write(doc)
                label_trame_temps = tkinter.LabelFrame(frame_trames, width = 50, background = "#CCFEE2", height=50)
                label_trame_temps.place(x = 0, y = i)
                label_temps = tkinter.Label(label_trame_temps, text = temps, background = "#CCFEE2", font = ("Mono Space",10,"bold"))
                label_temps.place(x = 12, y = 3)
                frame_trame = tkinter.Label(frame_trames, background = color, width=2000, height=2)
                frame_trame.place(x = 40, y = i)
                label_ports = tkinter.Label(frame_trame, text = ch1, background = color, font = ("Mono Space",10,"bold"))
                label_ports.place(x = 100, y = 3)   
                label_com = tkinter.Label(frame_trame, text = ch2, background = color, font = ("Mono Space",10,"bold")) 
                label_com.place(x = 400, y = 3)
                i += 35
                t += 1
            else:                            #si la trame n'a pas pu être lue
                if is_filtre == 0:           #s'il n'y a pas de filtre
                    ch1 = "               La trame n°"+str(t)+" est invalide."
                    ch2 = ""
                    doc = "Trame n°"+str(t)+" invalide\n\n"
                    color = "#FF9696"
                    temps = str(t)
                    res.write(doc)
                    label_trame_temps = tkinter.LabelFrame(frame_trames, width = 50, background = "#CCFEE2", height=50)
                    label_trame_temps.place(x = 0, y = i)
                    label_temps = tkinter.Label(label_trame_temps, text = temps, background = "#CCFEE2", font = ("Mono Space",10,"bold"))
                    label_temps.place(x = 12, y = 3)
                    frame_trame = tkinter.Label(frame_trames, background = color, width=2000, height=2)
                    frame_trame.place(x = 40, y = i)
                    label_ports = tkinter.Label(frame_trame, text = ch1, background = color, font = ("Mono Space",10,"bold"))
                    label_ports.place(x = 100, y = 3)   
                    label_com = tkinter.Label(frame_trame, text = ch2, background = color, font = ("Mono Space",10,"bold")) 
                    label_com.place(x = 400, y = 3)
                    i += 35
                    t += 1
    res.close()
    xscroll = tkinter.Scrollbar(frame_trames, orient="horizontal")
    xscroll.pack(side="bottom", fill="x")
    frame_trames.config(xscrollcommand=xscroll.set)
    xscroll.config(command=frame_trames.xview)
    

    yscroll = tkinter.Scrollbar(frame_trames, orient="vertical")
    yscroll.pack(side="right", fill="y")
    frame_trames.config(yscrollcommand=yscroll.set)
    yscroll.config(command=frame_trames.yview)
    
    un += 1

#fonction permettant de décoder la trace dont le nom a été donné, construire la deuxième interface graphique, puis de lancer le décodage de la trace
def visualiser():
    global trame, win2, entree_filtre, un

    #récupération de la trace
    fichier = open(entree.get()+".txt", "r")
    trame = lire_trame(fichier)
    un = 1
    
    #construction de la fenêtre
    win2 = tkinter.Tk()
    win2.title("Visualisateur de trafic réseau")
    win2.geometry("1200x700")
    win2.config(background = "#CDD6DC")
    win2.resizable(width = False, height = False)
    top = "          Machine A                      Machine B         | Comment                                                                                                                                "
    label_titres = tkinter.Label(win2, text = top, font = ('Arial', 16))
    label_titres.place(x = 0, y = 0)
    button_quit_bis = tkinter.Button(win2, text = " Quitter ", command = win2.destroy)
    button_quit_bis.place(x = 1100, y = 642)
    entree_filtre = tkinter.Entry(win2, width = 47, background = "#FFFFFF", foreground = "black", font = (("Arial"), 11))
    entree_filtre.place(x = 610, y = 645)
    button_search = tkinter.Button(win2, text = " Rechercher ", command = analyser)
    button_search.place(x = 1010, y = 642)
    entree_filtre.focus()
    #lancement du décodage
    analyser()
    win2.mainloop()


#instructions permettants la construction de la toute première interface

win = tkinter.Tk() #Fenêtre
win.title("Visualisateur de trafic réseau")
win.geometry("500x500")
win.config(background = "#CDD6DC")
win.resizable(width = False, height = False)
#Label: Visualisateur réseau.
img = tkinter.PhotoImage(file="logo.png")
label_img = tkinter.Label(win,image = img, background="#CDD6DC")
label_img.place(x = 0, y = 0)
#Cadre: Entrez le nom du fichier, etc.
cadre_entree = tkinter.LabelFrame(win, width = 380, height = 200, font = ("Arial", 11, "italic"), background = "#E4E4E4", labelanchor = "nw") #phrase courte
cadre_entree.place(x = 60, y = 200)
#Zone de texte
label_entree = tkinter.Label(cadre_entree, text = " Veuillez entrer le nom du fichier à analyser. ", height = 1, font = ("Arial", 10), background = "#E4E4E4")
label_entree.place(x = 30, y = 25)



#Zone d'Input
entree = tkinter.Entry(cadre_entree, width = 50, background = "#FFFFFF", foreground = "black")
entree.place(x = 35, y = 50)
#Ajout du bouton analyser
button_analyse = tkinter.Button(cadre_entree, text = " Analyser ", command = visualiser)
button_analyse.place(x = 155, y = 90)
#Ajout d'un bouton quit
button_quit = tkinter.Button(cadre_entree, text = " Quitter ", command = win.destroy)
button_quit.place(x = 250, y = 150)

entree.focus()

win.mainloop()
