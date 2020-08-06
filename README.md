<h3>Setup</h3>
  a. Download the program<br>
  b. Using cmd.exe navigate to folder the program was saved in<br>
  c. Create the database using <b>recruitment_task_api.py -create</b>. <br><i>You can add a number after this command to controll how much data to download (eg. <b>recruitment_task_api.py -create 500</b> (default is 1000 entries)</i><br>
  d. After the download is compleated you can proceede to use other options<br>
<h3>Available options</h3>
  <b>'-create'</b>  add entries to database<br>
  <b>'-password-list (amount)'</b>  display most common passwords in database. Default = 5<br>
  <b>'-mtfp'</b>  display male-to-female ratio in % <br>
  <b>'-avg-age (gender)'</b>  display average age of people in database (a - all (DEFAULT) | m - male | f - female<br>
  <b>'-pop-cities (amount)'</b>  display most popular cities in database. DEFAULT = 5<br>
  <b>'-max-sec-passwd'</b>  display most secure password in database<br>
  <b>'-born (from) (to)'</b>  display all people born between two dates in YYYY-MM-DD format<br>
  <b>'-h'</b>  display all the options in cmd window
