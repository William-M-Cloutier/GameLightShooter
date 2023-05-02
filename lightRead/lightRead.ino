#define L1 A2
#define L2 A3
#define L3 A4

//The below values are used to bring the read
//in values to 0 so we only look at difference
//in light 
int c1 = 0; 
int c2 = 0; 
int c3 = 0; 
//read values hold the current read value
int r1 = 0; 
int r2 = 0; 
int r3 = 0; 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); 
  // delay(50); 
  calibrate(); 
}

void loop() {
  // put your main code here, to run repeatedly:

  // Serial.print(c1); 
  // readVals(); 

  readCorrectVals(); 
  // Serial.println(r1); 

  // Serial.println(r1);
  // Serial.print(" ");
  // Serial.print(c2);
  // Serial.print(" ");  
  // Serial.println(r2); 
  // Serial.print(" "); 
  // Serial.println(r3);  

  printVals(); 
  delay(50); 
}

void printVals(){
  Serial.print(r1);
  Serial.print(" ");
  Serial.print(r2); 
  Serial.print(" "); 
  Serial.println(r3);  
}

void readVals(){
  r1 = analogRead(L1); 
  r2 = analogRead(L2); 
  r3 = analogRead(L3); 
}

void readCorrectVals(){
  readVals();  

  r1 -= c1; 
  r2 -= c2; 
  r3 -= c3; 

  if(r1 < 0){
    r1 = 0; 
  }
  if(r2 < 0){
    r2 = 0; 
  }
  if(r3 < 0){
    r3 = 0; 
  }
}

void calibrate(){
  int tot1 = 0; 
  int tot2 = 0; 
  int tot3 = 0; 
  for(int i = 0; i < 20; i++){
    tot1 += analogRead(L1); 
    tot2 += analogRead(L2); 
    tot3 += analogRead(L3); 
  }
  Serial.println(tot1); 
  Serial.println(tot2); 
  c1 = tot1/20; 
  c2 = tot2/20; 
  c3 = tot3/20; 
}
