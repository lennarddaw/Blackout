#include <WiFi.h>
#include <WiFiClient.h>
#include <HTTPClient.h>
#include "esp_camera.h"

// WLAN-Zugangsdaten
const char* ssid     = "devolo-108";
const char* password = "BKAJYQKRJAEVHEFO";

// Raspberry Pi Server-URL
const char* serverUrl = "http://192.168.2.145:5000/upload";  // passe IP hier an

// Zeit zwischen Aufnahmen (ms)
const unsigned long captureInterval = 1000;
unsigned long lastCapture = 0;

// Kamera-Pin-Definitionen (AI-Thinker ESP32-CAM)
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM     0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM       5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

void setup() {
  Serial.begin(115200);
  delay(1000);

  // WLAN verbinden
  WiFi.begin(ssid, password);
  Serial.print("Verbinde mit WLAN");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nVerbunden, IP: " + WiFi.localIP().toString());

  // Kamera konfigurieren
  camera_config_t config = {};
  config.ledc_channel    = LEDC_CHANNEL_0;
  config.ledc_timer      = LEDC_TIMER_0;
  config.pin_d0          = Y2_GPIO_NUM;
  config.pin_d1          = Y3_GPIO_NUM;
  config.pin_d2          = Y4_GPIO_NUM;
  config.pin_d3          = Y5_GPIO_NUM;
  config.pin_d4          = Y6_GPIO_NUM;
  config.pin_d5          = Y7_GPIO_NUM;
  config.pin_d6          = Y8_GPIO_NUM;
  config.pin_d7          = Y9_GPIO_NUM;
  config.pin_xclk        = XCLK_GPIO_NUM;
  config.pin_pclk        = PCLK_GPIO_NUM;
  config.pin_vsync       = VSYNC_GPIO_NUM;
  config.pin_href        = HREF_GPIO_NUM;
  config.pin_sscb_sda    = SIOD_GPIO_NUM;
  config.pin_sscb_scl    = SIOC_GPIO_NUM;
  config.pin_pwdn        = PWDN_GPIO_NUM;
  config.pin_reset       = RESET_GPIO_NUM;
  config.xclk_freq_hz    = 20000000;
  config.pixel_format    = PIXFORMAT_JPEG;

  if (psramFound()) {
    config.frame_size    = FRAMESIZE_VGA;
    config.jpeg_quality  = 10;
    config.fb_count      = 2;
  } else {
    config.frame_size    = FRAMESIZE_CIF;
    config.jpeg_quality  = 12;
    config.fb_count      = 1;
  }

  // Kamera initialisieren
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Kamera-Init fehlgeschlagen: 0x%x\n", err);
    while (true) { delay(1000); }  // Stop
  }
}

void loop() {
  unsigned long now = millis();
  if (now - lastCapture >= captureInterval) {
    lastCapture = now;

    // Frame holen
    camera_fb_t * fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Kamerabild fehlgeschlagen");
      return;
    }

    // HTTP POST
    WiFiClient client;
    HTTPClient http;
    http.begin(client, serverUrl);
    http.addHeader("Content-Type", "image/jpeg");

    int code = http.POST(fb->buf, fb->len);
    if (code > 0) {
      Serial.printf("Bild gesendet! Server antwortete: %d\n", code);
    } else {
      Serial.printf("Fehler beim Senden: %s\n", http.errorToString(code).c_str());
    }
    http.end();

    esp_camera_fb_return(fb);
  }

  delay(10);
}
