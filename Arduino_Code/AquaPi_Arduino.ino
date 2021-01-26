#include <ArduinoJson.h>
#include <DHT.h>

#define DHT_TYPE DHT11

#define WATERLEVEL_PIN_ANA 2
#define PLANTHUMIDITY_PIN_ANA 1

#define MOTORRELAIS_PIN_DIG 6
#define DHT_PIN_DIG 5

#define WATERLEVEL_PIN_VCC 3
#define DHT_PIN_VCC 4
#define MOTERRELAIS_PIN_VCC 7
#define PLANTHUMIDITY_PIN_VCC 2

float version = 1.0;
bool sensorsActive = false;
String statusString = "";

//Settings for Messages and Communication
String incomingString = ""; // for incoming serial data
const int capacitySetting = JSON_OBJECT_SIZE(2) + JSON_OBJECT_SIZE(4) + 40; //Number of Elements + String Copy Adder
StaticJsonDocument<capacitySetting> doc;
DeserializationError err;

//Sensor Values
DHT dht(DHT_PIN_DIG, DHT_TYPE);
float humidityRoom = 0.0f;
float temperatureRoom = 0.0f;
uint16_t humidityPlant = 0;//10Bit ADC. uint8_t not sufficient
uint16_t waterLevel = 0;

//Sensor Analog Value Translation
const unsigned int waterLevel_empty = 20;

//Configuration and target values
struct settings {
  unsigned int humidityPlant_target = 0;
  unsigned int motorOnTime_ms = 0;
  bool settingInitialized = false;
} ArduinoSetting;

//Serial Interface Config
const byte numChars = 128;
char receivedChars[numChars];
boolean newData = false;

namespace AquaPiMessage{
  String startDelimiter = "<";
  String endDelimiter = ">";
  
  String ACK(bool ack) {
    return startDelimiter + "{\"mst\":\"ACK\",\"ack\":\"" + ack + "\"}" + endDelimiter;
  }
  
  String STATUS(String statusId) {
    return startDelimiter + "{\"mst\":\"STS\",\"sid\":\"" + statusId + "\"}" + endDelimiter;
  }
  
  String DATA(float humidityRoom, float temperatureRoom, int humidityPlant, int waterLevel) {
    return startDelimiter +
           "{\"mst\":\"DTA\",\"val\":{\"humidityRoom\":" + String(humidityRoom) +
           ",\"temperatureRoom\":" + String(temperatureRoom) +
           ",\"humidityPlant\":" + String(humidityPlant) +
           ",\"waterLevel\":" + String(waterLevel) +
           "}}" +
           endDelimiter;
  }
}

void RevciveWithStartEndMarkers() {
  static boolean receiveInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    //Required due to bug in the implementation of the JSON Library used in the Raspberry
    if (rc == '\\')
      continue;

    if (receiveInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars) {
          ndx = numChars - 1;
        }
      }
      //Reached End Marker
      else {
        receivedChars[ndx] = '\0'; //terminates the String
        receiveInProgress = false;
        ndx = 0;
        newData = true;
      }
    }
    else if (rc == startMarker) {
      receiveInProgress = true;
    }
  }
}

void ShowNewData() {
  if (newData == true) {
    Serial.print("I Just Received: ");
    Serial.println(receivedChars);
  }
}

void SendSensorValues() {
  Serial.println(AquaPiMessage::DATA(humidityRoom, temperatureRoom, humidityPlant, waterLevel));
}

void UpdateSensorValues() {
  if (sensorsActive) {
    humidityRoom = dht.readHumidity();
    temperatureRoom = dht.readTemperature();
    waterLevel = analogRead(WATERLEVEL_PIN_ANA);
    humidityPlant = analogRead(PLANTHUMIDITY_PIN_ANA);
  }
}

String ActUponSensorValues() {
  if (humidityPlant > ArduinoSetting.humidityPlant_target && waterLevel > waterLevel_empty) {
    ActivateMotor();
    delay(ArduinoSetting.motorOnTime_ms);
    DeactivateMotor();
    return "WATERED";
  }
  else {
    return "NOT_WATERED";
  }
}

void ActivateMotor() {
  PORTD &= ~(1 << MOTORRELAIS_PIN_DIG);
}

void DeactivateMotor() {
  PORTD |= (1 << MOTORRELAIS_PIN_DIG);
}

void ActivateSensors() {
  PORTD |= ((1 << WATERLEVEL_PIN_VCC) | (1 << DHT_PIN_VCC) | (1 << MOTERRELAIS_PIN_VCC) | (1 << PLANTHUMIDITY_PIN_VCC));
  delay(1000);
  dht.begin();
  delay(1000);
  sensorsActive = true;
}

void DeactivateSensors() {
  // Ensure that Sensors are deactivated
  PORTD &= ~((1 << WATERLEVEL_PIN_VCC) | (1 << DHT_PIN_VCC) | (1 << MOTERRELAIS_PIN_VCC) | (1 << PLANTHUMIDITY_PIN_VCC));
  sensorsActive = false;
}

void Deserialize() {
  //Deserialize incomming Data
  err = deserializeJson(doc, receivedChars);

  //check for errors in the deserializer
  if (err) {
    Serial.println(AquaPiMessage::ACK(false));

  }
  else {
    String messageType = doc["mst"];

    if (messageType == "CMD") {
      String command = doc["cmd"];

      //USV = Update Sensor Values
      if (command == "USV") {
        Serial.println(AquaPiMessage::ACK(true));
        UpdateSensorValues();
      }

      //RUN = Activate Sensors
      else if (command == "RUN") {
        Serial.println(AquaPiMessage::ACK(true));
        ActivateSensors();
      }

      //RUN = Activate Sensors
      else if (command == "STO") {
        Serial.println(AquaPiMessage::ACK(true));
        DeactivateSensors();
      }

      //SSV = Send Sensor Values
      else if (command == "SSV") {
        Serial.println(AquaPiMessage::ACK(true));
        SendSensorValues();
      }

      //WON = Water On
      else if (command == "WON") {
        Serial.println(AquaPiMessage::ACK(true));
        ActivateMotor();
      }

      //WOF = Water OFF
      else if (command == "WOF") {
        Serial.println(AquaPiMessage::ACK(true));
        DeactivateMotor();
      }

      //ACT = Act upon new sensor values
      else if (command == "ACT") {
        Serial.println(AquaPiMessage::ACK(true));
        statusString = ActUponSensorValues();
      }

      //STS = Status Request
      else if (command == "STS") {
        Serial.println(AquaPiMessage::ACK(true));
        Serial.println(AquaPiMessage::STATUS(statusString));
      }

      //ALV = Alive
      else if (command == "ALV") {
        Serial.println(AquaPiMessage::ACK(true));
      }

      // Unknown command
      else {
        Serial.println(AquaPiMessage::ACK(false));
      }
    }
    //Setting Update
    else if (messageType == "STG") {
      Serial.println(AquaPiMessage::ACK(true));
      ArduinoSetting.humidityPlant_target = doc["stg"]["ph"];
      ArduinoSetting.motorOnTime_ms = doc["stg"]["mt"];
      ArduinoSetting.settingInitialized = true;
    }
    else {
      Serial.println(AquaPiMessage::ACK(false));
    }
  }
}

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect.
  }
  DDRD |= (1 << MOTORRELAIS_PIN_DIG); //Pinmode Output
  DDRD |= (1 << WATERLEVEL_PIN_VCC); //Pinmode Output
  DDRD |= (1 << DHT_PIN_VCC); //Pinmode Output
  DDRD |= (1 << MOTERRELAIS_PIN_VCC); //Pinmode Output
  DDRD |= (1 << PLANTHUMIDITY_PIN_VCC); //Pinmode Output

  // Ensure that Sensors are deactivated
  PORTD |= (1 << MOTORRELAIS_PIN_DIG); // Set Output to HIGH
  PORTD &= ~((1 << WATERLEVEL_PIN_VCC) | (1 << DHT_PIN_VCC) | (1 << MOTERRELAIS_PIN_VCC) | (1 << PLANTHUMIDITY_PIN_VCC));

  statusString = "None";
}

void loop() {
  RevciveWithStartEndMarkers();
  if (newData == true) {
    //ShowNewData();
    Deserialize();
    newData = false;
  }
}
