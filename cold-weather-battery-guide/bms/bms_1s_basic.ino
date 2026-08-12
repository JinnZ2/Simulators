/*
 * BMS 1S Basic — Single-cell LFP battery management with low-temperature
 * charge lockout. Reads cell voltage, battery temperature, and pack current;
 * enables/disables charge and discharge paths accordingly.
 *
 * Hardware:
 *   Arduino Nano or Uno (5V)
 *   INA219 current sensor (I2C, A4/A5)
 *   NTC thermistor 10k @ 25 C, Beta 3950, in 10k divider to 5V (A1)
 *   Cell voltage via 100k+10k divider to A0
 *   Discharge MOSFET IRLZ44N gate on D3
 *   Charge relay via NPN + 12V coil on D4
 *   Fault LED (red) on D5, OK LED (green) on D6, buzzer on D7
 *
 * Wire the shunt in the negative battery lead; INA219 VIN+ toward battery
 * negative, VIN- toward load negative. Relay is normally-energized when
 * charge is allowed so it fails safe (open) on loss of Arduino power.
 *
 * CC0.
 */

#include <Wire.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 ina219;

const int VOLTAGE_PIN = A0;
const int TEMP_PIN = A1;
const int DISCHARGE_FET = 3;
const int CHARGE_RELAY = 4;
const int FAULT_LED = 5;
const int OK_LED = 6;
const int BUZZER = 7;

const float VOLTAGE_DIVIDER_RATIO = (100000.0 + 10000.0) / 10000.0; // ~11:1
const float VREF = 5.0;
const float ADC_RES = 1024.0;

const float SERIES_RESISTOR = 10000.0;
const float NOMINAL_RES = 10000.0;
const float NOMINAL_TEMP = 25.0;
const float BETA = 3950.0;

// LFP thresholds
const float CELL_OV = 3.65;
const float CELL_UV = 2.50;
const float CELL_OV_RELEASE = 3.40;
const float CELL_UV_RELEASE = 2.80;
const float CHARGE_TEMP_MIN = -10.0;  // no charging below this
const float CHARGE_TEMP_MAX = 60.0;
const float OVERCURRENT_A = 2.0;

bool chargeAllowed = true;
bool dischargeAllowed = true;
bool faultState = false;

float cellVoltage = 0.0;
float temperature = 0.0;
float current = 0.0;

void setup() {
  pinMode(DISCHARGE_FET, OUTPUT);
  pinMode(CHARGE_RELAY, OUTPUT);
  pinMode(FAULT_LED, OUTPUT);
  pinMode(OK_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  digitalWrite(DISCHARGE_FET, HIGH);
  digitalWrite(CHARGE_RELAY, HIGH);
  digitalWrite(FAULT_LED, LOW);
  digitalWrite(OK_LED, HIGH);
  digitalWrite(BUZZER, LOW);

  Serial.begin(9600);
  if (!ina219.begin()) {
    Serial.println("INA219 not found - check wiring");
  }
}

void loop() {
  int rawADC = analogRead(VOLTAGE_PIN);
  float voltageInput = rawADC * VREF / ADC_RES;
  cellVoltage = voltageInput * VOLTAGE_DIVIDER_RATIO;

  rawADC = analogRead(TEMP_PIN);
  float resistance = SERIES_RESISTOR * (ADC_RES / rawADC - 1.0);
  float steinhart = log(resistance / NOMINAL_RES) / BETA + 1.0 / (NOMINAL_TEMP + 273.15);
  float tempK = 1.0 / steinhart;
  temperature = tempK - 273.15;

  current = ina219.getCurrent_mA() / 1000.0;

  if (cellVoltage > CELL_OV) chargeAllowed = false;
  if (cellVoltage < CELL_OV_RELEASE) chargeAllowed = true;

  if (cellVoltage < CELL_UV) dischargeAllowed = false;
  if (cellVoltage > CELL_UV_RELEASE) dischargeAllowed = true;

  if (abs(current) > OVERCURRENT_A) {
    chargeAllowed = false;
    dischargeAllowed = false;
    faultState = true;
  } else if (faultState && abs(current) < 0.1) {
    faultState = false;
  }

  if (temperature < CHARGE_TEMP_MIN || temperature > CHARGE_TEMP_MAX) {
    chargeAllowed = false;
  } else if (cellVoltage < CELL_OV_RELEASE) {
    chargeAllowed = true;
  }

  digitalWrite(DISCHARGE_FET, dischargeAllowed ? HIGH : LOW);
  digitalWrite(CHARGE_RELAY, chargeAllowed ? HIGH : LOW);

  bool anyFault = (!chargeAllowed || !dischargeAllowed || faultState);
  digitalWrite(FAULT_LED, anyFault ? HIGH : LOW);
  digitalWrite(OK_LED, anyFault ? LOW : HIGH);
  if (anyFault) tone(BUZZER, 1000, 200);

  Serial.print("Vcell:");
  Serial.print(cellVoltage, 3);
  Serial.print(" T:");
  Serial.print(temperature, 1);
  Serial.print(" I:");
  Serial.print(current, 3);
  Serial.print(" Chg:");
  Serial.print(chargeAllowed);
  Serial.print(" Dischg:");
  Serial.println(dischargeAllowed);

  delay(500);
}
