void setup() {
  Serial.begin(9600); // Inicia a comunicação serial a 9600 bps.
}

void loop() {
  for (int pin = A0; pin <= A3; pin++) {
    int sensorValue = analogRead(pin); // Lê o valor analógico.
    Serial.print(sensorValue);
    if (pin < A3) {
      Serial.print(","); // Adiciona uma vírgula entre os valores, exceto após o último valor.
    }
  }
  Serial.println(); // Finaliza a linha para o conjunto de valores.
  delay(200); // Pequena pausa para não saturar a comunicação serial.
}
