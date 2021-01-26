<?php	
   $connection = mysqli_connect("localhost", "aquapi","aquapi", "AquaPiDatabase");
   // check connection
   if(mysqli_connect_errno()){
   	echo 'Failed to connect to MySQL:'. mysqli_connect_error();
   	exit();
   }
   ?>
<!DOCTYPE html>
<html lang="en-US">
   <head>
      <meta charset="UTF-8" />
      <meta name="description" content="AquaPi Web Interface" />
      <meta name="keywords" content="Raspberry Pi, Arduino, AquaPi" />
      <meta name="author" content="Sascha Kirch" />
      <meta http-equiv="refresh" content="300">
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <base href="./" />
      <title>AguaPi Web Interface: Dashboard</title>
      <script type="text/javascript" src="https://www.google.com/jsapi"></script>
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
      <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
      <script type="text/javascript">
         google.charts.load('current', {'packages':['corechart']});
           google.charts.setOnLoadCallback(drawChart_plantHumidity);
           google.charts.setOnLoadCallback(drawChart_roomHumidity);
           google.charts.setOnLoadCallback(drawChart_roomTemperature);
           google.charts.setOnLoadCallback(drawChart_waterTankLevel);
           
         function drawChart_plantHumidity() {
         
               <?php	
            $strSQL = "SELECT * FROM (SELECT * FROM SensorMeasurement ORDER BY sensorMeasurementId DESC LIMIT 1000)var1 ORDER BY sensorMeasurementId ASC";
            echo "var data_plantHumidity = google.visualization.arrayToDataTable([";
            echo"['Time','Plant Humidity'],";	
            // Execute the query
            if($result = mysqli_query($connection,$strSQL)){
            while($row = mysqli_fetch_assoc($result)){
            echo "[new Date('".$row['timeStamp']."'),".$row['plantHumidity']."],";
            }				
            
            //free result set
            mysqli_free_result($result);
            } else {
            echo 'Could not run query: ' . mysqli_error();
            exit();
            }
            echo"]);";
            ?>
             
             var options_plantHumidity = {
               title: 'Plant Humidity',
	       width:'99%',
	       animation: {
	       startup: true,
	       duration: 3000,
	       easing: 'out',
	       },
	       legend:{
	       position: 'none'
	       },
	       colors: ['#3c8dbc']
             };
         var chart_plantHumidity = new google.visualization.AreaChart(document.getElementById('Chart_plantHumidity'));
         
         chart_plantHumidity.draw(data_plantHumidity, options_plantHumidity);
           }
           
         function drawChart_roomHumidity() {
         
               <?php	
            $strSQL = "SELECT * FROM (SELECT * FROM SensorMeasurement ORDER BY sensorMeasurementId DESC LIMIT 1000)var1 ORDER BY sensorMeasurementId ASC";
            echo "var data_roomHumidity = google.visualization.arrayToDataTable([";
            echo"['Time','Room Humidity'],";	
            // Execute the query
            if($result = mysqli_query($connection,$strSQL)){
            
            while($row = mysqli_fetch_assoc($result)){
            echo "[new Date('".$row['timeStamp']."'),".$row['roomHumidity']."],";
            }
            
            //free result set
            mysqli_free_result($result);
            } else {
            echo 'Could not run query: ' . mysqli_error();
            exit();
            }
            echo"]);";
            
            ?>
             
         
         var options_roomHumidity = {
               title: 'Room Humidity [%]',
	       width:'99%',
	       animation: {
	       startup: true,
	       duration: 3000,
	       easing: 'out',
	       },
	       legend:{
	       position: 'none'
	       },
	       colors: ['#3c8dbc']
             };
         var chart_roomHumidity = new google.visualization.AreaChart(document.getElementById('Chart_roomHumidity'));
             
         chart_roomHumidity.draw(data_roomHumidity, options_roomHumidity);
           }
           
           function drawChart_roomTemperature() {
         
               <?php	
            $strSQL = "SELECT * FROM (SELECT * FROM SensorMeasurement ORDER BY sensorMeasurementId DESC LIMIT 1000)var1 ORDER BY sensorMeasurementId ASC";
            echo "var data_roomTemperature = google.visualization.arrayToDataTable([";
            echo"['Time','Room Temperature'],";	
            // Execute the query
            if($result = mysqli_query($connection,$strSQL)){
            
            while($row = mysqli_fetch_assoc($result)){
            echo "[new Date('".$row['timeStamp']."'),".$row['roomTemperature']."],";
            }
            
            //free result set
            mysqli_free_result($result);
            } else {
            echo 'Could not run query: ' . mysqli_error();
            exit();
            }
            echo"]);";
            
            ?>
             
         
         var options_roomTemperature = {
               title: 'Room Temperature [°C]',
	       width:'99%',
	       animation: {
	       startup: true,
	       duration: 3000,
	       easing: 'out',
	       },
	       legend:{
	       position: 'none'
	       },
	       colors: ['#3c8dbc']
             };
         var chart_roomTemperature = new google.visualization.AreaChart(document.getElementById('Chart_roomTemperature'));
             
         chart_roomTemperature.draw(data_roomTemperature, options_roomTemperature);
           }
           
           function drawChart_waterTankLevel() {
         
               <?php	
            $strSQL = "SELECT * FROM (SELECT * FROM SensorMeasurement ORDER BY sensorMeasurementId DESC LIMIT 1000)var1 ORDER BY sensorMeasurementId ASC";
            echo "var data_waterTankLevel = google.visualization.arrayToDataTable([";
            echo"['Time','Water Tank Level'],";	
            // Execute the query
            if($result = mysqli_query($connection,$strSQL)){
            
            while($row = mysqli_fetch_assoc($result)){
            echo "[new Date('".$row['timeStamp']."'),".$row['waterTankLevel']."],";
            }
            
            //free result set
            mysqli_free_result($result);
            } 
	    else {
            echo 'Could not run query: ' . mysqli_error();
            exit();
            }
            echo"]);";
            
            ?>
             
         var options_waterTankLevel = {
               title: 'Watertank Level',
	       width:'99%',
	       animation: {
	       startup: true,
	       duration: 3000,
	       easing: 'out',
	       },
	       legend:{
	       position: 'none'
	       },
	       colors: ['#3c8dbc']
             };
         var chart_waterTankLevel = new google.visualization.AreaChart(document.getElementById('Chart_waterTankLevel'));
             
         chart_waterTankLevel.draw(data_waterTankLevel, options_waterTankLevel);
           }
         
           jQuery(document).ready(function(){
            jQuery(window).resize(function(){
             drawChart_plantHumidity();
             drawChart_roomHumidity();
             drawChart_roomTemperature();
             drawChart_waterTankLevel();
            });
           });
      </script>
      <link rel="stylesheet" href="styleSheets/styles.css" />
   </head>
   <body>
      <div class="logo">
         <a href="Dashboard.php"><img src="Logo.png" alt="Logo"></a>
      </div>
      <nav>
         <!--a class="logo">AquaPi</a-->
         <ul>
            <li><a href="Help_controller.php">Help</a></li>
            <li><a href="Tables_sensorMeasurements.php">Tables</a></li>
            <li><a class="active" href="Dashboard.php">Dashboard</a></li>
         </ul>
      </nav>
      <div class="main">
         <div id="Chart_plantHumidity" class="chartGraph"></div>
         <div id="Chart_roomHumidity" class="chartGraph"></div>
         <div id="Chart_roomTemperature" class="chartGraph"></div>
         <div id="Chart_waterTankLevel" class="chartGraph"></div>
      </div>
      <footer>
         <span><b>Mail:</b> <a href="mailto:skirch1@alumno.uned.es">skirch1@alumno.uned.es</a></span>
         <span><b>Creator:</b> "Sascha Kirch"</span>
         <span><b>AquaPi Version:</b> "v1.0"</span>
      </footer>
   </body>
</html>
