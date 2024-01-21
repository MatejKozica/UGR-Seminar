#include "NimBLEDevice.h"
#include "WiFi.h"
#include "HTTPClient.h"

int CONNECTED = 00;
int CONNECTION_FAILED = 01;
int ALREADY_CONNECTED = 02;
std::vector<std::string> values;      
NimBLEService *pService;
std::string characteristic_uuid = "aac111b6-9d28-4785-98b4-d6c872de03d5";


int postData(std::string value) {
  HTTPClient http;

  // Specify the URL of the API endpoint
  http.begin("http://192.168.123.233:8000/connect");
  http.setAuthorization("admin", "changeme");

  String payload = "{\"value\": \"" + String(value.c_str()) + "\"}";

  Serial.println(payload);
  // Send GET request
  int httpResponseCode = http.POST(payload);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response Code: ");
    Serial.println(httpResponseCode);

    // Read the response
    String content = http.getString();
    Serial.print("Response content:");
    Serial.println(content);
  } else {
    Serial.print("HTTP Request failed. Error code: ");
    Serial.println(httpResponseCode);
  }

  // Close connection
  http.end();

  return httpResponseCode;
};

class DataCallbacks : public NimBLECharacteristicCallbacks {
  void onWrite(NimBLECharacteristic *pCharacteristic) {
    std::string value = pCharacteristic->getValue();
    values.push_back(value);
  }
  void onRead(NimBLECharacteristic *pCharacteristic) {
    Serial.println(pCharacteristic->getValue().c_str());
  }
};

void connectToWifi(void) {
  const char *ssid = "Galaxy";
  const char *password = "ae310gyrz1";
  
  // start connecting
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi");
  }
  
  Serial.println("Connected to WiFi: " + String(ssid));
}

void initiateBLEServer(void) {
  NimBLEDevice::init("NimBLE");

  NimBLEServer *pServer = NimBLEDevice::createServer();
  pService = pServer->createService(characteristic_uuid);

  // Create a writable characteristic
  NimBLECharacteristic *serviceCharacteristic = pService->createCharacteristic(
      characteristic_uuid,
      NIMBLE_PROPERTY::WRITE | NIMBLE_PROPERTY::READ
  );
  
  serviceCharacteristic->setCallbacks(new DataCallbacks());
  
  pService->start();
    
  NimBLEAdvertising *pAdvertising = NimBLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(pService->getUUID());
  pAdvertising->start();

  Serial.println("Bluetooth server started");
}

void setup(void) {
  Serial.begin(115200);

  connectToWifi();
  initiateBLEServer();
}

void loop() {
  for (int i = 0; i < values.size(); i++) {
    postData(values[i]);
    NimBLECharacteristic *charact = pService->getCharacteristic(characteristic_uuid);
    charact->setValue(CONNECTED);
    values.erase(values.begin() + i);
  }
  delay(2000);
}

