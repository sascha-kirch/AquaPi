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
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta http-equiv="refresh" content="300">
      <base href="./" />
      <title>AguaPi Web Interface: Tables</title>
      <link rel="stylesheet" href="styleSheets/styles.css" />
      <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
      <script type="text/javascript">
         google.charts.load('current', {'packages':['table']});
         google.charts.setOnLoadCallback(drawTable);
          
         function drawTable() {
            
         <?php	
            $strSQL = "SELECT * FROM (SELECT SensorMeasurement.sensorMeasurementId, SensorMeasurement.timeStamp, SensorMeasurement.plantHumidity, SensorMeasurement.roomHumidity,SensorMeasurement.roomTemperature,SensorMeasurement.watertankLevel, Client.hostName, Client.IpAdress ";
            $strSQL = $strSQL . "FROM SensorMeasurement ";
            $strSQL = $strSQL . "INNER JOIN Client ON SensorMeasurement.clientMacAdressRefference = Client.macAdress ";
            $strSQL = $strSQL . "ORDER BY SensorMeasurement.timeStamp DESC LIMIT 1000)var1 ";
            echo "var data = google.visualization.arrayToDataTable([";
            echo"['ID','Time','Plant Humidity','Room Humidity','Room Temperature','Water Tank Level','Host Name','Ip Address'],";	
            // Execute the query
            if($result = mysqli_query($connection,$strSQL)){
            	while($row = mysqli_fetch_assoc($result)){
            		echo "['".$row['sensorMeasurementId']."','".$row['timeStamp']."',".$row['plantHumidity'].",".$row['roomHumidity'].",".$row['roomTemperature'].",".$row['watertankLevel'].",'".$row['hostName']."','".$row['IpAdress']."'],";
            	}				
            	
            	//free result set
            	mysqli_free_result($result);
            } else {
            	echo 'Could not run query: ' . mysqli_error();
            	exit();
            }
            echo"]);";
            ?>
          
         var options = {
		 page:'enable',
		 pageSize:30,
		 pagingButtons:'auto',
		 showRowNumber: false, 
		 width: '100%', 
		 height: '100%'
           };
                  
           var table = new google.visualization.Table(document.getElementById('table'));
          
           table.draw(data, options);
                        }
              
      </script>
   </head>
   <body>
      <!-- Navigation bar at the top of the page-->
      <div class="logo">
         <a href="Dashboard.php"><img src="Logo.png" alt="Logo" ></a>
      </div>
      <nav>
         <ul>
            <li><a href="Help_controller.php">Help</a></li>
            <li><a class="active" href="Tables_sensorMeasurements.php">Tables</a></li>
            <li><a href="Dashboard.php">Dashboard</a></li>
         </ul>
      </nav>
      <!-- Side navigation -->
      <div class="sidenav">
         <a class="active" href="Tables_sensorMeasurements.php">Sensor Measurements</a>
         <a href="Tables_clients.php">Clients</a>
         <a href="Tables_wateringProcesses.php">Watering Processes</a>
      </div>
      <div class="main-sidenav">
         <div id="table"  class="chartGraph"></div>
      </div>
      <footer>
         <span><b>Mail:</b> <a href="mailto:skirch1@alumno.uned.es">skirch1@alumno.uned.es</a></span>
         <span><b>Creator:</b> "Sascha Kirch"</span>
         <span><b>AquaPi Version:</b> "v1.0"</span>
      </footer>
   </body>
</html>
