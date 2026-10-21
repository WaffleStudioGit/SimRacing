/*
 * Sim racing gauge driver
 *
 * Two hobby servos: speedo + tach.
 * Serial 115200, lines:  V <speed_kmh> <rpm>\n
 * Optional:             C <max_speed> <max_rpm>\n
 *                       Z\n   (needles to zero)
 *
 * Wiring (Uno / Nano):
 *   Speed servo signal -> D9
 *   RPM   servo signal -> D10
 *   Servo V+ / GND from a separate 5V supply (common GND with Arduino)
 */

#include <Servo.h>

constexpr uint8_t SPEED_PIN = 9;
constexpr uint8_t RPM_PIN = 10;

// Mechanical travel of each needle (tune after mounting)
constexpr int SPEED_DEG_MIN = 0;
constexpr int SPEED_DEG_MAX = 180;
constexpr int RPM_DEG_MIN = 0;
constexpr int RPM_DEG_MAX = 180;

float maxSpeedKmh = 300.0f;
float maxRpm = 9000.0f;

Servo speedServo;
Servo rpmServo;

String lineBuf;

int mapClamped(float value, float vmax, int dmin, int dmax) {
  if (vmax < 1.0f) vmax = 1.0f;
  float t = value / vmax;
  if (t < 0.0f) t = 0.0f;
  if (t > 1.0f) t = 1.0f;
  return dmin + (int)((dmax - dmin) * t + 0.5f);
}

void setNeedles(float speedKmh, float rpm) {
  speedServo.write(mapClamped(speedKmh, maxSpeedKmh, SPEED_DEG_MIN, SPEED_DEG_MAX));
  rpmServo.write(mapClamped(rpm, maxRpm, RPM_DEG_MIN, RPM_DEG_MAX));
}

void handleLine(String line) {
  line.trim();
  if (line.length() == 0) return;

  char cmd = line.charAt(0);
  if (cmd == 'V' || cmd == 'v') {
    float speedKmh = 0.0f;
    float rpm = 0.0f;
    if (sscanf(line.c_str() + 1, "%f %f", &speedKmh, &rpm) == 2) {
      setNeedles(speedKmh, rpm);
    }
  } else if (cmd == 'C' || cmd == 'c') {
    float ms = 0.0f;
    float mr = 0.0f;
    if (sscanf(line.c_str() + 1, "%f %f", &ms, &mr) == 2) {
      if (ms > 1.0f) maxSpeedKmh = ms;
      if (mr > 1.0f) maxRpm = mr;
    }
  } else if (cmd == 'Z' || cmd == 'z') {
    setNeedles(0.0f, 0.0f);
  }
}

void setup() {
  Serial.begin(115200);
  speedServo.attach(SPEED_PIN);
  rpmServo.attach(RPM_PIN);
  setNeedles(0.0f, 0.0f);
  Serial.println(F("OK gauge_servos"));
}

void loop() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    if (c == '\n' || c == '\r') {
      if (lineBuf.length() > 0) {
        handleLine(lineBuf);
        lineBuf = "";
      }
    } else if (lineBuf.length() < 64) {
      lineBuf += c;
    } else {
      lineBuf = "";
    }
  }
}
