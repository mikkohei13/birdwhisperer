


Redbuild the image, if you change requirements.txt

  `docker build -t birdwhisperer .`

Run

  copy audio files to `/app/audio`
  run `python analyze.py filename.mp3`


# TODO

Test how Wihsper analyzes single-word audio files
Get list of species names and synonyms (mänty...) in order of abundance

Read GPX file
For loop each waypoint
Analyze audio file with whisper
Proofready with lehvenstein
Implement keywords (epävarma, radius?, count, additional info)
Generate Excel file

TODO:
- luettelo, jossa vain lajit
- poista duplikaatit
- skip audio of less than 2 seconds


12.10.2023 kokeilu
- 22 havaintoa
- 16 oikein
- 4 väärin, pahin: pihlaja -> kiitos kun katsoit -> niittynunnakoi

