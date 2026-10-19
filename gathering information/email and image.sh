
holehe test@gmail.com # if you want to show only the used web , use --only-used
# ------h8mail
h8mail -t victim@example.com
h8mail --gen-config
h8mail -t targets.txt -c config.ini

h8mail -t targets.txt -lb /path/to/breaches/  --loose -o local_results.csv
h8mail -t targets.txt -c config.ini -o full_report.csv 

#---------for user name 
sherlock test
#-----------------------------------image--------------------
exiftool photo.jpg

exiftool -gps* -T photo.jpg # coordinates

exiftool -p 'https://maps.google.com/?q=$gpslatitude,$gpslongitude' photo.jpg

exiftool -b -ThumbnailImage photo.jpg > thumb.jpg # Extract thumbnail

strings photo.jpg | grep -i -E "gps|lat|lon|software|copyright"


