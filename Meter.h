/**
 * Abstract driving an analog meter to be driven by PWM,
 * and do the math to calculate the right PWM values.
 */
class Meter {
	private:
		/**
		 * An analogWrite of analogMax*255*value wil set the meter
		 * to value fraction of its full range.
		 */
		const float analogMax;
		const int pin;
	public:
		Meter(int pin, float maxCurrent,
			float seriesResistance, float internalResistance);
		void setup();
		void setValue(float value);
};

