#include <DHT.h>

// 핀 및 상수 정의
#define DHTPIN 2  // DHT 센서 데이터 핀
#define DHTTYPE DHT11
#define LED_PIN 9
#define BUZZER_PIN 10

// DHT 센서 초기화
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  // 온도와 습도 읽기
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // 값이 정상적으로 읽혔는지 확인
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("DHT 센서에서 데이터를 읽을 수 없습니다.");
    return;
  }

  // 값 출력
  Serial.print("온도: ");
  Serial.print(temperature);
  Serial.print("°C, 습도: ");
  Serial.print(humidity);
  Serial.println("%");

  // 경고 조건 확인
  if (temperature >= 30 || humidity >= 70) {
    digitalWrite(LED_PIN, HIGH);   // LED 켜기
    digitalWrite(BUZZER_PIN, HIGH); // 부저 울리기
    delay(1000);                  // 1초 대기
    digitalWrite(LED_PIN, LOW);   // LED 끄기
    digitalWrite(BUZZER_PIN, LOW); // 부저 끄기
  }

  delay(2000); // 2초 대기
}
