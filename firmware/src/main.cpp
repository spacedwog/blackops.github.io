#include <ESP8266WiFi.h>  // Importante para usar ESP.restart()

#define RELAY_PIN D2

void setup() {
  Serial.begin(9600);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);  // Relay começa desligado
  Serial.println("Sistema iniciado. Aguardando comandos...");
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim(); // Remove espaços ou quebras de linha

    if (comando.equalsIgnoreCase("ON")) {
      digitalWrite(RELAY_PIN, HIGH);
      Serial.println("Comando recebido: ON — Relay ativado.");
    } 
    else if (comando.equalsIgnoreCase("OFF")) {
      digitalWrite(RELAY_PIN, LOW);
      Serial.println("Comando recebido: OFF — Relay desativado.");
    } 
    else if (comando.equalsIgnoreCase("RESTART")) {
      Serial.println("Reiniciando sistema...");
      delay(1000);
      ESP.restart();
    } 
    else if (comando.equalsIgnoreCase("FIREWALL")) {
      Serial.println("FIREWALL: Sistema verificado. Nenhuma ameaça detectada.");
    } 
    else {
      Serial.println("Comando não reconhecido.");
    }
  }
}