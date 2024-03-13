![current project diagram](https://github.com/tbkfi-project/Metropolia-2024Q1-Ohjelmisto1_Projekti/blob/main/diagram.png?raw=true)

### Kuvaus
Metropolia: Tieto- ja viestintätekniikan tutkinto-ohjelma, Ohjelmisto 1 -kurssin projekti.

### Ryhmä D
Tuomo Björk (tuomo.bjork@metropolia.fi) \
Aaro Jylhämäki (aaro.jylhamaki@metropolia.fi) \
Tuuli Lappalainen (tuuli.lappalainen@metropolia.fi) \
Noel Kokkonen (noel.kokkonen@metropolia.fi)

### Ajanseuranta ja kommunikaatio
[Ajanseuranta](https://docs.google.com/spreadsheets/d/1zNquF4rOppIsuHlkpdzrMcSmvQwr92FnjMw9hFcxoVU/edit?usp=sharing) \
[Discord](https://discord.com/channels/1207577718405857341/1207577718875623468)

### Projektin diagrammi
[Tallenne](https://drive.google.com/file/d/1tCwMWWl60WpciHbuS6r8Tt5wGIWZu9MJ/view?usp=sharing) 

- Pääsy vaatii kirjautumisen `metropolian sähköpostilla`.
- Kirjautumisen jälkeen saat tiedoston auki valitsemalla `Avaa sovelluksessa draw.io`.

### Ohjelman jatkokehitys ja käyttö

- Clone/lataa lähdekoodi laitteelle ja valmistele kehitysympäristösi.
- Riippuvaisuudet voit asentaa suorittamalla `setup.sh` (bash), joka luo virtuaalisen python ympäristön (`/.venv`) projektin pääkansioon. Tai yleisesti suorittamalla: `pip install -r requirements.txt`, lähdekoodin root-kansiossa.
- Määrittele ympäristömuuttujasi `config`-kansiossa olevalla `.env.template`:lla. Kopio tiedosto ja nimeä kopio uudelleen: `.env`, ja määrittele sen sisällä olevat muuttujat omaan ympäristöösi sopiviksi.
- Ohjelma käynnistyy `main.py`-tiedoston kautta.


- Saat tietokannasta kopion ajamalla `source '\path\to\ryhma_d_flight_game.sql\file'` MySQL Clientissa. 'ryhma_d_flight_game.sql'-tiedosto löytyy projektin 'root'-folderista. 
- Vaihtoehtoisesti voit myös kopioida ja ajaa 'ryhma_d_flight_game.sql'-tiedoston sisällön HeidiSQL-sovelluksen 'Query'-osiossa.
- Halutessasi vaihtaa tietokannan nimeä, voit tehdä sen muokkaamalla 'ryhma_d_flight_game.sql'-tiedoston 'CREATE DATABASE'-kohtaa, ennen ajoa HeidiSQL-sovelluksessa.