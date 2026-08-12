/*
 * BMS 1S Merged — Full-feature single-cell BMS with:
 *   - Electrical protection (over/under voltage, overcurrent w/ delayed trip,
 *     charge and discharge temperature limits)
 *   - Thermal state machine driving a Fresnel-heated solar block into the
 *     battery via a damper servo and PWM fan (preheat, wait, standby,
 *     overheat protect)
 *   - Predictive sunrise detection (photoresistor + 30-min stability)
 *   - PIR "jeans protection" safety shutter for the Fresnel focal spot
 *
 * Hardware (see bms/README.md for wiring/pin table and calibration):
 *   Arduino Nano/Uno (5V)
 *   INA219 current sensor (I2C, A4/A5)
 *   Battery NTC 10k @ 25C, Beta 3950, 10k divider to 5V -> A1
 *   Block NTC (same or thermocouple w/ MAX6675 for >250 C) -> A2
 *   Cell voltage 100k+10k divider -> A0
 *   Photoresistor + 10k to GND -> A3
 *   PIR sensor HC-SR501 -> D2
 *   Discharge MOSFET IRLZ44N gate -> D3
 *   Charge relay via NPN -> D4
 *   Fan MOSFET (PWM) -> D5
 *   Damper servo (SG90) -> D6
 *   Safety shutter servo -> D7
 *   Green OK LED -> D8, Red fault LED -> D9, Buzzer -> D10
 *   Blue sunrise-predicted LED -> D11
 *
 * CC0.
 */

#include <Wire.h>
#include <Adafruit_INA219.h>
#include <Servo.h>

Adafruit_INA219 ina219;

Servo damperServo;
Servo shutterServo;

// ---------- PIN DEFINITIONS ----------
const int PIN_CELL_VOLTAGE = A0;
const int PIN_BAT_NTC = A1;
const int PIN_BLOCK_NTC = A2;
const int PIN_LIGHT = A3;
const int PIN_PIR = 2;
const int PIN_DISCHG_FET = 3;
const int PIN_CHG_RELAY = 4;
const int PIN_FAN_PWM = 5;
const int PIN_DAMPER_SERVO = 6;
const int PIN_SHUTTER_SERVO = 7;
const int PIN_LED_OK = 8;
const int PIN_LED_FAULT = 9;
const int PIN_BUZZER = 10;
const int PIN_LED_SUNRISE = 11;

// ---------- ELECTRICAL BMS THRESHOLDS (LFP cell) ----------
const float CELL_OV = 3.65;
const float CELL_OV_RELEASE = 3.40;
const float CELL_UV = 2.50;
const float CELL_UV_RELEASE = 2.80;
const float CHARGE_TEMP_MIN = -10.0;
const float CHARGE_TEMP_MAX = 60.0;
const float DISCHARGE_TEMP_MIN = -40.0;
const float DISCHARGE_TEMP_MAX = 70.0;
const float OVERCURRENT_A = 2.0;
const unsigned long OVERCURRENT_DURATION_MS = 500;

// ---------- THERMAL CONTROL THRESHOLDS ----------
const float BLOCK_MIN_USEFUL = 80.0;
const float BAT_PREHEAT_TARGET = 0.0;
const float BAT_OVERHEAT = 50.0;
const float BLOCK_OVERHEAT = 300.0;
const float HYSTERESIS = 2.0;

// ---------- SUNRISE PREDICTION ----------
const float LIGHT_THRESHOLD = 30.0;
const unsigned long SUNRISE_CONFIRM_MS = 1800000UL; // 30 minutes
unsigned long lightStableSince = 0;
bool sunrisePredicted = false;

// ---------- JEANS PROTECTION ----------
bool motionDetected = false;
bool shutterClosed = false;

// ---------- CALIBRATION ----------
const float VOLTAGE_DIVIDER_RATIO = (100000.0 + 10000.0) / 10000.0;
const float ADC_VREF = 5.0;
const float ADC_RES = 1024.0;
const float NTC_SERIES_RESISTOR = 10000.0;
const float NTC_NOMINAL_RES = 10000.0;
const float NTC_NOMINAL_TEMP = 25.0;
const float NTC_BETA = 3950.0;

// ---------- STATE ----------
float cellVoltage = 0.0;
float batteryTemp = 0.0;
float blockTemp = 0.0;
float currentAmps = 0.0;
float lightPercent = 0.0;

bool chargeAllowed = true;
bool dischargeAllowed = true;
bool faultState = false;

enum ThermalState {
  STANDBY,
  PREHEAT,
  CHARGE_WAIT,
  OVERHEAT_PROTECT
};
ThermalState thermalState = STANDBY;

unsigned long overcurrentStart = 0;
bool overcurrentTripped = false;

void readSensors();
void electricalProtection();
void thermalControl();
void predictiveSunrise();
void safetyShutter();
void actuateOutputs();
void serialDebug();

void setup() {
  Serial.begin(115200);

  if (!ina219.begin()) {
    Serial.println("INA219 not found!");
    while (1);
  }
  ina219.setCalibration_16V_400mA();

  damperServo.attach(PIN_DAMPER_SERVO);
  shutterServo.attach(PIN_SHUTTER_SERVO);
  damperServo.write(0);
  shutterServo.write(0);

  pinMode(PIN_DISCHG_FET, OUTPUT);
  pinMode(PIN_CHG_RELAY, OUTPUT);
  pinMode(PIN_FAN_PWM, OUTPUT);
  pinMode(PIN_LED_OK, OUTPUT);
  pinMode(PIN_LED_FAULT, OUTPUT);
  pinMode(PIN_LED_SUNRISE, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_PIR, INPUT);

  digitalWrite(PIN_DISCHG_FET, HIGH);
  digitalWrite(PIN_CHG_RELAY, HIGH);
  digitalWrite(PIN_FAN_PWM, LOW);
  digitalWrite(PIN_LED_OK, HIGH);
  digitalWrite(PIN_LED_FAULT, LOW);
  digitalWrite(PIN_LED_SUNRISE, LOW);
  digitalWrite(PIN_BUZZER, LOW);

  Serial.println("BMS+Thermal started. Jeans protection active.");
}

void loop() {
  readSensors();
  electricalProtection();
  thermalControl();
  predictiveSunrise();
  safetyShutter();
  actuateOutputs();
  serialDebug();
  delay(500);
}

void readSensors() {
  int raw = analogRead(PIN_CELL_VOLTAGE);
  float voltageInput = raw * ADC_VREF / ADC_RES;
  cellVoltage = voltageInput * VOLTAGE_DIVIDER_RATIO;

  raw = analogRead(PIN_BAT_NTC);
  float resistance = NTC_SERIES_RESISTOR * (ADC_RES / raw - 1.0);
  float steinhart = log(resistance / NTC_NOMINAL_RES) / NTC_BETA + 1.0 / (NTC_NOMINAL_TEMP + 273.15);
  batteryTemp = 1.0 / steinhart - 273.15;

  raw = analogRead(PIN_BLOCK_NTC);
  resistance = NTC_SERIES_RESISTOR * (ADC_RES / raw - 1.0);
  steinhart = log(resistance / NTC_NOMINAL_RES) / NTC_BETA + 1.0 / (NTC_NOMINAL_TEMP + 273.15);
  blockTemp = 1.0 / steinhart - 273.15;

  currentAmps = ina219.getCurrent_mA() / 1000.0;

  raw = analogRead(PIN_LIGHT);
  lightPercent = (raw / ADC_RES) * 100.0;

  motionDetected = (digitalRead(PIN_PIR) == HIGH);
}

void electricalProtection() {
  if (abs(currentAmps) > OVERCURRENT_A) {
    if (!overcurrentTripped) {
      if (overcurrentStart == 0) {
        overcurrentStart = millis();
      } else if (millis() - overcurrentStart > OVERCURRENT_DURATION_MS) {
        overcurrentTripped = true;
      }
    }
  } else {
    overcurrentStart = 0;
    overcurrentTripped = false;
  }

  if (cellVoltage > CELL_OV) chargeAllowed = false;
  if (cellVoltage < CELL_OV_RELEASE) chargeAllowed = true;

  if (cellVoltage < CELL_UV) dischargeAllowed = false;
  if (cellVoltage > CELL_UV_RELEASE) dischargeAllowed = true;

  if (batteryTemp < CHARGE_TEMP_MIN || batteryTemp > CHARGE_TEMP_MAX) {
    chargeAllowed = false;
  } else if (cellVoltage < CELL_OV_RELEASE) {
    chargeAllowed = true;
  }

  if (batteryTemp < DISCHARGE_TEMP_MIN || batteryTemp > DISCHARGE_TEMP_MAX) {
    dischargeAllowed = false;
  } else if (cellVoltage > CELL_UV_RELEASE && !overcurrentTripped) {
    dischargeAllowed = true;
  }

  if (overcurrentTripped) {
    chargeAllowed = false;
    dischargeAllowed = false;
  }

  faultState = (!chargeAllowed || !dischargeAllowed || overcurrentTripped);
}

void thermalControl() {
  switch (thermalState) {
    case STANDBY:
      if (batteryTemp < BAT_PREHEAT_TARGET && blockTemp > BLOCK_MIN_USEFUL + HYSTERESIS) {
        thermalState = PREHEAT;
      }
      if (batteryTemp > BAT_OVERHEAT) thermalState = OVERHEAT_PROTECT;
      break;

    case PREHEAT:
      if (batteryTemp > BAT_PREHEAT_TARGET || blockTemp < BLOCK_MIN_USEFUL - HYSTERESIS) {
        thermalState = STANDBY;
      }
      if (batteryTemp < BAT_PREHEAT_TARGET && blockTemp < BLOCK_MIN_USEFUL) {
        thermalState = CHARGE_WAIT;
      }
      if (batteryTemp > BAT_OVERHEAT) thermalState = OVERHEAT_PROTECT;
      break;

    case CHARGE_WAIT:
      if (blockTemp > BLOCK_MIN_USEFUL + HYSTERESIS && batteryTemp < BAT_PREHEAT_TARGET) {
        thermalState = PREHEAT;
      }
      if (batteryTemp > BAT_PREHEAT_TARGET) thermalState = STANDBY;
      if (batteryTemp > BAT_OVERHEAT) thermalState = OVERHEAT_PROTECT;
      break;

    case OVERHEAT_PROTECT:
      if (batteryTemp < BAT_OVERHEAT - 5.0) thermalState = STANDBY;
      break;
  }
}

void predictiveSunrise() {
  if (lightPercent > LIGHT_THRESHOLD) {
    if (lightStableSince == 0) {
      lightStableSince = millis();
    } else if (millis() - lightStableSince > SUNRISE_CONFIRM_MS && !sunrisePredicted) {
      sunrisePredicted = true;
      Serial.println("SUNRISE PREDICTED: Block should be hot soon.");
    }
  } else {
    lightStableSince = 0;
    sunrisePredicted = false;
  }
  digitalWrite(PIN_LED_SUNRISE, sunrisePredicted ? HIGH : LOW);
}

void safetyShutter() {
  if (motionDetected) {
    if (!shutterClosed) {
      shutterServo.write(90);
      shutterClosed = true;
      Serial.println("MOTION DETECTED! Shutter closed. Remember the jeans.");
    }
    tone(PIN_BUZZER, 1000);
  } else {
    if (shutterClosed) {
      shutterServo.write(0);
      shutterClosed = false;
    }
    noTone(PIN_BUZZER);
  }
}

void actuateOutputs() {
  digitalWrite(PIN_DISCHG_FET, dischargeAllowed ? HIGH : LOW);
  digitalWrite(PIN_CHG_RELAY, chargeAllowed ? HIGH : LOW);

  switch (thermalState) {
    case STANDBY:
    case CHARGE_WAIT:
      damperServo.write(0);
      analogWrite(PIN_FAN_PWM, 0);
      break;
    case PREHEAT: {
      damperServo.write(90);
      float delta = blockTemp - batteryTemp;
      int fanSpeed = map((int)constrain(delta, 10.0f, 100.0f), 10, 100, 50, 255);
      analogWrite(PIN_FAN_PWM, fanSpeed);
      break;
    }
    case OVERHEAT_PROTECT:
      damperServo.write(0);
      analogWrite(PIN_FAN_PWM, 255);
      break;
  }

  digitalWrite(PIN_LED_OK, faultState ? LOW : HIGH);
  digitalWrite(PIN_LED_FAULT, faultState ? HIGH : LOW);

  static unsigned long lastFaultBeep = 0;
  if (faultState && !motionDetected && millis() - lastFaultBeep > 1000) {
    tone(PIN_BUZZER, 800, 200);
    lastFaultBeep = millis();
  }
}

void serialDebug() {
  Serial.print("V:");
  Serial.print(cellVoltage, 3);
  Serial.print(" BatT:");
  Serial.print(batteryTemp, 1);
  Serial.print(" BlockT:");
  Serial.print(blockTemp, 1);
  Serial.print(" I:");
  Serial.print(currentAmps, 3);
  Serial.print(" Chg:");
  Serial.print(chargeAllowed);
  Serial.print(" Dsch:");
  Serial.print(dischargeAllowed);
  Serial.print(" ThState:");
  Serial.print((int)thermalState);
  Serial.print(" Light:");
  Serial.print(lightPercent, 0);
  Serial.print(" Sunrise:");
  Serial.print(sunrisePredicted);
  Serial.print(" Motion:");
  Serial.println(motionDetected);
}
