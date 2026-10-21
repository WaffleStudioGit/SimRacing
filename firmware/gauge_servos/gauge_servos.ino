/*
 * Sim dash: speed/RPM servos + 10-LED shift light + cabin controls
 *
 * PC → Arduino (115200):
 *   V <speed_kmh> <rpm>
 *   C <max_speed> <max_rpm>
 *   Z
 *
 * Arduino → PC (on change / ~20 Hz):
 *   I <engine> <headlights> <btn1> <btn2> <btn3>   // 0 or 1 each
 *
 * Wiring (Uno):
 *   Speed servo D9, RPM servo D10  (own 5V supply, common GND)
 *   LED bar anode → D2..D8, D11, D12, D13  (cathode → 220Ω → GND)
 *     order: G G G G  Y Y Y  R R R
 *   Engine key (toggle)  A0 → switch → GND   (INPUT_PULLUP)
 *   Headlights rocker    A1 → switch → GND
 *   Pushbuttons 1..3     A2 A3 A4 → button → GND
 */

#include <Servo.h>

constexpr uint8_t SPEED_PIN = 9;
constexpr uint8_t RPM_PIN = 10;

constexpr uint8_t LED_PINS[10] = {2, 3, 4, 5, 6, 7, 8, 11, 12, 13};
constexpr uint8_t NUM_LEDS = 10;

constexpr uint8_t PIN_ENGINE = A0;
constexpr uint8_t PIN_LIGHTS = A1;
constexpr uint8_t PIN_BTN1 = A2;
constexpr uint8_t PIN_BTN2 = A3;
constexpr uint8_t PIN_BTN3 = A4;

constexpr int SPEED_DEG_MIN = 0;
constexpr int SPEED_DEG_MAX = 180;
constexpr int RPM_DEG_MIN = 0;
constexpr int RPM_DEG_MAX = 180;

// Shift light: first LED at this fraction of redline, full bar at 1.0
constexpr float LED_START_FRAC = 0.55f;
constexpr float LED_FLASH_FRAC = 0.97f;

float maxSpeedKmh = 300.0f;
float maxRpm = 9000.0f;
float lastSpeed = 0.0f;
float lastRpm = 0.0f;

Servo speedServo;
Servo rpmServo;
String lineBuf;

uint8_t prevEngine = 0xFF;
uint8_t prevLights = 0xFF;
uint8_t prevBtn1 = 0xFF;
uint8_t prevBtn2 = 0xFF;
uint8_t prevBtn3 = 0xFF;
unsigned long lastInputMs = 0;
unsigned long lastBlinkMs = 0;
bool blinkOn = true;

int mapClamped(float value, float vmax, int dmin, int dmax) {
  if (vmax < 1.0f) vmax = 1.0f;
  float t = value / vmax;
  if (t < 0.0f) t = 0.0f;
  if (t > 1.0f) t = 1.0f;
  return dmin + (int)((dmax - dmin) * t + 0.5f);
}

uint8_t readActiveLow(uint8_t pin) {
  return digitalRead(pin) == LOW ? 1 : 0;
}

void setAllLeds(bool on) {
  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    digitalWrite(LED_PINS[i], on ? HIGH : LOW);
  }
}

void updateShiftLights(float rpm, bool engineOn) {
  if (!engineOn) {
    setAllLeds(false);
    return;
  }

  float frac = 0.0f;
  if (maxRpm > 1.0f) frac = rpm / maxRpm;
  if (frac < 0.0f) frac = 0.0f;
  if (frac > 1.0f) frac = 1.0f;

  if (frac >= LED_FLASH_FRAC) {
    unsigned long now = millis();
    if (now - lastBlinkMs >= 80) {
      lastBlinkMs = now;
      blinkOn = !blinkOn;
    }
    setAllLeds(blinkOn);
    return;
  }

  int lit = 0;
  if (frac > LED_START_FRAC) {
    float span = 1.0f - LED_START_FRAC;
    if (span < 0.01f) span = 0.01f;
    lit = (int)(((frac - LED_START_FRAC) / span) * NUM_LEDS + 0.0001f);
    if (lit < 0) lit = 0;
    if (lit > NUM_LEDS) lit = NUM_LEDS;
  }

  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    digitalWrite(LED_PINS[i], (i < lit) ? HIGH : LOW);
  }
}

void setOutputs(float speedKmh, float rpm, bool engineOn) {
  lastSpeed = speedKmh;
  lastRpm = rpm;
  if (!engineOn) {
    speedServo.write(SPEED_DEG_MIN);
    rpmServo.write(RPM_DEG_MIN);
    setAllLeds(false);
    return;
  }
  speedServo.write(mapClamped(speedKmh, maxSpeedKmh, SPEED_DEG_MIN, SPEED_DEG_MAX));
  rpmServo.write(mapClamped(rpm, maxRpm, RPM_DEG_MIN, RPM_DEG_MAX));
  updateShiftLights(rpm, true);
}

void reportInputs(bool force) {
  uint8_t engine = readActiveLow(PIN_ENGINE);
  uint8_t lights = readActiveLow(PIN_LIGHTS);
  uint8_t b1 = readActiveLow(PIN_BTN1);
  uint8_t b2 = readActiveLow(PIN_BTN2);
  uint8_t b3 = readActiveLow(PIN_BTN3);

  bool changed = force ||
      engine != prevEngine || lights != prevLights ||
      b1 != prevBtn1 || b2 != prevBtn2 || b3 != prevBtn3;

  unsigned long now = millis();
  if (!changed && (now - lastInputMs) < 50) return;

  // Engine key edge: refresh gauges/LEDs immediately
  if (engine != prevEngine && prevEngine != 0xFF) {
    setOutputs(lastSpeed, lastRpm, engine != 0);
  }

  prevEngine = engine;
  prevLights = lights;
  prevBtn1 = b1;
  prevBtn2 = b2;
  prevBtn3 = b3;
  lastInputMs = now;

  Serial.print(F("I "));
  Serial.print(engine);
  Serial.print(' ');
  Serial.print(lights);
  Serial.print(' ');
  Serial.print(b1);
  Serial.print(' ');
  Serial.print(b2);
  Serial.print(' ');
  Serial.println(b3);
}

void handleLine(String line) {
  line.trim();
  if (line.length() == 0) return;

  char cmd = line.charAt(0);
  bool engineOn = readActiveLow(PIN_ENGINE) != 0;

  if (cmd == 'V' || cmd == 'v') {
    float speedKmh = 0.0f;
    float rpm = 0.0f;
    if (sscanf(line.c_str() + 1, "%f %f", &speedKmh, &rpm) == 2) {
      setOutputs(speedKmh, rpm, engineOn);
    }
  } else if (cmd == 'C' || cmd == 'c') {
    float ms = 0.0f;
    float mr = 0.0f;
    if (sscanf(line.c_str() + 1, "%f %f", &ms, &mr) == 2) {
      if (ms > 1.0f) maxSpeedKmh = ms;
      if (mr > 1.0f) maxRpm = mr;
      setOutputs(lastSpeed, lastRpm, engineOn);
    }
  } else if (cmd == 'Z' || cmd == 'z') {
    setOutputs(0.0f, 0.0f, engineOn);
  }
}

void setup() {
  Serial.begin(115200);

  for (uint8_t i = 0; i < NUM_LEDS; i++) {
    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW);
  }

  pinMode(PIN_ENGINE, INPUT_PULLUP);
  pinMode(PIN_LIGHTS, INPUT_PULLUP);
  pinMode(PIN_BTN1, INPUT_PULLUP);
  pinMode(PIN_BTN2, INPUT_PULLUP);
  pinMode(PIN_BTN3, INPUT_PULLUP);

  speedServo.attach(SPEED_PIN);
  rpmServo.attach(RPM_PIN);
  setOutputs(0.0f, 0.0f, readActiveLow(PIN_ENGINE) != 0);

  Serial.println(F("OK gauge_servos"));
  reportInputs(true);
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

  // Keep redline blink alive between telemetry frames
  if (readActiveLow(PIN_ENGINE) && lastRpm / maxRpm >= LED_FLASH_FRAC) {
    updateShiftLights(lastRpm, true);
  }

  reportInputs(false);
}
