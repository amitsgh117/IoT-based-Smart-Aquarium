float CALIBRATION_value = 29; // using pH = 7 for distilled water
int N = 10, counter=0;
void setup(){
  pinMode(12,OUTPUT); // RELAY PIN
  digitalWrite(12,HIGH);  // RELAY OFF
  Serial.begin(9600);
  delay(2000);
}
void loop() {
  int values[N];
  for(int i=0;i<N;i++){ 
    values[i]=analogRead(A0); // arduino readings
    delay(30);
  }
  
  // sorting
  int i=0; 
  while(i<N-1){
    int j = i+1;
    while(j<N){
      if(values[i]>values[j]){
        int temp=values[i];
        values[i]=values[j];
        values[j]=temp;
      }
      j++;
    }
    i++;
  }

  // taking average of middle values of above sorted arduino data 
  int pH_sum=0;
  for(int i=2;i<N-2;i++){
    pH_sum+=values[i];
  }
  
  // pH_sum/6 is the average
  float V = (float)pH_sum*5.0/1024/6;  // using nernst equation
  float pH = -5.70 * V + CALIBRATION_value;
  
  // controlling relay (which controls the solenoid valve for non ideal pH conditions)  
  if(counter%5==1){ // checking after every 10 seconds
    if(pH > 8.0 || pH < 6.5){
      digitalWrite(12,LOW); // RELAY ON
      delay(2000);
      digitalWrite(12,HIGH); // RELAY OFF
    }
    else{
      digitalWrite(12,HIGH); // RELAY OFF
    }  
  }
  counter+=1;
  
  Serial.println(pH); // print + SERIAL COMMUNICATION for sending these values to raspberry pi
  delay(2000);
}
