#include "uart.h"
#define USART0_ENABLED
#define F_CPU 16000000UL		// Define Crystal Frequency of Uno Board
#include <avr/io.h>				// Standard AVR IO Library
#include <util/delay.h> 			// Standard AVR Delay Library
#include<avr/interrupt.h>
#define SET(port,bit) port |=(1<<bit)
#define CLR(port,bit) port &=~(1<<bit)
#define TOGGLE(port,bit)port ^= (1<<bit)
#define pin0 PD0
#define pin1 PD1
#define pin2 PD2
#define pin3 PD3
#define pin4 PD4
#define pin5 PD5
#define pin6 PD6
#define pin7 PD7
#define pin8 PB0
#define pin9 PB2
#define pin10 PB1
#define pin11 PB3
#define pin12 PB4
#define pin13 PB5
#define A0 PC0
#define A1 PC1
#define A2 PC2
#define A3 PC3
#define A4 PC4
#define A5 PC5
#define D DDRD
#define B DDRB
#define C DDRC

int final_stop;
char uart0_readByte(void){

	uint16_t rx;
	uint8_t rx_status, rx_data;

	rx = uart0_getc();
	rx_status = (uint8_t)(rx >> 8);
	rx = rx << 8;
	rx_data = (uint8_t)(rx >> 8);

	if(rx_status == 0 && rx_data != 0){
		return rx_data;
	} else {
		return -1;
	}

}

void init_button(void){
	CLR(D,pin2);
	CLR(D,pin3);     //sensor pin as input
	CLR(D,pin4);
	
	SET(D,pin6);
	SET(B,pin11);    //speed pin as output
	
	SET(PORTD,pin6);	//speed pin as output
	SET(PORTB,pin11);
	
	SET(D,pin7);
	SET(B,pin8);    //direction pin as output
	SET(B,pin9);
	SET(B,pin10);
	
	SET(B,pin12);		//buzzer pin as output
	CLR(PORTB,pin12);
	
	SET(B,pin13);		//striking mechanism pin as output
	
		SET(D,pin2);		
		SET(PORTD,pin2);
}

void timer_init()
{
	cli(); //disable all interrupts
	
	TCCR0B = 0x00;	//Stop
	
	TCNT0 = 0xFF;	//Counter higher 8-bit value to which OCR2A value is compared with
	
	OCR0A = 0xFF;	//Output compare register low value for Led
	
	//  Clear OC2A, on compare match (set output to low level)
	TCCR0A |= (1 << COM0A1);
	TCCR0A &= ~(1 << COM0A0);

	// FAST PWM 8-bit Mode
	TCCR0A |= (1 << WGM00);
	TCCR0A |= (1 << WGM01);
	TCCR0B &= ~(1 << WGM02);
	
	// Set Prescalar to 64
	TCCR0B &= ~((1 << CS01) | (1 << CS00));
	TCCR0B |= (1 << CS02);
	
	
	TCCR2B = 0x00;	//Stop
	
	TCNT2 = 0xFF;	//Counter higher 8-bit value to which OCR2A value is compared with
	
	OCR2A = 0xFF;	//Output compare register low value for Led
	
	//  Clear OC2A, on compare match (set output to low level)
	TCCR2A |= (1 << COM2A1);
	TCCR2A &= ~(1 << COM2A0);

	// FAST PWM 8-bit Mode
	TCCR2A |= (1 << WGM20);
	TCCR2A |= (1 << WGM21);
	TCCR2B &= ~(1 << WGM22);
	
	// Set Prescalar to 64
	TCCR2B &= ~((1 << CS21) | (1 << CS20));
	TCCR2B |= (1 << CS22);
	sei(); //re-enable interrupts
}
void R_motor_speed(unsigned char R_speed){
OCR0A = 255 - (unsigned char)R_speed;	}

void L_motor_speed(unsigned char L_speed){
OCR2A = 255 - (unsigned char)L_speed; 	}

void buzzer_on(void){
	SET(PORTB,pin12);
}
void buzzer_off(void){
	CLR(PORTB,pin12);
}
unsigned char one(void){
	unsigned char status1 = PIND & (1 << 2);	// Read PIN_BUTTON
	return status1;
}
unsigned char two(void){
	unsigned char status2 = PIND & (1 << 3);	// Read PIN_BUTTON
	return status2;
}
unsigned char three(void){
	unsigned char status3 =PIND & (1 << 4);	// Read PIN_BUTTON
	return status3;
}
int main(void){
	timer_init();
	init_button();
	char rx_byte;
	
	uart0_init(UART_BAUD_SELECT(9600, F_CPU));
	uart0_flush();
	uart0_puts("*** Arduino Uno UART0 ECHO ***\n");
	while(1)
	{
		rx_byte = uart0_readByte();
		if(rx_byte =='f'){
			forward();
		}
		if(rx_byte =='b'){
			backward();
		}
	}
}

stop(int sig){
	R_motor_speed(255-0);
	L_motor_speed(255-0);
	buzzer_on();	_delay_ms(1000);		buzzer_off();		//beep for 1 sec
	SET(PORTB,pin13);											//strike & wait for 2 sec
	_delay_ms(2000);
	buzzer_on();	_delay_ms(2000);		buzzer_off();		//beep for 2 sec
	final_stop=1;
if(sig==1){	backward();		}
	if(sig==2){	forward();		}
}
final_stoper(){
	_delay_ms(2000);
	R_motor_speed(255-0);
	L_motor_speed(255-0);
	buzzer_on();	_delay_ms(8000);		buzzer_off();		//beep for 1 sec
	while(1){}
}

forward(){
unsigned char a,b,c;
		SET(PORTD,pin7);  SET(PORTB,pin9);			//direction pin as backward
		CLR(PORTB,pin8);  CLR(PORTB,pin10);
		char rx_byte;
		while(1){
L_motor_speed(255-94.6);	R_motor_speed(255-41.8);			//We have used the concept of radius and angle to find the circumferincial distance hence the speeds provided make the bot the move in a perfect circle.
			//over this we have the possibility of adding the white line sensor values and then adjust the bot only when it leaves the track
		a=one();
		b=two();
		c=three();

		if(a == 0){
			L_motor_speed(255-255);
		} else {
			L_motor_speed(255-0);
		}
		
		if(b == 0){
			SET(PORTB,pin12);
		} else {
			CLR(PORTB,pin12);
		}
		
		if(c == 0){
			R_motor_speed(255-255);
		} else {
			R_motor_speed(255-0);
		}		
		
		rx_byte = uart0_readByte();
		if(rx_byte =='s'){
			if(final_stop==1){	final_stoper();}
			stop(1);			
		}
	}
}

backward(){
unsigned char a,b,c;
	CLR(PORTD,pin7);  CLR(PORTB,pin9);			//direction pin as backward
	SET(PORTB,pin8);  SET(PORTB,pin10);
	char rx_byte;
	while(1){
R_motor_speed(255-41.15);
L_motor_speed(255-95);	
		if(a == 0){
			L_motor_speed(255-255);
		} else {
			L_motor_speed(255-0);
		}
		
		if(b == 0){
			SET(PORTB,pin12);
		} else {
			CLR(PORTB,pin12);
		}
		
		if(c == 0){
			R_motor_speed(255-255);
		} else {
			R_motor_speed(255-0);
		}		
		rx_byte = uart0_readByte();		
		if(rx_byte =='s'){
			if(final_stop==1){	final_stoper();}
			stop(2);
		}
	}	
}