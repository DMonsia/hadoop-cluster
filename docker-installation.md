# Installation de docker

## Installation sur Ubuntu
Ouvrez un terminal et entrez successivement les deux commandes ci-dessous. 

```
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```
Une fois l’installation terminée, il vous est recommandé d’utiliser docker sans être en mode super utilisateur. Pour faire cela, une commande vous est donnée dans les logs de l’installation.
Copiez et exécutez là.

Exemple: sudo usermod -aG docker [hostname]


## Installation sur Windows 

### Télécharger docker 
[Télécharger](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)
Puis installer.

À la fin de l’installation cliquer sur le bouton de redémarrage `close and restart` pour redémarrer l’ordinateur. 
<!-- suivez le didacticiel d'installation `docker-instllation-didacticiel.pdf` contenu dans le dossier ressources.  -->

### Ouvrir Windows `powershell` en tant que admin
- Allez dans la barre de recherche windows et entrer powershell
- Ensuite faire un clique droit sur powershell et cliquez sur l’option `ouvrir en tant qu'administrateur`

NB: Vous exécuterez toutes les commandes ci-dessous dans le terminal.

### Étape 1 : activer le sous-système Windows pour Linux
```
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

### Étape 2 - Consulter la configuration requise pour exécuter WSL 2
NB: Cette étape n’est pas nécessaire si vous avez l’habitude de faire la mise à jour de votre système d’exploitation. <br>
Vérifier le de numéro de version de build
- Maintenez les touches  `Windows + R`
- Dans le champ qui s'ouvre tapez `winver` et sélectionnez OK
Dans les informations système qui apparaîtront,
 - si la version du build est 1903 c'est ok
 - sinon faite un mise à jour de windows

### Étape 3 : activer la fonctionnalité Machine virtuelle
```
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

### Étape 4 : télécharger le package de mise à jour du noyau Linux
Cliquez [ici](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi) et installé la mise à jour une fois le téléchargement terminé. <br>

### Étape 5 : définir WSL 2 comme version par défaut
```
wsl --set-default-version 2
```

### Étape 6 : installer la distribution Linux de votre choix
```
wsl --install -d Ubuntu-20.04 
```
nom d'utilisateur: docker <br>
mot de passe: docker<br>


### Étape 7: Vérifier que docker est installé 
```
docker -v
```

### Installation de `make` sur Windows
Executez successivement les deux commandes ci-dessous.
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
```
choco install make
```

---

links:<br>
https://www.youtube.com/watch?v=hiry-gfyjv4 <br>
https://docs.docker.com/desktop/install/windows-install/ <br>
https://docs.microsoft.com/fr-fr/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package <br>
https://docs.microsoft.com/fr-fr/windows/wsl/install#upgrade-version-from-wsl-1-to-wsl-2 <br>
https://www.youtube.com/watch?v=5TavcolACQY <br>