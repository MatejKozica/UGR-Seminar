#include "NimBLEDevice.h"
#include "WiFi.h"
#include "HTTPClient.h"

int CONNECTED = 00;
int CONNECTION_FAILED = 01;
int ALREADY_CONNECTED = 02;

int getData(void) {
  HTTPClient http;

  // Specify the URL of the API endpoint
  http.begin("https://api.chucknorris.io/jokes/random");

  // Send GET request
  int httpResponseCode = http.GET();

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response Code: ");
    Serial.println(httpResponseCode);

    // Read the response
    String payload = http.getString();
    Serial.print("Response payload:");
    Serial.println(payload);
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

    // client is sending username and password combination which is separated by space
    Serial.print("Value received from client: ");
    Serial.println(value.c_str());

    getData();

    // set value to characteristic so client can read it
    pCharacteristic->setValue(ALREADY_CONNECTED);
  }
  void onRead(NimBLECharacteristic *pCharacteristic) {
  }
};

void connectToWifi(void) {
  const char *ssid = "Xiaomi 12T";
  const char *password = "tometomic";
  
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
  NimBLEService *pService = pServer->createService("aac111b6-9d28-4785-98b4-d6c872de03d5");

  // Create a writable characteristic
  NimBLECharacteristic *writeCharacteristic = pService->createCharacteristic(
      "aac111b6-9d28-4785-98b4-d6c872de03d5",
      NIMBLE_PROPERTY::WRITE | NIMBLE_PROPERTY::READ
  );
  
  writeCharacteristic->setCallbacks(new DataCallbacks());
  
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
  delay(2000);
}