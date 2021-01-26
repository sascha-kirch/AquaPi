<!DOCTYPE html>
<html lang="en-US">
   <head>
      <meta charset="UTF-8" />
      <meta name="description" content="AquaPi Web Interface" />
      <meta name="keywords" content="Raspberry Pi, Arduino, AquaPi" />
      <meta name="author" content="Sascha Kirch" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <base href="./" />
      <title>AguaPi Web Interface: Help</title>
      <link rel="stylesheet" href="styleSheets/styles.css" />
      <!--link rel="icon" href="media/favicon.ico"/-->
   </head>
   <body>
      <!-- Navigation bar at the top of the page-->
      <div class="logo">
         <a href="Dashboard.php"><img src="Logo.png" alt="Logo"></a>
      </div>
      <nav>
         <!--a class="logo">AquaPi</a-->
         <ul>
            <li><a class="active" href="Help_controller.php">Help</a></li>
            <li><a href="Tables_sensorMeasurements.php">Tables</a></li>
            <li><a  href="Dashboard.php">Dashboard</a></li>
         </ul>
      </nav>
      <!-- Side navigation -->
      <div class="sidenav">
         <a href="Help_controller.php">Controller</a>
         <a class="active" href="Help_schematic.php">Hardware Setup</a>
      </div>
      <div class="main-sidenav">
         <img class="help_img" src="schematic.png" alt="Schematic" style="width:70% ">
      </div>
      <footer>
         <span><b>Mail:</b> <a href="mailto:skirch1@alumno.uned.es">skirch1@alumno.uned.es</a></span>
         <span><b>Creator:</b> "Sascha Kirch"</span>
         <span><b>AquaPi Version:</b> "v1.0"</span>
      </footer>
   </body>
</html>
