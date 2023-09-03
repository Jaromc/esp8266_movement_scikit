#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>

/* Assign a unique ID to this sensor at the same time */
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

#include "eml_common.h"
#include "eml_net.h"
#include "model.h"

// array to map gesture index to a name
const char* GESTURES[] = {
  "pitch",
  "yaw",
  "roll"
};

const int NUM_SAMPLES = 10;
int samplesRead = 0;
float sample_array[NUM_SAMPLES*3];

void setup() {
  //Serial.begin(115200);
  Serial.begin(9600);
  Serial.println("HMC5883 Magnetometer Test"); Serial.println("");
  
  /* Initialise the sensor */
  if(!mag.begin())
  {
    /* There was a problem detecting the HMC5883 ... check your connections */
    Serial.println("Ooops, no HMC5883 detected ... Check your wiring!");
    while(1);
  }
}

void loop() {
  sensors_event_t event; 
  mag.getEvent(&event);

  //normalise the data
  sample_array[samplesRead * 3 + 0] = (event.magnetic.x + 90.0) / 180.0;
  sample_array[samplesRead * 3 + 1] = (event.magnetic.y + 90.0) / 180.0;
  sample_array[samplesRead * 3 + 2] = (event.magnetic.z + 90.0) / 180.0;

  samplesRead++;

  // gather thre required samples
  if (samplesRead == NUM_SAMPLES) {

    long int start_time = micros();

    const int32_t predicted_class = model_predict(sample_array, NUM_SAMPLES*3);

    Serial.print("Inference time (us): ");
    Serial.println(micros() - start_time);

    Serial.print("Prediction: ");
    Serial.println(predicted_class);

    samplesRead = 0;
    delay(1000);
  }
}